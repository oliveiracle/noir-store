(function () {
    /* Only run typewriter on desktop */
    if (window.innerWidth < 992) return;

    var stage = document.querySelector('.about-stage');
    var textEl = document.getElementById('aboutText');
    var labelEl = document.getElementById('aboutChapterLabel');
    var dots = document.querySelectorAll('.about-dot');
    var soundBtn = document.getElementById('aboutSoundBtn');

    if (!stage) return;

    /* ── Web Audio click synthesiser ── */
    var audioCtx = null;
    var soundOn = false;

    function getAudioCtx() {
        if (!audioCtx) audioCtx = new window.AudioContext();
        return audioCtx;
    }

    function playClick() {
        if (!soundOn) return;
        try {
            var ctx = getAudioCtx();
            var now = ctx.currentTime;
            var sr = ctx.sampleRate;

            /* ── Layer 1: crisp top-end click (key contact) ──
               White noise with fast exponential decay, bandpass around 4kHz */
            var clickLen = Math.floor(sr * 0.014);
            var clickBuf = ctx.createBuffer(1, clickLen, sr);
            var clickData = clickBuf.getChannelData(0);
            for (var i = 0; i < clickLen; i++) {
                clickData[i] = (Math.random() * 2 - 1) * Math.exp(-i / (clickLen * 0.18));
            }
            var clickSrc = ctx.createBufferSource();
            clickSrc.buffer = clickBuf;

            var bp = ctx.createBiquadFilter();
            bp.type = 'bandpass';
            bp.frequency.value = 4200;
            bp.Q.value = 1.4;

            var clickGain = ctx.createGain();
            clickGain.gain.value = 0.55;

            clickSrc.connect(bp);
            bp.connect(clickGain);
            clickGain.connect(ctx.destination);
            clickSrc.start(now);

            /* ── Layer 2: soft body thud (finger + keycap mass) ──
               Low noise burst filtered below 200Hz, very short */
            var thudLen = Math.floor(sr * 0.022);
            var thudBuf = ctx.createBuffer(1, thudLen, sr);
            var thudData = thudBuf.getChannelData(0);
            for (var j = 0; j < thudLen; j++) {
                thudData[j] = (Math.random() * 2 - 1) * Math.exp(-j / (thudLen * 0.25));
            }
            var thudSrc = ctx.createBufferSource();
            thudSrc.buffer = thudBuf;

            var lp = ctx.createBiquadFilter();
            lp.type = 'lowpass';
            lp.frequency.value = 180;

            var thudGain = ctx.createGain();
            thudGain.gain.value = 0.35;

            thudSrc.connect(lp);
            lp.connect(thudGain);
            thudGain.connect(ctx.destination);
            thudSrc.start(now);
        } catch (e) { /* silence any audio errors */ }
    }

    /* ── Sound toggle button ── */
    if (soundBtn) {
        soundBtn.addEventListener('click', function () {
            soundOn = !soundOn;
            soundBtn.setAttribute('aria-pressed', soundOn);
            soundBtn.querySelector('.sound-label').textContent = soundOn ? 'SOUND ON' : 'SOUND OFF';
            soundBtn.querySelector('i').className = soundOn ? 'fas fa-volume-up' : 'fas fa-volume-mute';
            /* Resume AudioContext on first user gesture (browser policy) */
            if (soundOn) getAudioCtx().resume();
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
