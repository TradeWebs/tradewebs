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

/* ── Contact form: submit to the shared TradeWebs forms Worker ─── */
const FORMS_ENDPOINT = 'https://tradewebs-forms.tradewebs.workers.dev/';
const form = document.getElementById('contact-form');
const submitBtn = document.getElementById('contact-submit');
const statusEl = document.getElementById('contact-form-status');

if (form) {
  form.addEventListener('submit', async e => {
    e.preventDefault();
    submitBtn.textContent = 'Sending…';
    submitBtn.disabled = true;
    if (statusEl) statusEl.textContent = '';

    try {
      const res = await fetch(FORMS_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
      });
      if (!res.ok) throw new Error('Request failed');

      form.reset();
      submitBtn.textContent = 'Sent — thank you!';
      if (statusEl) {
        statusEl.textContent = "Thanks — we'll be in touch the same day.";
        statusEl.classList.add('contact-form__status--ok');
      }
    } catch (err) {
      submitBtn.textContent = 'Send — let\'s get started';
      submitBtn.disabled = false;
      if (statusEl) {
        statusEl.textContent = 'Something went wrong — please WhatsApp us instead using the link below.';
        statusEl.classList.add('contact-form__status--error');
      }
    }
  });
}
