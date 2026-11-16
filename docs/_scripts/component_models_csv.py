"""Generate the component-model and input-parameter documentation from CSV files.

Expected input files:
- Parameter.csv: component and parameter definitions
- Label.csv: label -> long description
- Headers.csv: heading -> introduction

The script is called from ``conf.py`` during documentation builds and can also
be run directly from the ``docs`` directory:

    python _scripts/component_models_csv.py parameter_list_eesyplan.csv parameter_long_description_eesyplan.csv component_hdrs.csv
"""


import csv
import html
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict


DOCS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AREA_ORDER = [  # areas not listed here are added at the end in input order
    "Energy bus", "Energy consumption", "Energy production", "Energy conversion", "Energy providers",
    "Energy storage", "Energy transport", "Energy excess", "Energy shortage",
]
PAGE_TITLE = "Component models"
INPUT_TITLE = "Input parameters"
PARAM_FILE = "Parameter.csv"
LABEL_FILE = "Label.csv"
INTRO_FILE = "Headers.csv"
COMPONENT_ROW = "name"  # parameter_name of the row that describes the component itself

# column C "Component published on OpenPlan": components with one of these values are shown.
# To show more components, add e.g. "staging,sandbox".
PUBLISHED = {"production"}
# components that are not shown although column C says so (e.g. EnergyStorage: row "name" says production,
# all other rows say no)
HIDDEN_COMPONENTS = {"EnergyStorage"}
IGNORED_TEXTS = {"asset_name"}  # column J of the row "name": values that are not shown below the table
# a line of the component description (column M, row "name") that starts with this text is the source of the
# default parameter set. It is always taken out of the description. With SHOW_SOURCE = True it is shown below the
# table after the text of column J ("... – Source: ..."), with False it is not shown at all.
SOURCE_PREFIX = "Source of default parameter set:"
SHOW_SOURCE = False

ICON_DIR = "_static/icons"  # icon of a component: <component name>.svg or .png (relative to the folder docs)
ICON_EXT = (".svg", ".png")
IMAGE_DIR = "images/components"  # graphics for pages, areas, components and labels (relative to the folder docs)
IMAGE_EXT = (".png", ".svg", ".jpg", ".jpeg", ".gif")
# labels of the old page "Input parameters" (MVS parameter list) that other pages still refer to -> new label;
# they are placed as additional targets on the new page, so the old links keep working
LEGACY_LABELS = {
    "installedcap-label": "installed_capacity", "maxcap-label": "maximum_capacity",
    "efficiency-label": "conversion_efficiency", "crate-label": "charging_c_rate",
    "dispatchprice-label": "variable_costs", "lifetime-label": "lifetime_asset",
    "specificcosts-label": "specific_investment_costs", "specificomcosts-label": "specific_operation_costs",
    "socmin-label": "min_state_of_charge", "socmax-label": "max_state_of_charge",
    "energyprice-label": "energy_price", "feedintariff-label": "feedin_tariff",
    "feedincap-label": "maximum_feed_in_power", "peakdemand-label": "peak_demand_pricing",
    "peakdemandperiod-label": "peak_demand_pricing_period", "renshare-label": "renewable_share",
}

# key -> (headers in the CSV file, lower case; a header also matches if it starts with one of them;
#         fallback column index if no header matches)
COLUMNS = {
    "parameter": (["parameter_name"], 0),
    "component": (["component"], 1),
    "published": (["component published on openplan"], 2),
    "show": (["show parameter in gui"], 3),
    "type": (["input type openplan"], 5),
    "title": (["description of the parameter in openplan"], 6),
    "default": (["default value"], 7),
    "unit": (["unit"], 8),
    "set_text": (["short description"], 9),
    "area": (["component category for documentation"], 10),
    "label": (["label for long description"], 11),
    "text": (["long description"], 12),
}
# column F: these types go into the table (numbers and timeseries); "float | int | None" counts too
TABLE_TYPES = re.compile(r"\b(float|int|arraylike)\b", re.I)
INPUT_TEXT = "user input"  # this text in default column (no default, the user enters the value) is shown grey and italic
YES = {"yes", "ja", "y", "true", "1", "x"}
NO = {"no", "nein", "n", "false", "0"}


# ------------------------------------------------------------------ helpers
def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def heading(title, char, overline=False):
    line = char * len(title)
    return f"{line}\n{title}\n{line}\n" if overline else f"{title}\n{line}\n"


def rst_text(text):
    """Escape characters with a special meaning in reStructuredText; one paragraph per line of the cell."""
    text = re.sub(r"([\\*`|_])", r"\\\1", str(text).strip())
    return "\n\n".join(p.strip() for p in re.split(r"\n\s*\n|\n", text) if p.strip())


def rst_inline(text):
    return re.sub(r"([\\*`|_])", r"\\\1", " ".join(str(text).split()))


def ref(text, label):
    return f":ref:`{text} <{label}>`"


def raw_html(lines):
    return [".. raw:: html", ""] + ["   " + line for line in lines] + [""]


def comp_id(name):
    return f"comp-{slug(name)}"


def own_param_id(name, title):
    return f"comp-{slug(name)}-{slug(title)}"


def input_id(key):
    return f"param-{slug(key)}"


def find_icon(icon_dir, name):
    """file name of the icon of a component: <name>.svg or <name>.png in icon_dir (None if there is none)"""
    return next((name + ext for ext in ICON_EXT if os.path.isfile(os.path.join(icon_dir, name + ext))), None)


def image_key(name):
    """file name rule for graphics: lower case, spaces (and other separators) -> '_'"""
    return re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")


def find_graphics(image_dir):
    """All graphics in image_dir: {image_key: [(file, caption or None), ...]} sorted by number.
    'HeatPump.png' -> key 'heatpump'; 'HeatPump_2.png' -> key 'heatpump', number 2."""
    found = defaultdict(list)
    if not os.path.isdir(image_dir):
        return found
    for file in sorted(os.listdir(image_dir)):
        stem, ext = os.path.splitext(file)
        if ext.lower() not in IMAGE_EXT:
            continue
        m = re.match(r"^(.*?)(?:[_-](\d+))?$", stem)
        caption_file = os.path.join(image_dir, stem + ".txt")
        caption = open(caption_file, encoding="utf-8").read().strip() if os.path.exists(caption_file) else None
        found[image_key(m.group(1))].append((int(m.group(2) or 0), file, caption or None))
    return {k: [(f, c) for _, f, c in sorted(v)] for k, v in found.items()}


def graphic_rst(url, file, caption, alt):
    """one graphic as reStructuredText: image, or figure if there is a caption"""
    if caption:
        return [f".. figure:: {url}{file}", f"   :alt: {alt}", "   :figclass: cm-graphic", "",
                "   " + rst_inline(caption), ""]
    return [f".. image:: {url}{file}", f"   :alt: {alt}", "   :class: cm-graphic", ""]


def format_default(value):
    """Default value for the table as it is in the CSV file (column H), numbers in German format.
    Empty cells and "None" stay empty; technical values derived from other parameters (self.*) are shown as '–'."""
    if value is None or (isinstance(value, str) and value.strip() in ("", "None", "none")):
        return ""
    if isinstance(value, str) and value.strip().startswith("self."):
        return "–"
    if isinstance(value, bool) or (isinstance(value, str) and value.strip() in ("True", "False")):
        return "yes" if str(value) == "True" else "no"
    if isinstance(value, (int, float)):
        if float(value).is_integer():
            return f"{int(value):,}".replace(",", ".")
        whole, frac = f"{value:.6f}".rstrip("0").split(".")
        return f"{int(whole):,}".replace(",", ".") + "," + frac
    return str(value).strip()


def cap(text):
    return text[:1].upper() + text[1:]


def is_yes(value, default):
    v = str(value).strip().lower() if value is not None else ""
    return True if v in YES else False if v in NO else default


# ------------------------------------------------------------------ read the CSV files
def find_columns(header_row):
    """column index of every key in COLUMNS, found by the header (exact or as beginning of the header)"""
    header = [str(h or "").strip().lower() for h in header_row]
    col = {}
    for key, (names, fallback) in COLUMNS.items():
        col[key] = next((i for n in names for i, h in enumerate(header) if h == n), None)
        if col[key] is None:
            col[key] = next((i for n in names for i, h in enumerate(header) if h.startswith(n)), fallback)
    return col


def read_csv_rows(path):
    """Return all rows from a UTF-8 CSV file.

    A delimiter is detected from comma, semicolon, or tab. ``utf-8-sig`` also
    handles CSV files exported with a UTF-8 BOM.
    """
    with open(path, encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        return list(csv.reader(f, dialect))


def read_labels(path):
    labels = OrderedDict()
    rows = read_csv_rows(path)
    for row in rows[1:]:
        if row and row[0]:
            labels[str(row[0]).strip()] = (
                str(row[1]).strip() if len(row) > 1 and row[1] else ""
            )
    return labels


def read_intros(path):
    intros = {}
    if not os.path.exists(path):
        return intros

    rows = read_csv_rows(path)
    for row in rows[1:]:
        if not (row and row[0] and len(row) > 1 and row[1] and str(row[1]).strip()):
            continue
        key = str(row[0]).replace("¶", "").strip().lower()
        intros[key] = (
            str(row[1])
            .replace("\r\n", "\n")
            .replace("\r", "\n")
            .strip("\n")
        )
    return intros


def read_parameter_list(parameter_path, label_path, intro_path):
    rows = read_csv_rows(parameter_path)
    if not rows:
        raise ValueError(f"Parameter file is empty: {parameter_path}")

    col = find_columns(rows[0])
    labels = read_labels(label_path)
    intros = read_intros(intro_path)

    areas_by_lower = {a.lower(): a for a in AREA_ORDER}

    def area_name(value):
        value = " ".join(str(value or "").split())
        return areas_by_lower.get(value.lower(), value)

    components = OrderedDict()
    warnings = []
    seen = {}

    for n, row in enumerate(rows[1:], start=2):
        def get(key):
            return row[col[key]] if col[key] < len(row) else None

        name = get("component")
        if not name:
            continue

        name = str(name).strip()
        comp = components.setdefault(
            name,
            {
                "area": area_name(get("area")),
                "show": False,
                "description": None,
                "default_set": None,
                "source": None,
                "params": [],
                "has_row": False,
                "warnings": [],
            },
        )

        parameter = str(get("parameter") or "").strip()
        title = str(get("title") or "").strip()

        if parameter == COMPONENT_ROW:
            comp["has_row"] = True
            comp["area"] = area_name(get("area")) or comp["area"]

            published = str(get("published") or "").strip().lower()
            comp["show"] = (
                published in {p.lower() for p in PUBLISHED}
                and name not in HIDDEN_COMPONENTS
            )

            description = str(get("text") or "").replace("\r\n", "\n").strip()
            source = re.search(
                r"(?im)^[ \t]*" + re.escape(SOURCE_PREFIX) + r".*$",
                description,
            )
            if source:
                description = (
                    description[: source.start()] + description[source.end() :]
                ).strip()

            comp["source"] = source.group(0).strip() if source else None
            comp["description"] = description or None

            set_text = str(get("set_text") or "").strip()
            comp["default_set"] = (
                set_text
                if set_text and set_text not in IGNORED_TEXTS
                else None
            )

            if is_yes(get("show"), default=False) and "asset_name" in labels:
                comp["params"].append(
                    {
                        "in_table": False,
                        "title": cap(title or "Name"),
                        "default": "",
                        "unit": "–",
                        "label": "asset_name",
                        "own_text": None,
                        "row": n,
                    }
                )
            continue

        if not is_yes(get("show"), default=False):
            continue

        key = (name, parameter or title)
        if key in seen:
            comp["warnings"].append(
                f"row {n}: parameter '{key[1]}' of {name} appears twice "
                f"(also row {seen[key]}), the second row is ignored"
            )
            continue
        seen[key] = n

        if not title:
            title = parameter.replace("_", " ")
            comp["warnings"].append(
                f"row {n}: {name}, '{parameter}' has no name in column "
                f"'description of the parameter in OpenPlan', '{title}' is used"
            )

        text = str(get("text") or "").strip()
        value_type = str(get("type") or "").strip()

        if not value_type:
            comp["warnings"].append(
                f"row {n}: {name}, '{title}' has no type "
                "(column 'input type OpenPlan'), it is shown in the table"
            )

        comp["params"].append(
            {
                "in_table": not value_type or bool(TABLE_TYPES.search(value_type)),
                "title": cap(title),
                "default": format_default(get("default")),
                "unit": (
                    str(get("unit")).strip()
                    if str(get("unit") or "").strip() not in ("", "None")
                    else "–"
                ),
                "label": str(get("label") or "").strip(),
                "own_text": (
                    text
                    if text and not text.lower().startswith("label:")
                    else None
                ),
                "row": n,
            }
        )

    for name, comp in components.items():
        if comp["show"]:
            warnings += comp["warnings"]
        if not comp["has_row"]:
            warnings.append(
                f"{name}: no row '{COMPONENT_ROW}', the component is not shown"
            )
        if comp["show"] and not comp["description"]:
            warnings.append(
                f"{name}: no description "
                f"(row '{COMPONENT_ROW}', column 'long description')"
            )
        if comp["show"] and not comp["area"]:
            warnings.append(
                f"{name}: no area "
                "(column 'Component category for documentation')"
            )

    return components, labels, intros, warnings


# ------------------------------------------------------------------ build both pages
def build_component_models(
    parameter_file=PARAM_FILE,
    label_file=LABEL_FILE,
    intro_file=INTRO_FILE,
    output="model/components.rst",
    input_output="model/input_parameters.rst",
    icon_dir=ICON_DIR,
    image_dir=IMAGE_DIR,
    docs_dir=DOCS_DIR,
):
    """Write the component-model and input-parameter RST pages."""
    parameter_file, label_file, intro_file, output, input_output, icon_dir, image_dir = (
        os.path.join(docs_dir, p)
        for p in (
            parameter_file,
            label_file,
            intro_file,
            output,
            input_output,
            icon_dir,
            image_dir,
        )
    )
    all_components, labels, intros, warnings = read_parameter_list(
        parameter_file,
        label_file,
        intro_file,
    )
    components = OrderedDict((n, c) for n, c in all_components.items() if c["show"])
    icon_url = os.path.relpath(icon_dir, os.path.dirname(output)).replace(os.sep, "/") + "/"
    icon_of = {}
    for name in components:
        icon_of[name] = find_icon(icon_dir, name)
        if not icon_of[name]:
            warnings.append(f"{name}: no icon (file {ICON_DIR}/{name}.svg is missing)")

    # which components use which label (only shown components and parameters)
    used_by, label_titles = defaultdict(list), defaultdict(Counter)
    for name, comp in components.items():
        for p in comp["params"]:
            if p["label"] in labels:
                if name not in used_by[p["label"]]:
                    used_by[p["label"]].append(name)
                label_titles[p["label"]][p["title"]] += 1

    def label_title(key):
        titles = label_titles[key]
        if not titles:
            return cap(key.replace("_", " "))
        stems = {t.split(" (")[0] for t in titles}
        if len(titles) > 1 and len(stems) == 1:  # e.g. "Timeseries (kW)" / "Timeseries (kW/kWp)" -> "Timeseries"
            return cap(stems.pop())
        return cap(titles.most_common(1)[0][0])

    def img(name):
        icon = icon_of.get(name)
        if not icon:
            return ""
        return f'<img class="" src="{icon_url}{icon}" alt="" title="{html.escape(name, quote=True)}">'

    def intro(heading_text):
        """Return the introduction text for a page or area, if present."""
        return intros.get(heading_text.lower())

    graphics_found, graphics_used = find_graphics(image_dir), set()

    def graphics(name, page_output, alt=None):
        """graphics from the folder images/components for a page, area, component or label (list of rst lines)"""
        key = image_key(name)
        if key in graphics_used:
            if key in graphics_found:
                warnings.append(f"graphics '{key}': the name fits twice (e.g. area and component), shown only once")
            return []
        graphics_used.add(key)
        url = os.path.relpath(image_dir, os.path.dirname(page_output)).replace(os.sep, "/") + "/"
        lines = []
        for file, caption in graphics_found.get(key, []):
            lines += graphic_rst(url, file, caption, alt or name)
        return lines

    areas = OrderedDict((a, []) for a in AREA_ORDER)
    for name, comp in components.items():
        areas.setdefault(comp["area"], []).append(name)
    areas = OrderedDict((a, n) for a, n in areas.items() if n)
    known = {PAGE_TITLE.lower(), INPUT_TITLE.lower()} | {a.lower() for a in areas}
    for key in intros:
        if key not in known:
            warnings.append(f"file '{os.path.basename(intro_file)}': '{key}' is neither a page nor an area with shown components")

    # ---------------------------------------------------------- page "Component models"
    out = [f".. This page is generated automatically from {os.path.basename(parameter_file)}, "
           f"{os.path.basename(label_file)} and {os.path.basename(intro_file)} by _scripts/component_models_csv.py.",
           "   Changes have to be made in the CSV files, not here.", "",
           ".. role:: cm-source", "", ".. role:: cm-input", "", ".. _component_models:", "", heading(PAGE_TITLE, "-")]
    page_intro = intro(PAGE_TITLE)
    if page_intro:
        out += [page_intro, ""]
    out += graphics(PAGE_TITLE, output)

    cards = ['<div class="cm-overview">']
    for area, names in areas.items():
        cards += ['  <div class="cm-card">',
                  f'    <a class="cm-card-title" href="#{slug(area)}">{html.escape(area)}'
                  f'<span class="cm-card-count">{len(names)}</span></a>',
                  '    <ul class="cm-card-list">']
        cards += [f'      <li><a href="#{comp_id(n)}">{img(n)}<span>{html.escape(n)}</span></a></li>' for n in names]
        cards += ["    </ul>", "  </div>"]
    cards += ["</div>"]
    out += raw_html(cards)

    no_link = []
    for area, names in areas.items():
        out += [f".. _{slug(area).replace('-', '_')}:", "", heading(area, "#")]
        out += raw_html(['<div class="cm-tiles">']
                        + [f'  <a class="cm-tile" href="#{comp_id(n)}">{img(n)}<span>{html.escape(n)}</span></a>'
                           for n in names] + ["</div>"])
        area_intro = intro(area)
        if area_intro:
            out += [area_intro, ""]
        out += graphics(area, output)
        for name in names:
            comp = components[name]
            out += [f".. _{comp_id(name)}:", "", heading(name, "="), ".. container:: cm-head", ""]
            icon = icon_of.get(name)
            if icon:
                out += [f"   .. image:: {icon_url}{icon}", f"      :alt: {name} icon", ""]
            for p in comp["params"]:
                if not p["own_text"] and p["label"] not in labels:
                    no_link.append(f"{name}: {p['title']}")
            table_params = [p for p in comp["params"] if p["in_table"]]
            if table_params:
                out += ["   .. list-table::", "      :header-rows: 1", "      :class: cm-param-table", "",
                        "      * - Parameter", "        - Default", "        - Unit"]
                for p in table_params:
                    if p["own_text"]:  # most specific description: the text at the component
                        cell = ref(rst_inline(p["title"]), own_param_id(name, p["title"]))
                    elif p["label"] in labels:
                        cell = ref(rst_inline(p["title"]), input_id(p["label"]))
                    else:
                        cell = rst_inline(p["title"])
                    default = (f":cm-input:`{rst_inline(p['default'])}`"
                               if p["default"].lower() == INPUT_TEXT.lower() else rst_inline(p["default"]))
                    out += [f"      * - {cell}", f"        - {default}",
                            f"        - {rst_inline(p['unit'])}"]
                out.append("")
            # below the table, small and grey: text of column J about the default parameter set and, if SHOW_SOURCE,
            # the source ("Source of default parameter set: X" -> "Source: X")
            below = [comp["default_set"]] if comp["default_set"] else []
            if SHOW_SOURCE and comp["source"]:
                below.append("Source: " + comp["source"][len(SOURCE_PREFIX):].strip())
            if below:
                out += ["   .. rst-class:: cm-default-set", "",
                        "   " + " – ".join(":cm-source:`" + rst_inline(t).replace("`", "'") + "`" for t in below), ""]
            if comp["description"]:
                out += [rst_text(comp["description"]), ""]
            out += graphics(name, output)
            for p in comp["params"]:
                if not p["own_text"]:
                    continue
                out += [f".. _{own_param_id(name, p['title'])}:", "", ".. rst-class:: cm-param", "",
                        heading(p["title"], "^"), rst_text(p["own_text"]), ""]
                if p["label"] in labels and len(used_by[p["label"]]) > 1:
                    out += [f"General description: {ref(label_title(p['label']), input_id(p['label']))}", ""]
            out.append("")
    write_if_changed(output, "\n".join(out).rstrip() + "\n")

    # ---------------------------------------------------------- page "Input parameters"
    keys = sorted((k for k in labels if used_by[k]), key=lambda k: label_title(k).lower())
    unused = [k for k in labels if not used_by[k]]
    inp = [f".. This page is generated automatically from {os.path.basename(parameter_file)}, "
           f"{os.path.basename(label_file)} and {os.path.basename(intro_file)} by _scripts/component_models_csv.py.",
           "   Changes have to be made in the CSV files, not here.", "",
           ".. _input_parameters:", "", heading(INPUT_TITLE, "=", overline=True)]
    input_intro = intro(INPUT_TITLE)
    if input_intro:
        inp += [input_intro, ""]
    inp += graphics(INPUT_TITLE, input_output)
    inp += [".. admonition:: Parameters on this page", "   :class: cm-params-box", "",
           "   " + ", ".join(ref(label_title(k), input_id(k)) for k in keys), ""]
    for key in keys:
        inp += [f".. _{old}:" for old, new in LEGACY_LABELS.items() if new == key]
        inp += [f".. _{input_id(key)}:", "", heading(label_title(key), "*", overline=True)]
        if labels[key]:
            inp += [rst_text(labels[key]), ""]
        inp += graphics(key, input_output, label_title(key))
        inp += ["**Used by:** " + ", ".join(ref(n, comp_id(n)) for n in used_by[key]), "", ""]
    write_if_changed(input_output, "\n".join(inp).rstrip() + "\n")

    hidden = [n for n, c in all_components.items() if not c["show"]]
    print(f"component_models: {len(components)} components in {len(areas)} areas"
          f"{f' ({len(hidden)} hidden)' if hidden else ''}, "
          f"{sum(len(c['params']) for c in components.values())} parameters "
          f"({sum(p['in_table'] for c in components.values() for p in c['params'])} in the tables), "
          f"{len(keys)} input parameters")
    if no_link:
        warnings.append(f"{len(no_link)} parameters without description (no label in Label CSV, no own text): "
                        + "; ".join(no_link))
    if unused:
        warnings.append("labels not used by any shown parameter: " + ", ".join(unused))
    for key, files in graphics_found.items():
        if key not in graphics_used:
            warnings.append("graphics not shown (name matches no page, area, shown component or label): "
                            + ", ".join(f for f, _ in files))
    for w in warnings:
        print("component_models WARNING:", w)
    return warnings


def write_if_changed(path, text):
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if text != old:  # avoids unnecessary rebuilds
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)



if __name__ == "__main__":
    if len(sys.argv) == 4:
        build_component_models(
            parameter_file=sys.argv[1],
            label_file=sys.argv[2],
            intro_file=sys.argv[3],
            docs_dir=os.getcwd(),
        )
    else:
        print(
            "Usage: python _scripts/component_models_csv.py "
            "Parameter.csv Label.csv Headers.csv"
        )