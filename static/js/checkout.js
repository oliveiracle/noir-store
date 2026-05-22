// Handles the Stripe card element and payment confirmation on the checkout page

(function () {
    const form = document.getElementById('payment-form');
    if (!form) return;

    const stripePublicKey = form.dataset.stripeKey;
    const clientSecret    = form.dataset.clientSecret;

    const stripe   = Stripe(stripePublicKey);
    const elements = stripe.elements();

    const style = {
        base: {
            color: '#f0ede8',
            fontFamily: 'Montserrat, sans-serif',
            fontSize: '14px',
            letterSpacing: '0.05em',
            '::placeholder': { color: 'rgba(240,237,232,0.35)' },
        },
        invalid: { color: '#c0392b' },
    };

    const card = elements.create('card', { style: style });
    card.mount('#card-element');

    card.addEventListener('change', function (e) {
        document.getElementById('card-errors').textContent = e.error ? e.error.message : '';
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        document.getElementById('submit-btn').disabled = true;

        stripe.confirmCardPayment(clientSecret, {
            payment_method: { card: card },
        }).then(function (result) {
            if (result.error) {
                document.getElementById('card-errors').textContent = result.error.message;
                document.getElementById('submit-btn').disabled = false;
            } else {
                form.submit();
            }
        });
    });
}());
