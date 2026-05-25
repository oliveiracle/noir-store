// Typewriter animation for the About page
// Types each chapter one character at a time, pauses, then erases it

(function () {
    if (window.innerWidth < 992) return;

    const stage    = document.querySelector('.about-stage');
    const textEl   = document.getElementById('aboutText');
    const labelEl  = document.getElementById('aboutChapterLabel');
    const dots     = document.querySelectorAll('.about-dot');

    if (!stage) return;

    const chapters = [
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

    let currentChapter = 0;
    let currentChar    = 0;
    let typing         = true;
    let paused         = false;
    const SPEED        = 38;
    const PAUSE_AFTER  = 2200;
    const ERASE_SPEED  = 18;

    function updateDots() {
        dots.forEach(function (d, i) {
            d.classList.toggle('active', i === currentChapter);
        });
    }

    function typeNext() {
        if (paused) return;
        const chapter = chapters[currentChapter];

        if (typing) {
            if (currentChar <= chapter.text.length) {
                textEl.textContent = chapter.text.slice(0, currentChar);
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

    labelEl.textContent = chapters[0].label;
    updateDots();
    setTimeout(typeNext, 800);

    dots.forEach(function (dot) {
        dot.addEventListener('click', function () {
            const target = parseInt(dot.dataset.chapter, 10);
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
