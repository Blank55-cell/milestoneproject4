// quick selector helper
const $ = (selector) => document.querySelector(selector);

// mobile nav toggle
const menuBtn = $('#menu-btn');
const navLinks = $('.nav-links');

if (menuBtn) {
    menuBtn.addEventListener('click', () => {
        navLinks.classList.toggle('open');
    });
}

// checkout button logic
const checkoutBtn = $('#checkout-button');

if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
        console.log('Checkout clicked'); 
        alert('Payment system not connected yet.');
    });
}

// smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
        const target = document.querySelector(link.getAttribute('href'));
        e.preventDefault();

        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});