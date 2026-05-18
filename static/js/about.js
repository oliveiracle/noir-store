(function () {
    /* Only run typewriter on desktop */
    if (window.innerWidth < 992) return;

    var stage = document.querySelector('.about-stage');
    var textEl = document.getElementById('aboutText');
    var labelEl = document.getElementById('aboutChapterLabel');
    var dots = document.querySelectorAll('.about-dot');
    var soundBtn = document.getElementById('aboutSoundBtn');

    if (!stage) return;

    /* ── Keyboard sound ── */
    var soundOn = false;
    var clickSound = new Audio('/static/sounds/virtualzero-mechanical-keyboard-typing-hd-372290.mp3');
    clickSound.volume = 0.5;

    function playClick() {
        if (!soundOn) return;
        var s = clickSound.cloneNode();
        s.currentTime = Math.random() * 3;
        s.volume = 0.5;
        s.play().catch(function () {});
        setTimeout(function () { s.pause(); }, 120);
    }

    /* ── Sound toggle button ── */
    if (soundBtn) {
        soundBtn.addEventListener('click', function () {
            soundOn = !soundOn;
            soundBtn.setAttribute('aria-pressed', soundOn);
            soundBtn.querySelector('.sound-label').textContent = soundOn ? 'SOUND ON' : 'SOUND OFF';
            soundBtn.querySelector('i').className = soundOn ? 'fas fa-volume-up' : 'fas fa-volume-mute';
        });
    }

    /* ── Chapters ── */
    var chapters = [
        {
            label: 'I — The Origin',
            text: 'NOIR was born in 2019 in a small studio in Paris. No investors. No mood boards. Just two people who believed that modern menswear had lost its way — drowning in logos, noise and excess.',
        },
        {
            label: 'II — The Vision',
            text: 'We set one rule: if it doesn\'t need to be there, it isn\'t. Every seam, every cut, every fabric choice is a decision made in silence. We don\'t follow trends. We follow conviction.',
        },
        {
            label: 'III — The Product',
            text: 'Each NOIR piece is constructed to last a decade, not a season. We source from mills in Portugal and Japan. We produce in small runs. We never restock what sells out.',
        },
        {
            label: 'IV — The Future',
            text: 'NOIR will never be a big brand. That\'s the point. We exist for the few who understand that the most powerful thing a man can wear is restraint.',
        },
    ];

    var currentChapter = 0;
    var currentChar = 0;
    var typing = true;
    var paused = false;
    var SPEED = 38;
    var PAUSE_AFTER = 2200;
    var ERASE_SPEED = 18;

    function updateDots() {
        dots.forEach(function (d, i) {
            d.classList.toggle('active', i === currentChapter);
        });
    }

    function typeNext() {
        if (paused) return;
        var chapter = chapters[currentChapter];

        if (typing) {
            if (currentChar <= chapter.text.length) {
                textEl.textContent = chapter.text.slice(0, currentChar);
                if (currentChar > 0) playClick();
                currentChar++;
                setTimeout(typeNext, SPEED);
            } else {
                paused = true;
                setTimeout(function () {
                    paused = false;
                    typing = false;
                    typeNext();
                }, PAUSE_AFTER);
            }
        } else {
            if (currentChar > 0) {
                currentChar--;
                textEl.textContent = chapter.text.slice(0, currentChar);
                setTimeout(typeNext, ERASE_SPEED);
            } else {
                currentChapter = (currentChapter + 1) % chapters.length;
                labelEl.textContent = chapters[currentChapter].label;
                updateDots();
                typing = true;
                setTimeout(typeNext, 400);
            }
        }
    }

    /* Initialise */
    labelEl.textContent = chapters[0].label;
    updateDots();
    setTimeout(typeNext, 800);

    /* Dot navigation */
    dots.forEach(function (dot) {
        dot.addEventListener('click', function () {
            var target = parseInt(dot.dataset.chapter, 10);
            if (target === currentChapter) return;
            currentChapter = target;
            currentChar = 0;
            typing = true;
            paused = false;
            textEl.textContent = '';
            labelEl.textContent = chapters[currentChapter].label;
            updateDots();
            typeNext();
        });
    });
}());
