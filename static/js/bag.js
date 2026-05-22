// Handles the +/- quantity buttons on the bag page

function changeQty(btn, delta) {
    const input = btn.parentElement.querySelector('.bag-qty-input');
    const val = parseInt(input.value, 10) + delta;

    if (val >= 1 && val <= 10) input.value = val;
}
