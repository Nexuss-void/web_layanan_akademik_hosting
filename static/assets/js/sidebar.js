document.addEventListener("DOMContentLoaded", function () {
    const appLayout = document.getElementById("appLayout");
    const hamburgerBtn = document.getElementById("hamburgerBtn");
    const sidebarOverlay = document.getElementById("sidebarOverlay");

    if (window.innerWidth <= 768 && appLayout) {
        appLayout.classList.add("sidebar-collapsed");
    }

    if (hamburgerBtn && appLayout) {
        hamburgerBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            appLayout.classList.toggle("sidebar-collapsed");
        });
    }

    if (sidebarOverlay && appLayout) {
        sidebarOverlay.addEventListener("click", function () {
            appLayout.classList.add("sidebar-collapsed");
        });
    }
});