/* dashboard_admin.js
 * Fungsi: hamburger menu (buka/tutup sidebar) untuk tampilan mobile.
 * Letakkan file ini di: static/assets/js/dashboard_admin.js
 */

(function () {
    'use strict';

    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (!hamburgerBtn || !sidebar || !overlay) return;

    /* ---------- helpers ---------- */
    function openSidebar() {
        sidebar.classList.add('is-open');
        overlay.classList.add('is-visible');
        hamburgerBtn.classList.add('is-open');
        hamburgerBtn.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden'; // cegah scroll halaman
    }

    function closeSidebar() {
        sidebar.classList.remove('is-open');
        overlay.classList.remove('is-visible');
        hamburgerBtn.classList.remove('is-open');
        hamburgerBtn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
    }

    /* ---------- event listeners ---------- */
    hamburgerBtn.addEventListener('click', function () {
        const isOpen = sidebar.classList.contains('is-open');
        isOpen ? closeSidebar() : openSidebar();
    });

    // Tombol X di dalam sidebar
    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }

    // Klik overlay → tutup sidebar
    overlay.addEventListener('click', closeSidebar);

    // Tekan Escape → tutup sidebar
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && sidebar.classList.contains('is-open')) {
            closeSidebar();
        }
    });

    // Jika window di-resize ke desktop → reset state agar tidak stuck
    window.addEventListener('resize', function () {
        if (window.innerWidth > 980) {
            closeSidebar();
        }
    });
})();