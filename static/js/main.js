document.addEventListener("DOMContentLoaded", function () {
    // Sticky navbar shadow on scroll
    const navbar = document.querySelector(".navbar-sh");
    const backToTop = document.querySelector(".back-to-top");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 40) {
            navbar && navbar.classList.add("scrolled");
        } else {
            navbar && navbar.classList.remove("scrolled");
        }

        if (backToTop) {
            if (window.scrollY > 400) {
                backToTop.classList.add("show");
            } else {
                backToTop.classList.remove("show");
            }
        }
    });

    // Back to top click
    if (backToTop) {
        backToTop.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // Initialize AOS scroll animations
    if (window.AOS) {
        AOS.init({ duration: 700, once: true, offset: 60 });
    }
});
