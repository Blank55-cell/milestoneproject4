/*global document, console, fetch, alert, Stripe */

// quick selector helper
const $ = function (selector) {
    "use strict";
    return document.querySelector(selector);
};

// mobile nav toggle
const menuBtn = $("#menu-btn");
const navLinks = $(".nav-links");

if (menuBtn) {
    menuBtn.addEventListener("click", function () {
        "use strict";
        if (navLinks) {
            navLinks.classList.toggle("open");
        }
    });
}

// checkout button logic
const checkoutBtn = $("#checkout-button");

if (checkoutBtn) {
    checkoutBtn.addEventListener("click", function () {
        "use strict";
        console.log("Checkout clicked");

        const listingId = checkoutBtn.getAttribute("data-listing-id");
        if (!listingId) {
            console.error("Property listing ID is missing.");
            return;
        }

        checkoutBtn.disabled = true;
        checkoutBtn.innerText = "Redirecting to checkout...";

        const cookieRow = document.cookie
            .split("; ")
            .find(function (row) {
                return row.startsWith("csrftoken=");
            });

        let csrfToken = "";
        if (cookieRow) {
            csrfToken = cookieRow.split("=")[1];
        }

        fetch("/checkout/session/" + listingId + "/", {
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            method: "POST"
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data.error) {
                    alert("Error initializing payment: " + data.error);
                    checkoutBtn.disabled = false;
                    checkoutBtn.innerText = "Pay Holding Deposit (£250)";
                    return;
                }

                const stripe = new Stripe(data.stripe_public_key);
                stripe.redirectToCheckout({
                    sessionId: data.id
                });
            })
            .catch(function (error) {
                console.error("Stripe Integration Error:", error);
                alert("Something went wrong communicating with the server.");
                checkoutBtn.disabled = false;
                checkoutBtn.innerText = "Pay Holding Deposit (£250)";
            });
    });
}

// smooth scroll for anchor links
document.querySelectorAll("a[href^=\"#\"]").forEach(function (link) {
    "use strict";
    link.addEventListener("click", function (e) {
        const targetAttr = link.getAttribute("href");
        if (targetAttr) {
            const target = document.querySelector(targetAttr);
            e.preventDefault();

            if (target) {
                target.scrollIntoView({
                    behavior: "smooth"
                });
            }
        }
    });
});
