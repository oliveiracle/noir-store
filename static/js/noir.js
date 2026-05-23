// Homepage hero — dark starfield with gravitational wave ripples on mouse move

(function () {
    'use strict';

    const canvas = document.getElementById('starfield');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let W = 0, H = 0, animId;
    let mouseX = 0, mouseY = 0;
    let tick = 0;

    function resize() {
        const hero = canvas.parentElement;
        W = canvas.width  = hero.offsetWidth;
        H = canvas.height = hero.offsetHeight;
        mouseX = W / 2;
        mouseY = H / 2;
        buildStars();
    }

    // Three star layers at different depths
    const layers = [
        { stars: [], count: 180, maxR: 0.3,  speed: 0.006, parallax: 0.004 },
        { stars: [], count: 70,  maxR: 0.7,  speed: 0.012, parallax: 0.010 },
        { stars: [], count: 18,  maxR: 1.4,  speed: 0.018, parallax: 0.018 },
    ];

    function buildStars() {
        layers.forEach(function (layer) {
            layer.stars = [];
            for (let i = 0; i < layer.count; i++) {
                layer.stars.push({
                    x: Math.random() * W,
                    y: Math.random() * H,
                    r: Math.random() * layer.maxR + 0.08,
                    baseAlpha: Math.random() * 0.4 + 0.15,
                    phase: Math.random() * Math.PI * 2,
                    speed: Math.random() * 0.008 + 0.002,
                    drift: (Math.random() - 0.5) * layer.speed,
                });
            }
        });
    }

    function drawStars(ox, oy) {
        layers.forEach(function (layer) {
            layer.stars.forEach(function (s) {
                s.phase += s.speed;
                const alpha = Math.max(0, s.baseAlpha + Math.sin(s.phase) * 0.12);
                s.x += s.drift;
                if (s.x < 0) s.x = W;
                if (s.x > W) s.x = 0;

                const px = s.x - ox * W * layer.parallax;
                const py = s.y - oy * H * layer.parallax;

                ctx.beginPath();
                ctx.arc(px, py, s.r, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(240,237,232,' + alpha + ')';
                ctx.fill();
            });
        });
    }

    // Gravitational wave ripples
    const waves = [];

    function spawnWave() {
        waves.push({ x: mouseX, y: mouseY, r: 0, alpha: 0.18 });
    }

    let waveTimer = 0;
    function drawWaves() {
        waveTimer++;
        if (waveTimer % 18 === 0) spawnWave();

        for (let i = waves.length - 1; i >= 0; i--) {
            const w = waves[i];
            w.r     += 2.2;
            w.alpha -= 0.004;
            if (w.alpha <= 0) { waves.splice(i, 1); continue; }

            ctx.beginPath();
            ctx.arc(w.x, w.y, w.r, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(201,169,110,' + w.alpha + ')';
            ctx.lineWidth = 0.6;
            ctx.stroke();
        }
    }

    function loop() {
        tick++;
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, W, H);

        const ox = (mouseX / W) - 0.5;
        const oy = (mouseY / H) - 0.5;

        drawStars(ox, oy);
        drawWaves();

        animId = requestAnimationFrame(loop);
    }

    resize();
    loop();

    window.addEventListener('resize', function () {
        cancelAnimationFrame(animId);
        resize();
        loop();
    });

    document.addEventListener('mousemove', function (e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Letter gravity — letters repel from mouse cursor
    const titleEl = document.getElementById('gravTitle');
    if (!titleEl) return;

    const lines   = titleEl.querySelectorAll('.grav-line');
    const letters = [];

    lines.forEach(function (line) {
        const text = line.textContent;
        line.textContent = '';
        line.style.display = 'block';
        text.split('').forEach(function (char) {
            const span = document.createElement('span');
            span.className   = 'grav-letter';
            span.textContent = char;
            span.setAttribute('aria-hidden', 'true');
            line.appendChild(span);
            letters.push(span);
        });
    });

    const gravStyle = document.createElement('style');
    gravStyle.textContent = '.grav-letter{display:inline-block;will-change:transform} #gravTitle{cursor:default;user-select:none}';
    document.head.appendChild(gravStyle);

    document.addEventListener('mousemove', function (e) {
        letters.forEach(function (letter) {
            const rect = letter.getBoundingClientRect();
            const cx   = rect.left + rect.width  / 2;
            const cy   = rect.top  + rect.height / 2;
            const dx   = e.clientX - cx;
            const dy   = e.clientY - cy;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const influence = 220;

            if (dist < influence && dist > 0) {
                const force = Math.pow((influence - dist) / influence, 2) * 14;
                letter.style.transform  = 'translate(' + (dx / dist * force) + 'px,' + (dy / dist * force) + 'px)';
                letter.style.transition = 'transform 0.1s ease-out';
            } else {
                letter.style.transform  = 'translate(0,0)';
                letter.style.transition = 'transform 0.5s ease-out';
            }
        });
    });

    titleEl.addEventListener('mouseleave', function () {
        letters.forEach(function (l) {
            l.style.transform  = 'translate(0,0)';
            l.style.transition = 'transform 0.7s ease-out';
        });
    });

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        cancelAnimationFrame(animId);
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, W, H);
    }

}());
