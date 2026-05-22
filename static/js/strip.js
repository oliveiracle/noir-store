// Horizontal scroll strip on the homepage

(function () {
    if (window.innerWidth < 768) return;

    const section = document.getElementById('stripSection');
    const track   = document.getElementById('stripTrack');
    if (!section || !track) return;

    let current = 0;
    let target  = 0;
    const ease  = 0.03;
    let raf;

    function tick() {
        current += (target - current) * ease;
        track.style.transform = 'translateX(-' + current + 'px)';
        raf = requestAnimationFrame(tick);
    }

    section.addEventListener('mousemove', function (e) {
        const rect = section.getBoundingClientRect();
        const x    = (e.clientX - rect.left) / rect.width;
        const maxT = track.scrollWidth - rect.width;
        if (maxT <= 0) return;
        target = x * maxT;
        if (!raf) raf = requestAnimationFrame(tick);
    });

    section.addEventListener('mouseleave', function () {
        target = 0;
    });
}());
