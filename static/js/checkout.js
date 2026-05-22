// Handles the Stripe card element and payment confirmation on the checkout page

(function () {
    var form = document.getElementById('payment-form');
    if (!form) return;

    // Get the Stripe public key and client secret from data attributes on the form
    // These are set by Django in the checkout template
    var stripePublicKey = form.dataset.stripeKey;
    var clientSecret    = form.dataset.clientSecret;

    // Initialise Stripe with the public key
    var stripe   = Stripe(stripePublicKey);
    var elements = stripe.elements();

    // Style the card input to match the NOIR colour scheme
    var style = {
        base: {
            color: '#f0ede8',
            fontFamily: 'Montserrat, sans-serif',
            fontSize: '14px',
            letterSpacing: '0.05em',
            '::placeholder': { color: 'rgba(240,237,232,0.35)' },
        },
        invalid: { color: '#c0392b' },
    };

    // Create and mount the Stripe card element into the page
    var card = elements.create('card', { style: style });
    card.mount('#card-element');

    // Show any card validation errors in real time as the user types
    card.addEventListener('change', function (e) {
        document.getElementById('card-errors').textContent = e.error ? e.error.message : '';
    });

    // Handle form submission
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        // Disable the button to prevent double submissions
        document.getElementById('submit-btn').disabled = true;

        // Ask Stripe to confirm the payment using the client secret from the server
        stripe.confirmCardPayment(clientSecret, {
            payment_method: { card: card },
        }).then(function (result) {
            if (result.error) {
                // Show the error and re-enable the button so the user can try again
                document.getElementById('card-errors').textContent = result.error.message;
                document.getElementById('submit-btn').disabled = false;
            } else {
                // Payment succeeded — submit the form to the Django view
                form.submit();
            }
        });
    });
}());
