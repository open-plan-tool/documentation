# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath(".."))




# def copy_readme():
    # with open("../README.rst", "r", encoding="utf8") as fp:
        # data = fp.readlines()
    # with open("readme.inc", "w") as fp:
        # fp.writelines(data[data.index("Setup\n") :])
#
# # Page "Component models" (model/components.rst), generated from the parameter list

DOCS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = DOCS_DIR / "_scripts"

sys.path.insert(0, str(SCRIPTS_DIR))

from component_models_csv import build_component_models

build_component_models(
    parameter_file="parameter_list_eesyplan.csv",
    label_file="parameter_long_description_eesyplan.csv",
    intro_file="component_hdrs.csv",
    output="model/components.rst",
    input_output="model/input_parameters.rst",
)



# copy_readme()

# -- Project information -----------------------------------------------------

project = "open_plan"
copyright = "2023, Reiner Lemoine Institut and Open Plan team"
author = "Reiner Lemoine Institut and Open Plan team"

# from multi_vector_simulator.version import version_num

# release = version_num

# -- General configuration ---------------------------------------------------

master_doc = "index"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.imgmath",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.extlinks",
    # "sphinxcontrib.rsvgconverter",
    "numpydoc",
    "sphinxcontrib.jquery",  # the navigation of the theme needs jQuery
]

mathjax_path="https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS-MML_HTMLorMML"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# generate autosummary even if no references
autosummary_generate = True
autosummary_imported_members = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

numpydoc_show_class_members = False

html_theme = "sphinx_rtd_theme"

#html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'table-style.css',
    'components.css',  # page "Component models"
]

html_js_files = ['nav-fix.js']  # opens the navigation also for links to labels
