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
    checkoutBtn.addEventListener('click', async () => {
        console.log('Checkout clicked'); 
        
        // Extract the unique listing ID from our HTML data attribute
        const listingId = checkoutBtn.getAttribute('data-listing-id');
        if (!listingId) {
            console.error('Property listing ID is missing.');
            return;
        }

        // Disable button text during transaction processing to prevent duplicate clicks
        checkoutBtn.disabled = true;
        checkoutBtn.innerText = 'Redirecting to checkout...';

        try {
            // Get the CSRF token from the Django cookie so our POST request passes security checks
            const csrfToken = document.cookie
                .split('; ')
                .find(row => row.startsWith('csrftoken='))
                ?.split('=')[1];

            // Request a secure Stripe checkout session from our Django views backend
            const response = await fetch(`/checkout/session/${listingId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            const data = await response.json();

            if (data.error) {
                alert(`Error initializing payment: ${data.error}`);
                checkoutBtn.disabled = false;
                checkoutBtn.innerText = 'Pay Holding Deposit (£250)';
                return;
            }

            // Dynamically load Stripe's client side library and execute redirection
            const stripe = Stripe(data.stripe_public_key);
            await stripe.redirectToCheckout({
                sessionId: data.id
            });

        } catch (error) {
            console.error('Stripe Integration Error:', error);
            alert('Something went wrong communicating with the server.');
            checkoutBtn.disabled = false;
            checkoutBtn.innerText = 'Pay Holding Deposit (£250)';
        }
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