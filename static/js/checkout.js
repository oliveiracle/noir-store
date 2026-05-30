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

        var getVal = function (id) {
            var el = document.getElementById(id);
            return el ? el.value.trim() : '';
        };

        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: getVal('id_full_name'),
                    email: getVal('id_email'),
                    phone: getVal('id_phone_number'),
                    address: {
                        line1: getVal('id_street_address1'),
                        line2: getVal('id_street_address2'),
                        city: getVal('id_town_or_city'),
                        postal_code: getVal('id_postcode'),
                        country: getVal('id_country'),
                        state: getVal('id_county'),
                    },
                },
            },
            shipping: {
                name: getVal('id_full_name'),
                phone: getVal('id_phone_number'),
                address: {
                    line1: getVal('id_street_address1'),
                    line2: getVal('id_street_address2'),
                    city: getVal('id_town_or_city'),
                    postal_code: getVal('id_postcode'),
                    country: getVal('id_country'),
                    state: getVal('id_county'),
                },
            },
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
