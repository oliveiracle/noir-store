// Horizontal drag-to-scroll strip with gravity parallax on images

(function () {
    const section = document.getElementById('stripSection');
    if (!section) return;

    // Drag-to-scroll
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

    // Gravity parallax — images repel from mouse, like DARK MATTER letters
    const items = section.querySelectorAll('.strip-item');

    items.forEach(function (item) {
        const img = item.querySelector('.strip-img');
        if (!img) return;

        item.addEventListener('mousemove', function (e) {
            if (isDragging) return;
            const rect    = item.getBoundingClientRect();
            const cx      = rect.left + rect.width  / 2;
            const cy      = rect.top  + rect.height / 2;
            const dx      = e.clientX - cx;
            const dy      = e.clientY - cy;
            const dist    = Math.sqrt(dx * dx + dy * dy);
            const influence = Math.max(rect.width, rect.height) * 0.75;

            if (dist < influence && dist > 0) {
                const force = Math.pow((influence - dist) / influence, 2) * 18;
                const tx = -(dx / dist) * force;
                const ty = -(dy / dist) * force;
                img.style.transform  = 'scale(1.08) translate(' + tx + 'px,' + ty + 'px)';
                img.style.transition = 'transform 0.1s ease-out';
            }
        });

        item.addEventListener('mouseleave', function () {
            img.style.transform  = 'scale(1) translate(0,0)';
            img.style.transition = 'transform 0.6s cubic-bezier(.25,.46,.45,.94)';
        });
    });

    // Touch support
    let touchStartX     = 0;
    let touchScrollLeft = 0;

    section.addEventListener('touchstart', function (e) {
        touchStartX     = e.touches[0].pageX;
        touchScrollLeft = section.scrollLeft;
    }, { passive: true });

    section.addEventListener('touchmove', function (e) {
        const walk = (touchStartX - e.touches[0].pageX) * 1.5;
        section.scrollLeft = touchScrollLeft + walk;
    }, { passive: true });
}());
