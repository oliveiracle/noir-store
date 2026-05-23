// Homepage hero animations — starfield, nebulae, shooting stars, letter gravity

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
        build();
    }

    // Three star layers with different speeds and sizes to create depth
    const layers = [
        { stars: [], count: 260, maxR: 0.32, speed: 0.007, parallax: 0.006 },
        { stars: [], count: 110, maxR: 0.85, speed: 0.014, parallax: 0.014 },
        { stars: [],  count: 26, maxR: 2.0,  speed: 0.022, parallax: 0.026 },
    ];

    function buildStars() {
        layers.forEach(function (layer) {
            layer.stars = [];
            for (let i = 0; i < layer.count; i++) {
                layer.stars.push({
                    x: Math.random() * W,
                    y: Math.random() * H,
                    r: Math.random() * layer.maxR + 0.08,
                    baseAlpha: Math.random() * 0.55 + 0.2,
                    twinkleSpeed: Math.random() * 0.012 + 0.003,
                    twinklePhase: Math.random() * Math.PI * 2,
                    drift: (Math.random() - 0.5) * layer.speed,
                });
            }
        });
    }

    function drawLayers(ox, oy) {
        layers.forEach(function (layer) {
            layer.stars.forEach(function (s) {
                s.twinklePhase += s.twinkleSpeed;
                const alpha = Math.max(0, s.baseAlpha + Math.sin(s.twinklePhase) * 0.18);
                s.x += s.drift;
                if (s.x < 0) s.x = W;
                if (s.x > W) s.x = 0;

                const px = s.x - ox * W * layer.parallax;
                const py = s.y - oy * H * layer.parallax;

                ctx.beginPath();
                ctx.arc(px, py, s.r, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(240,237,232,' + alpha + ')';
                ctx.fill();

                if (s.r > 1.4) {
                    const spikeLen = s.r * 7;
                    ctx.strokeStyle = 'rgba(240,237,232,' + (alpha * 0.22) + ')';
                    ctx.lineWidth = 0.5;
                    for (let a = 0; a < Math.PI * 2; a += Math.PI / 2) {
                        ctx.beginPath();
                        ctx.moveTo(px + Math.cos(a) * s.r, py + Math.sin(a) * s.r);
                        ctx.lineTo(px + Math.cos(a) * spikeLen, py + Math.sin(a) * spikeLen);
                        ctx.stroke();
                    }
                }
            });
        });
    }

    // Nebulae
    let nebulae = [];
    function buildNebulae() {
        nebulae = [
            { x: W * 0.72, y: H * 0.22, r: W * 0.28, cr: 55,  cg: 35,  cb: 110, a: 0.055 },
            { x: W * 0.18, y: H * 0.55, r: W * 0.22, cr: 20,  cg: 45,  cb: 85,  a: 0.04  },
            { x: W * 0.50, y: H * 0.38, r: W * 0.35, cr: 201, cg: 130, cb: 50,  a: 0.022 },
        ];
    }

    function drawNebulae(ox, oy) {
        nebulae.forEach(function (n) {
            const nx  = n.x + ox * 0.4 * W;
            const ny  = n.y + oy * 0.4 * H;
            const grd = ctx.createRadialGradient(nx, ny, 0, nx, ny, n.r);
            grd.addColorStop(0,    'rgba(' + n.cr + ',' + n.cg + ',' + n.cb + ',' + n.a + ')');
            grd.addColorStop(0.45, 'rgba(' + n.cr + ',' + n.cg + ',' + n.cb + ',' + (n.a * 0.35) + ')');
            grd.addColorStop(1,    'rgba(0,0,0,0)');
            ctx.fillStyle = grd;
            ctx.beginPath();
            ctx.arc(nx, ny, n.r, 0, Math.PI * 2);
            ctx.fill();
        });
    }

    // Shooting stars
    let shooters = [];

    function spawnShooter() {
        shooters.push({
            x: Math.random() * W * 0.75 + W * 0.05,
            y: Math.random() * H * 0.4,
            vx: Math.random() * 5 + 3,
            vy: Math.random() * 2.5 + 1.5,
            len: Math.random() * 90 + 40,
            alpha: 1,
            fade: 0.018 + Math.random() * 0.012,
        });
    }

    setInterval(function () { if (Math.random() > 0.35) spawnShooter(); }, 6000);

    function drawShooters() {
        for (let i = shooters.length - 1; i >= 0; i--) {
            const s = shooters[i];
            s.x += s.vx; s.y += s.vy; s.alpha -= s.fade;
            if (s.alpha <= 0) { shooters.splice(i, 1); continue; }

            const steps = s.len / s.vx;
            const tail  = ctx.createLinearGradient(s.x - s.vx * steps, s.y - s.vy * steps, s.x, s.y);
            tail.addColorStop(0, 'rgba(240,237,232,0)');
            tail.addColorStop(1, 'rgba(240,237,232,' + (s.alpha * 0.7) + ')');
            ctx.strokeStyle = tail;
            ctx.lineWidth = 0.8;
            ctx.beginPath();
            ctx.moveTo(s.x - s.vx * steps, s.y - s.vy * steps);
            ctx.lineTo(s.x, s.y);
            ctx.stroke();
        }
    }

    function loop() {
        tick++;
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, W, H);

        const ox = (mouseX / W) - 0.5;
        const oy = (mouseY / H) - 0.5;

        drawNebulae(ox, oy);
        drawLayers(ox, oy);
        drawShooters();

        animId = requestAnimationFrame(loop);
    }

    function build() {
        buildStars();
        buildNebulae();
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

    // Letter gravity — letters repel from the mouse cursor
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
    gravStyle.textContent = '.grav-letter{display:inline-block;will-change:transform;transition:transform 0.12s cubic-bezier(.25,.46,.45,.94)} #gravTitle{cursor:pointer;user-select:none}';
    document.head.appendChild(gravStyle);

    let isCollapsing = false;

    document.addEventListener('mousemove', function (e) {
        if (isCollapsing) return;
        letters.forEach(function (letter) {
            const rect = letter.getBoundingClientRect();
            const cx   = rect.left + rect.width  / 2;
            const cy   = rect.top  + rect.height / 2;
            const dx   = e.clientX - cx;
            const dy   = e.clientY - cy;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const influence = 260;

            if (dist < influence && dist > 0) {
                const force = Math.pow((influence - dist) / influence, 2) * 16;
                letter.style.transform  = 'translate(' + (dx / dist * force) + 'px,' + (dy / dist * force) + 'px)';
                letter.style.transition = 'transform 0.1s ease-out';
            } else {
                letter.style.transform  = 'translate(0,0)';
                letter.style.transition = 'transform 0.5s ease-out';
            }
        });
    });

    titleEl.addEventListener('mouseleave', function () {
        if (isCollapsing) return;
        letters.forEach(function (l) {
            l.style.transform  = 'translate(0,0)';
            l.style.transition = 'transform 0.7s ease-out';
        });
    });

    // Click DARK MATTER to collapse and expand the letters
    titleEl.addEventListener('click', function () {
        if (isCollapsing) return;
        isCollapsing = true;

        letters.forEach(function (letter) {
            setTimeout(function () {
                letter.style.transition = 'transform 280ms cubic-bezier(.55,0,1,.45),opacity 230ms ease';
                letter.style.transform  = 'scale(0)';
                letter.style.opacity    = '0';
            }, Math.random() * 110);
        });

        setTimeout(function () {
            const pt = document.createElement('div');
            pt.style.cssText = 'position:fixed;top:50%;left:50%;width:3px;height:3px;background:#f0ede8;border-radius:50%;transform:translate(-50%,-50%) scale(1);transition:transform .38s,opacity .38s;z-index:9999;pointer-events:none;box-shadow:0 0 18px 6px rgba(201,169,110,.7)';
            document.body.appendChild(pt);
            requestAnimationFrame(function () { requestAnimationFrame(function () {
                pt.style.transform = 'translate(-50%,-50%) scale(90)';
                pt.style.opacity   = '0';
            }); });
            setTimeout(function () { pt.remove(); }, 420);
        }, 300);

        setTimeout(function () {
            letters.forEach(function (letter, i) {
                setTimeout(function () {
                    letter.style.transition = 'transform .14s ease-out,opacity .14s ease';
                    letter.style.transform  = 'scale(1.25)';
                    letter.style.opacity    = '1';
                    setTimeout(function () {
                        letter.style.transition = 'transform .45s cubic-bezier(.175,.885,.32,1.275)';
                        letter.style.transform  = 'scale(1)';
                    }, 140);
                }, i * 30);
            });
            setTimeout(function () { isCollapsing = false; }, letters.length * 30 + 400);
        }, 660);
    });

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        cancelAnimationFrame(animId);
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, W, H);
    }

}());
