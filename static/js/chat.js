// NOIR chat widget — a simple keyword-based assistant

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

    function findProducts(msg) {
        const words = msg.toLowerCase().replace(/[?!.,]/g, '').split(' ').filter(function (w) {
            return w.length > 3;
        });
        const matches = products.filter(function (p) {
            const name = p.name.toLowerCase();
            const cat  = p.category.toLowerCase();
            return words.some(function (w) {
                return name.indexOf(w) !== -1 || cat.indexOf(w) !== -1;
            });
        });
        if (!matches.length) return null;
        return matches.map(function (p) {
            return p.name + ' — €' + p.price;
        }).join('\n');
    }

    const rules = [
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

    function reply(msg) {
        const lower = msg.toLowerCase();
        for (let i = 0; i < rules.length; i++) {
            for (let j = 0; j < rules[i].k.length; j++) {
                if (lower.indexOf(rules[i].k[j]) !== -1) return rules[i].r;
            }
        }
        const found = findProducts(msg);
        if (found) return 'Here\'s what we have:\n' + found;
        return "I'm not sure about that. Try asking about a product, shipping, returns or sizing — or visit our FAQ page.";
    }

    function addMsg(text, cls) {
        const d = document.createElement('div');
        d.className = 'chat-msg ' + cls;
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
        const msg = input.value.trim();
        if (!msg) return;
        addMsg(msg, 'chat-msg--user');
        input.value = '';
        setTimeout(function () { addMsg(reply(msg), 'chat-msg--bot'); }, 350);
    });
}());
