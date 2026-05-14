(function () {
    var form = document.getElementById('payment-form');
    if (!form) return;

    var stripePublicKey = form.dataset.stripeKey;
    var clientSecret    = form.dataset.clientSecret;

    var stripe   = Stripe(stripePublicKey);
    var elements = stripe.elements();

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

    var card = elements.create('card', { style: style });
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
