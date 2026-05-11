(function () {
    var wrap = document.getElementById('imgWrap');
    var img  = document.getElementById('detailImg');
    if (!wrap || !img) return;

    wrap.addEventListener('mouseenter', function () {
        img.style.transition = 'transform .3s ease';
        img.style.transform  = 'scale(3)';
    });

    wrap.addEventListener('mousemove', function (e) {
        var r = wrap.getBoundingClientRect();
        var x = ((e.clientX - r.left)  / r.width)  * 100;
        var y = ((e.clientY - r.top)   / r.height) * 100;
        img.style.transition      = 'transform .3s ease';
        img.style.transformOrigin = x + '% ' + y + '%';
    });

    wrap.addEventListener('mouseleave', function () {
        img.style.transition      = 'transform .4s ease, transform-origin 0s';
        img.style.transform       = 'scale(1)';
        img.style.transformOrigin = 'center center';
    });
}());
