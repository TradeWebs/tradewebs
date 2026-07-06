/* TradeWebs — main.js */

/* ── Nav: scroll state ─────────────────────────────────────── */
const nav = document.getElementById('nav');
const onScroll = () => {
  nav.classList.toggle('scrolled', window.scrollY > 20);
};
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* ── Mobile burger menu ────────────────────────────────────── */
const burger = document.getElementById('burger');
const mobileMenu = document.getElementById('mobile-menu');

burger.addEventListener('click', () => {
  const isOpen = mobileMenu.classList.toggle('open');
  burger.setAttribute('aria-expanded', String(isOpen));
  mobileMenu.setAttribute('aria-hidden', String(!isOpen));
});

// Close on link click
mobileMenu.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    mobileMenu.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
    mobileMenu.setAttribute('aria-hidden', 'true');
  });
});

/* ── Scroll reveal (IntersectionObserver) ──────────────────── */
const revealEls = document.querySelectorAll('.reveal');

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
);

revealEls.forEach(el => revealObserver.observe(el));

/* ── Stagger sibling reveals ────────────────────────────────── */
// Groups: steps, features, examples, pricing cards, faq items
const staggerGroups = [
  '.steps',
  '.features',
  '.examples',
  '.pricing-cards',
  '.faq-list',
];

staggerGroups.forEach(selector => {
  const parent = document.querySelector(selector);
  if (!parent) return;
  const children = parent.querySelectorAll('.reveal');
  children.forEach((child, i) => {
    child.style.transitionDelay = `${i * 0.1}s`;
  });
});

/* ── Smooth anchor scrolling with nav offset ───────────────── */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const navH = nav.getBoundingClientRect().height;
    const top = target.getBoundingClientRect().top + window.scrollY - navH - 16;
    window.scrollTo({ top, behavior: 'smooth' });
  });
});

/* ── Contact form: simple feedback ────────────────────────── */
const form = document.getElementById('contact-form');
const submitBtn = document.getElementById('contact-submit');

if (form) {
  form.addEventListener('submit', e => {
    // Netlify will handle the actual submission.
    // This just gives instant visual feedback.
    submitBtn.textContent = 'Sending…';
    submitBtn.disabled = true;
  });
}
