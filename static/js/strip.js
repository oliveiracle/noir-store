// Horizontal drag-to-scroll strip on the homepage

(function () {
    const section = document.getElementById('stripSection');
    if (!section) return;

    let isDragging  = false;
    let startX      = 0;
    let scrollStart = 0;

    section.addEventListener('mousedown', function (e) {
        isDragging  = true;
        startX      = e.pageX;
        scrollStart = section.scrollLeft;
        section.style.cursor = 'grabbing';
    });

    document.addEventListener('mouseup', function () {
        isDragging = false;
        section.style.cursor = 'grab';
    });

    section.addEventListener('mousemove', function (e) {
        if (!isDragging) return;
        e.preventDefault();
        const walk = (e.pageX - startX) * 1.5;
        section.scrollLeft = scrollStart - walk;
    });

    // Touch support
    let touchStartX     = 0;
    let touchScrollLeft = 0;

    section.addEventListener('touchstart', function (e) {
        touchStartX    = e.touches[0].pageX;
        touchScrollLeft = section.scrollLeft;
    }, { passive: true });

    section.addEventListener('touchmove', function (e) {
        const walk = (touchStartX - e.touches[0].pageX) * 1.5;
        section.scrollLeft = touchScrollLeft + walk;
    }, { passive: true });
}());
