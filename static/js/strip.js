(function () {
    if (window.innerWidth < 768) return;

    var section = document.getElementById('stripSection');
    var track   = document.getElementById('stripTrack');
    if (!section || !track) return;

    var current = 0;
    var target  = 0;
    var ease    = 0.03;
    var raf;

    function tick() {
        current += (target - current) * ease;
        track.style.transform = 'translateX(-' + current + 'px)';
        raf = requestAnimationFrame(tick);
    }

    section.addEventListener('mousemove', function (e) {
        var rect = section.getBoundingClientRect();
        var x    = (e.clientX - rect.left) / rect.width;
        var maxT = track.scrollWidth - rect.width;
        if (maxT <= 0) return;
        target = x * maxT;
        if (!raf) raf = requestAnimationFrame(tick);
    });

    section.addEventListener('mouseleave', function () {
        target = 0;
    });
}());
