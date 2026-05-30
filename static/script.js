document.addEventListener("DOMContentLoaded", function () {
    const bmiFill = document.querySelector(".bmi-progress-fill");

    if (bmiFill) {
        const widthValue = bmiFill.getAttribute("data-width");
        bmiFill.style.width = widthValue + "%";
    }
});