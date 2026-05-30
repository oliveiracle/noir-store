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
            r: 'We offer free shipping on orders over €150. Orders below that have a flat 10% shipping fee. Delivery takes 3–5 business days.'
        },
        {
            k: ['return', 'refund', 'exchange'],
            r: 'You can return any item within 30 days of delivery. Items must be unworn and in original packaging. Visit our Returns page for more details.'
        },
        {
            k: ['size', 'sizing', 'fit', 'measurements', 'small', 'large', 'medium'],
            r: 'Our pieces run true to size. We recommend going one size up for a relaxed fit. Check the product page for size options (XS–XL).'
        },
        {
            k: ['payment', 'pay', 'card', 'stripe', 'checkout'],
            r: 'We accept all major credit and debit cards securely via Stripe. Your payment details are never stored on our servers.'
        },
        {
            k: ['contact', 'email', 'phone', 'reach', 'support', 'help'],
            r: 'Reach us via the Contact page. We respond within 24 hours, Monday to Friday.'
        },
        {
            k: ['order', 'track', 'tracking', 'where is my'],
            r: 'You can view your order history in your account profile. For tracking updates, check the confirmation email sent after purchase.'
        },
        {
            k: ['wishlist', 'save', 'favourite', 'favorite'],
            r: 'You can save items to your wishlist by clicking the wishlist button on any product page. You\'ll need to be signed in.'
        },
        {
            k: ['account', 'login', 'sign in', 'register', 'password'],
            r: 'You can create an account or sign in from the top right of the page. Your profile stores your delivery info and order history.'
        },
        {
            k: ['discount', 'promo', 'code', 'sale', 'offer'],
            r: 'We don\'t currently run discount codes. Free shipping is automatically applied to orders over €150.'
        },
    ];

    function reply(msg) {
        var clean = normalize(msg);

        // Try product search first — more specific than keyword rules
        var matches = findProducts(msg);

        if (matches.length === 1) {
            var p = matches[0];
            if (isPriceQuestion(msg)) {
                return 'The ' + p.name + ' is priced at €' + p.price + '.';
            }
            if (isAvailabilityQuestion(msg)) {
                return 'Yes, we carry the ' + p.name + ' — it\'s €' + p.price + '. You can find it in our shop.';
            }
            return 'Here\'s what I found:\n• ' + p.name + ' — €' + p.price + '\nYou can find it in our shop.';
        }

        if (matches.length > 1) {
            if (isPriceQuestion(msg)) {
                return 'Here are the matching products and their prices:\n' + formatProductList(matches);
            }
            return 'I found a few items that match:\n' + formatProductList(matches);
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
                return 'Hello! How can I help you today? You can ask me about products, pricing, shipping, returns or sizing.';
            }
            return 'What can I help you with?';
        }

        if (containsAny(clean, ['thank', 'thanks', 'obrigado', 'cheers'])) {
            return "You\'re welcome. Is there anything else I can help you with?";
        }

        return "I\'m not sure about that. Try asking about a specific product, shipping, returns or sizing — or visit our FAQ page.";
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
