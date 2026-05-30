// NOIR chat widget

(function () {
    const widget  = document.getElementById('noir-chat');
    if (!widget) return;

    const toggle   = document.getElementById('chatToggle');
    const closeBtn = document.getElementById('chatClose');
    const box      = document.getElementById('chatBox');
    const form     = document.getElementById('chatForm');
    const input    = document.getElementById('chatInput');
    const msgs     = document.getElementById('chatMessages');

    const products = JSON.parse(widget.dataset.products || '[]');

    var greeted = false;

    function normalize(str) {
        return str.toLowerCase().replace(/[^a-z0-9 ]/g, '').trim();
    }

    function containsAny(str, words) {
        return words.some(function (w) { return str.indexOf(w) !== -1; });
    }

    // Search products by matching words in the message against name and category
    function findProducts(msg) {
        var clean = normalize(msg);
        var words = clean.split(' ').filter(function (w) { return w.length > 2; });
        var matches = products.filter(function (p) {
            var name = normalize(p.name);
            var cat  = normalize(p.category);
            return words.some(function (w) {
                return name.indexOf(w) !== -1 || cat.indexOf(w) !== -1;
            });
        });
        return matches;
    }

    function isPriceQuestion(msg) {
        var clean = normalize(msg);
        return containsAny(clean, ['price', 'cost', 'how much', 'costs', 'priced', 'expensive']);
    }

    function isAvailabilityQuestion(msg) {
        var clean = normalize(msg);
        return containsAny(clean, ['available', 'in stock', 'have', 'sell', 'got', 'do you carry']);
    }

    function formatProductList(matches) {
        return matches.map(function (p) {
            return '• ' + p.name + ' — €' + p.price;
        }).join('\n');
    }

    var rules = [
        {
            k: ['shipping', 'delivery', 'deliver', 'postage', 'dispatch'],
            r: 'Shipping is free on orders over €150 — otherwise it\'s a flat 10% of your order total. Should arrive in 3–5 business days.'
        },
        {
            k: ['return', 'refund', 'exchange'],
            r: 'No worries — you have 30 days from delivery to return anything. Just make sure it\'s unworn and in the original packaging. Head to the Returns page and we\'ll sort it out.'
        },
        {
            k: ['size', 'sizing', 'fit', 'measurements', 'small', 'large', 'medium'],
            r: 'Everything runs true to size. If you want a more relaxed, oversized look go one size up. We stock XS through XL on most pieces.'
        },
        {
            k: ['payment', 'pay', 'card', 'stripe', 'checkout'],
            r: 'We take all major cards through Stripe — it\'s fully secure and we never store your card details.'
        },
        {
            k: ['contact', 'email', 'phone', 'reach', 'support', 'help'],
            r: 'Best way to reach us is through the Contact page. We usually reply within 24 hours on weekdays.'
        },
        {
            k: ['order', 'track', 'tracking', 'where is'],
            r: 'You can check your order history in your account. Tracking info should come through in your confirmation email — if not, drop us a message via the Contact page.'
        },
        {
            k: ['wishlist', 'save', 'favourite', 'favorite'],
            r: 'Just hit the wishlist button on any product page and it\'ll be saved to your account. You\'ll need to be signed in for that.'
        },
        {
            k: ['account', 'login', 'sign in', 'register', 'password'],
            r: 'You can sign in or create an account from the icon in the top right. Once you\'re in, your delivery info and order history are all there.'
        },
        {
            k: ['discount', 'promo', 'code', 'sale', 'offer', 'coupon'],
            r: 'We don\'t do discount codes right now. The best deal we offer is free shipping when you spend over €150.'
        },
    ];

    function reply(msg) {
        var clean = normalize(msg);

        // Try product search first — more specific than keyword rules
        var matches = findProducts(msg);

        if (matches.length === 1) {
            var p = matches[0];
            if (isPriceQuestion(msg)) {
                return 'The ' + p.name + ' is €' + p.price + '. You can find it in the shop if you want to take a closer look.';
            }
            if (isAvailabilityQuestion(msg)) {
                return 'Yes, we have the ' + p.name + ' — it\'s €' + p.price + '. Check it out in the shop.';
            }
            return 'Found it — ' + p.name + ' at €' + p.price + '. Head to the shop to see the full details.';
        }

        if (matches.length > 1) {
            if (isPriceQuestion(msg)) {
                return 'Here\'s what we have with prices:\n' + formatProductList(matches);
            }
            return 'A few things came up:\n' + formatProductList(matches);
        }

        // Check topic rules
        for (var i = 0; i < rules.length; i++) {
            if (containsAny(clean, rules[i].k)) {
                return rules[i].r;
            }
        }

        // Greeting — only reply with hello if nothing else matched
        if (containsAny(clean, ['hello', 'hi', 'hey', 'hola', 'oi', 'good morning', 'good afternoon'])) {
            if (!greeted) {
                greeted = true;
                return 'Hey! What can I help you with? Ask me about a product, shipping, sizing or returns.';
            }
            return 'What else can I help you with?';
        }

        if (containsAny(clean, ['thank', 'thanks', 'obrigado', 'cheers'])) {
            return 'Of course! Let me know if there\'s anything else.';
        }

        return 'Not sure I caught that — try asking about a specific product or something like shipping, sizing or returns. I\'ll do my best!';
    }

    function addMsg(text, cls) {
        var d = document.createElement('div');
        d.className = 'chat-msg ' + cls;
        d.style.whiteSpace = 'pre-line';
        d.textContent = text;
        msgs.appendChild(d);
        msgs.scrollTop = msgs.scrollHeight;
    }

    toggle.addEventListener('click', function () {
        box.classList.toggle('chat-box--open');
        if (box.classList.contains('chat-box--open')) input.focus();
    });

    closeBtn.addEventListener('click', function () {
        box.classList.remove('chat-box--open');
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        var msg = input.value.trim();
        if (!msg) return;
        addMsg(msg, 'chat-msg--user');
        input.value = '';
        setTimeout(function () { addMsg(reply(msg), 'chat-msg--bot'); }, 350);
    });
}());
