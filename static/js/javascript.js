/*document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".nav-links");

  if (!btn || !nav) return;

  btn.addEventListener("click", () => {
    nav.classList.toggle("open");
    const isOpen = nav.classList.contains("open");
    btn.setAttribute("aria-expanded", String(isOpen));
  });

  // Optional: close menu if user clicks outside
  document.addEventListener("click", (e) => {
    if (!nav.contains(e.target) && !btn.contains(e.target)) {
      nav.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    }
  });
});*/

document.addEventListener("DOMContentLoaded", function () {
  var btn = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav-links");

  if (!btn || !nav) return;

  btn.addEventListener("click", function () {
    nav.classList.toggle("open");
    var isOpen = nav.classList.contains("open");
    btn.setAttribute("aria-expanded", String(isOpen));
  });

  document.addEventListener("click", function (e) {
    if (!nav.contains(e.target) && !btn.contains(e.target)) {
      nav.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    }
  });
});