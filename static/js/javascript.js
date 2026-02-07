document.addEventListener("DOMContentLoaded", () => {
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
});