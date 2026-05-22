// NOIR chat widget — a simple keyword-based assistant
// It matches user input against a list of rules and replies accordingly

(function () {
    var widget  = document.getElementById('noir-chat');
    if (!widget) return;

    var toggle  = document.getElementById('chatToggle');
    var closeBtn = document.getElementById('chatClose');
    var box     = document.getElementById('chatBox');
    var form    = document.getElementById('chatForm');
    var input   = document.getElementById('chatInput');
    var msgs    = document.getElementById('chatMessages');

    // Product data is passed from Django as a JSON string in the data attribute
    var products = JSON.parse(widget.dataset.products || '[]');

    // Search for products that match keywords in the user's message
    function findProducts(msg) {
        var words = msg.toLowerCase().replace(/[?!.,]/g, '').split(' ').filter(function (w) {
            return w.length > 3; // Ignore short words like "the", "a", etc.
        });
        var matches = products.filter(function (p) {
            var name = p.name.toLowerCase();
            var cat  = p.category.toLowerCase();
            return words.some(function (w) {
                return name.indexOf(w) !== -1 || cat.indexOf(w) !== -1;
            });
        });
        if (!matches.length) return null;
        return matches.map(function (p) {
            return p.name + ' — €' + p.price;
        }).join('\n');
    }

    // Rules array — each rule has keywords and a reply
    var rules = [
        { k: ['shipping', 'delivery', 'deliver', 'postage'],
          r: 'We offer free shipping on orders over €150. Orders below that have a flat 10% shipping fee. Delivery takes 3–5 business days.' },
        { k: ['return', 'refund', 'exchange'],
          r: 'You can return any item within 30 days of delivery. Items must be unworn and in original packaging. Visit our Returns page for instructions.' },
        { k: ['size', 'sizing', 'fit', 'measurements'],
          r: 'Our pieces run true to size. We recommend going one size up for a relaxed fit. Still unsure? Contact us via our Contact page.' },
        { k: ['payment', 'pay', 'card', 'stripe'],
          r: 'We accept all major credit and debit cards securely via Stripe. Your payment details are never stored.' },
        { k: ['contact', 'email', 'phone', 'reach'],
          r: 'You can reach us via the Contact page. We respond within 24 hours, Monday to Friday.' },
        { k: ['hello', 'hi', 'hey', 'hola', 'oi'],
          r: 'Hello! How can I help you today? Ask me about products, shipping, returns or sizing.' },
        { k: ['thank', 'thanks', 'obrigado'],
          r: "You're welcome. Is there anything else I can help you with?" },
    ];

    // Check the message against each rule and return the first match
    function reply(msg) {
        var lower = msg.toLowerCase();
        for (var i = 0; i < rules.length; i++) {
            for (var j = 0; j < rules[i].k.length; j++) {
                if (lower.indexOf(rules[i].k[j]) !== -1) return rules[i].r;
            }
        }
        // Try to find matching products if no rule matched
        var found = findProducts(msg);
        if (found) return 'Here\'s what we have:\n' + found;
        return "I'm not sure about that. Try asking about a product, shipping, returns or sizing — or visit our FAQ page.";
    }

    // Add a message bubble to the chat window
    function addMsg(text, cls) {
        var d = document.createElement('div');
        d.className = 'chat-msg ' + cls;
        d.textContent = text;
        msgs.appendChild(d);
        // Auto-scroll to the latest message
        msgs.scrollTop = msgs.scrollHeight;
    }

    // Open/close the chat box when clicking the toggle button
    toggle.addEventListener('click', function () {
        box.classList.toggle('chat-box--open');
        if (box.classList.contains('chat-box--open')) input.focus();
    });

    closeBtn.addEventListener('click', function () {
        box.classList.remove('chat-box--open');
    });

    // Handle message submission
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        var msg = input.value.trim();
        if (!msg) return;
        addMsg(msg, 'chat-msg--user');
        input.value = '';
        // Small delay before the bot replies to feel more natural
        setTimeout(function () { addMsg(reply(msg), 'chat-msg--bot'); }, 350);
    });
}());
