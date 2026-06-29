const menuToggle = document.getElementById("menuToggle");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");

menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("show");
});

menuToggle.onclick = () => {
    sidebar.classList.toggle("show");
    overlay.classList.toggle("show");
}

overlay.onclick = () => {
    sidebar.classList.remove("show");
    overlay.classList.remove("show");
}