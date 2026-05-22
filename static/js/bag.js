// Handles the +/- quantity buttons on the bag page

function changeQty(btn, delta) {
    // Find the number input inside the same row as the clicked button
    var input = btn.parentElement.querySelector('.bag-qty-input');
    var val = parseInt(input.value) + delta;

    // Only update if the value stays between 1 and 10
    if (val >= 1 && val <= 10) input.value = val;
}
