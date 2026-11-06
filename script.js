const menuBtn = document.getElementById("menuBtn");
const navLinks = document.getElementById("navLinks");
const themeToggle = document.getElementById("themeToggle");

menuBtn.addEventListener("click", () => {
  navLinks.classList.toggle("open");
});

document.querySelectorAll(".nav-links a").forEach((link) => {
  link.addEventListener("click", () => navLinks.classList.remove("open"));
});

function setTheme(isDark) {
  document.body.classList.toggle("dark-mode", isDark);
  themeToggle.textContent = isDark ? "☀️ Light Mode" : "🌙 Dark Mode";
  themeToggle.setAttribute(
    "aria-label",
    isDark ? "Switch to light mode" : "Switch to dark mode"
  );
  try {
    localStorage.setItem("portfolio-theme", isDark ? "dark" : "light");
  } catch (error) {
    // The theme still works if browser storage is unavailable.
  }
}

let savedTheme = "light";
try {
  savedTheme = localStorage.getItem("portfolio-theme") || "light";
} catch (error) {
  // Use light mode by default if browser storage is unavailable.
}
setTheme(savedTheme === "dark");

themeToggle.addEventListener("click", () => {
  setTheme(!document.body.classList.contains("dark-mode"));
});

document.getElementById("year").textContent = new Date().getFullYear();


// Decorative motion: reveal sections/cards as they enter the viewport.
document.addEventListener("DOMContentLoaded", () => {
  const revealTargets = document.querySelectorAll(
    ".section-title, .section-text, .skill, .project-card, .education-card, .contact-details"
  );
  revealTargets.forEach((element) => element.classList.add("reveal-on-scroll"));

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          currentObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealTargets.forEach((element) => observer.observe(element));
  } else {
    revealTargets.forEach((element) => element.classList.add("is-visible"));
  }
});

const scrollProgress = document.getElementById("scrollProgress");
function updateScrollProgress() {
  if (!scrollProgress) return;
  const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollableHeight > 0 ? (window.scrollY / scrollableHeight) * 100 : 0;
  scrollProgress.style.width = `${Math.min(100, Math.max(0, progress))}%`;
}
window.addEventListener("scroll", updateScrollProgress, { passive: true });
window.addEventListener("resize", updateScrollProgress);
updateScrollProgress();



// Extra scroll reveals and gentle card tilt.
document.addEventListener("DOMContentLoaded", () => {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reducedMotion) return;

  const revealTargets = document.querySelectorAll(
    "section h2, section p, .card, .skill-card, .project-card, .certificate-card, .education-card, .contact-form, .home-image"
  );

  revealTargets.forEach((el, index) => {
    if (el.closest(".home-text")) return; // the hero already has entrance animations
    el.classList.add("reveal");
    if (el.matches(".home-image")) el.classList.add("reveal-right");
    el.style.transitionDelay = `${Math.min((index % 5) * 70, 280)}ms`;
  });

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -35px 0px" });

  document.querySelectorAll(".reveal, .reveal-left, .reveal-right").forEach(el => {
    revealObserver.observe(el);
  });

  // Subtle 3D tilt for pointer devices only.
  const tiltCards = document.querySelectorAll(".card, .skill-card, .project-card, .certificate-card, .education-card");
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (finePointer) {
    tiltCards.forEach(card => {
      card.addEventListener("mousemove", event => {
        const rect = card.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width;
        const y = (event.clientY - rect.top) / rect.height;
        const rotateY = (x - 0.5) * 4;
        const rotateX = (0.5 - y) * 4;
        card.style.transform = `translateY(-6px) perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
      });
    });
  }
});


// Profile photo: gentle 3D tilt that follows the mouse (desktop only).
document.addEventListener("DOMContentLoaded", () => {
  const frame = document.getElementById("photoFrame");
  if (!frame) return;
  const ok = window.matchMedia("(hover: hover) and (pointer: fine)").matches &&
             !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!ok) return;
  frame.addEventListener("mousemove", (e) => {
    const r = frame.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    frame.style.setProperty("--ry", `${x * 14}deg`);
    frame.style.setProperty("--rx", `${-y * 14}deg`);
  });
  frame.addEventListener("mouseleave", () => {
    frame.style.setProperty("--rx", "0deg");
    frame.style.setProperty("--ry", "0deg");
  });
});
