// Adds a zoom effect to the product image on the detail page

(function () {
    var wrap = document.getElementById('imgWrap');
    var img  = document.getElementById('detailImg');
    if (!wrap || !img) return;

    // Zoom in when the mouse enters the image area
    wrap.addEventListener('mouseenter', function () {
        img.style.transition = 'transform .3s ease';
        img.style.transform  = 'scale(3)';
    });

    // Move the zoom origin to follow the cursor position
    wrap.addEventListener('mousemove', function (e) {
        var r = wrap.getBoundingClientRect();
        // Calculate where the cursor is as a percentage of the image size
        var x = ((e.clientX - r.left)  / r.width)  * 100;
        var y = ((e.clientY - r.top)   / r.height) * 100;
        img.style.transition      = 'transform .3s ease';
        img.style.transformOrigin = x + '% ' + y + '%';
    });

    // Reset the zoom when the mouse leaves
    wrap.addEventListener('mouseleave', function () {
        img.style.transition      = 'transform .4s ease, transform-origin 0s';
        img.style.transform       = 'scale(1)';
        img.style.transformOrigin = 'center center';
    });
}());
