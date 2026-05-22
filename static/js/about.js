// Typewriter animation for the About page
// Types each chapter one character at a time, pauses, then erases it

(function () {
    // Only run on desktop — mobile shows a static version instead
    if (window.innerWidth < 992) return;

    var stage    = document.querySelector('.about-stage');
    var textEl   = document.getElementById('aboutText');
    var labelEl  = document.getElementById('aboutChapterLabel');
    var dots     = document.querySelectorAll('.about-dot');
    var soundBtn = document.getElementById('aboutSoundBtn');

    if (!stage) return;

    // Sound setup — cloning the audio node lets us play overlapping clicks
    var soundOn = false;
    var clickSound = new Audio('/static/sounds/virtualzero-mechanical-keyboard-typing-hd-372290.mp3');
    clickSound.volume = 0.5;

    function playClick() {
        if (!soundOn) return;
        var s = clickSound.cloneNode();
        s.currentTime = Math.random() * 3; // Start at a random point in the sound
        s.volume = 0.5;
        s.play().catch(function () {});
        setTimeout(function () { s.pause(); }, 120);
    }

    // Toggle sound on/off and update the button label
    if (soundBtn) {
        soundBtn.addEventListener('click', function () {
            soundOn = !soundOn;
            soundBtn.setAttribute('aria-pressed', soundOn);
            soundBtn.querySelector('.sound-label').textContent = soundOn ? 'SOUND ON' : 'SOUND OFF';
            soundBtn.querySelector('i').className = soundOn ? 'fas fa-volume-up' : 'fas fa-volume-mute';
        });
    }

    // The four brand story chapters
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
    var currentChar    = 0;
    var typing         = true;  // true = typing forward, false = erasing
    var paused         = false;
    var SPEED          = 38;    // ms per character when typing
    var PAUSE_AFTER    = 2200;  // ms to wait before erasing
    var ERASE_SPEED    = 18;    // ms per character when erasing

    // Update which dot is highlighted
    function updateDots() {
        dots.forEach(function (d, i) {
            d.classList.toggle('active', i === currentChapter);
        });
    }

    // Main typewriter loop — called recursively via setTimeout
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
                // Finished typing — pause before erasing
                paused = true;
                setTimeout(function () {
                    paused = false;
                    typing = false;
                    typeNext();
                }, PAUSE_AFTER);
            }
        } else {
            if (currentChar > 0) {
                // Erase one character at a time
                currentChar--;
                textEl.textContent = chapter.text.slice(0, currentChar);
                setTimeout(typeNext, ERASE_SPEED);
            } else {
                // Move to the next chapter and start typing again
                currentChapter = (currentChapter + 1) % chapters.length;
                labelEl.textContent = chapters[currentChapter].label;
                updateDots();
                typing = true;
                setTimeout(typeNext, 400);
            }
        }
    }

    // Initialise the first chapter and start
    labelEl.textContent = chapters[0].label;
    updateDots();
    setTimeout(typeNext, 800);

    // Allow clicking the dots to jump to a specific chapter
    dots.forEach(function (dot) {
        dot.addEventListener('click', function () {
            var target = parseInt(dot.dataset.chapter, 10);
            if (target === currentChapter) return;
            currentChapter = target;
            currentChar    = 0;
            typing         = true;
            paused         = false;
            textEl.textContent  = '';
            labelEl.textContent = chapters[currentChapter].label;
            updateDots();
            typeNext();
        });
    });
}());
