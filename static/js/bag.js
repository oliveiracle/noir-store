function changeQty(btn, delta) {
    var input = btn.parentElement.querySelector('.bag-qty-input');
    var val = parseInt(input.value) + delta;
    if (val >= 1 && val <= 10) input.value = val;
}
