// Opens the left navigation at the section that contains the current link target.
// The theme only does this when the link target is the section itself; with this script it also works for
// links to labels (e.g. ":ref:`Installed capacity <param-installed-capacity>`" or ":ref:`Sink <comp-sink>`").
(function () {
  function openNav() {
    var hash = decodeURIComponent(window.location.hash.slice(1));
    var menu = document.querySelector(".wy-menu-vertical");
    var target = hash && document.getElementById(hash);
    if (!menu || !target) return;
    var sec = target.tagName === "SECTION" ? target : target.closest("section");
    var link = null;
    while (sec && !link) {
      link = menu.querySelector('a[href="#' + CSS.escape(sec.id) + '"]');
      sec = sec.parentElement ? sec.parentElement.closest("section") : null;
    }
    if (!link) return;
    menu.querySelectorAll(".current").forEach(function (el) {
      el.classList.remove("current");
      el.setAttribute("aria-expanded", "false");
    });
    link.classList.add("current");
    for (var li = link.closest("li"); li; li = li.parentElement.closest("li")) {
      li.classList.add("current");
      li.setAttribute("aria-expanded", "true");
    }
    var l1 = link.closest("li.toctree-l1");
    if (l1 && l1.parentElement) l1.parentElement.classList.add("current");
    var side = document.querySelector(".wy-side-scroll");
    if (side) {
      var top = link.getBoundingClientRect().top - side.getBoundingClientRect().top + side.scrollTop;
      side.scrollTop = Math.max(0, top - side.clientHeight / 3);
    }
  }
  window.addEventListener("hashchange", function () { setTimeout(openNav, 0); });
  window.addEventListener("load", function () { setTimeout(openNav, 50); });
})();
