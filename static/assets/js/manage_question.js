function openPeriodSelect() {
    const select = document.getElementById('periodSelect');

    select.focus();

    // Untuk browser yang mendukung showPicker()
    if (select.showPicker) {
        select.showPicker();
    }
}

const MASTER = JSON.parse(document.getElementById('all-questions-data').textContent || '[]');
const INITIAL_ACTIVE_IDS = JSON.parse(document.getElementById('active-ids-data').textContent || '[]');

const activeIdsSet = new Set(INITIAL_ACTIVE_IDS);
let bankSoal = MASTER.filter(s => !activeIdsSet.has(s.id));
let activeSoal = MASTER.filter(s => activeIdsSet.has(s.id));
let bankSel = new Set();
let activeSel = new Set();

/* ── RENDER ── */
const CHECKSVG = `<svg width="11" height="11" viewBox="0 0 24 24" fill="none"><path d="M5 13L9 17L19 7" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" /></svg>`;
const EMPTY_BANK = `<div class="empty-state"><svg width="40" height="40" viewBox="0 0 24 24" fill="none"><path d="M4 5.5C4 4.67 4.67 4 5.5 4H18.5C19.33 4 20 4.67 20 5.5V18.5C20 19.33 19.33 20 18.5 20H5.5C4.67 20 4 19.33 4 18.5V5.5Z" stroke="#cbd5e1" stroke-width="1.5" /><path d="M8 9H16M8 13H12" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round" /></svg><p>Bank soal kosong.<br>Semua soal sudah aktif.</p></div>`;
const EMPTY_ACTIVE = `<div class="empty-state"><svg width="40" height="40" viewBox="0 0 24 24" fill="none"><path d="M9 12L11 14L15.5 9.5" stroke="#cbd5e1" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" /><circle cx="12" cy="12" r="9" stroke="#cbd5e1" stroke-width="1.5" /></svg><p>Belum ada soal aktif.<br>Tambahkan dari bank soal.</p></div>`;

function renderList(arr, sel, side, listId, filterVal) {
    const el = document.getElementById(listId);
    const f = filterVal.toLowerCase();
    const filtered = arr.filter(s => {
        const qText = (s.question_text || s.text || '').toLowerCase();
        const qKat = (s.category || s.categ || '').toLowerCase();
        return qText.includes(f) || qKat.includes(f);
    });
    if (!filtered.length) { el.innerHTML = side === 'bank' ? EMPTY_BANK : EMPTY_ACTIVE; return; }
    const isSel = id => sel.has(id);
    el.innerHTML = filtered.map(s => `
    <div class="soal-item${isSel(s.id) ? ' sel' : ''}${side === 'active' ? ' active-side' : ''}"
        onclick="toggle('${side}',${s.id})">
        <div class="s-check">${isSel(s.id) ? CHECKSVG : ''}</div>
        <div class="s-body">
            <div class="s-text">${s.question_text || s.text}</div>
        </div>
        <span class="s-cat">${s.category || s.categ}</span>
    </div>`).join('');
}
function onPeriodChange(id) { window.location.href = `/manage-questions/?id=${id}`; }

function render() {
    const fb = document.getElementById('searchBank').value;
    const fa = document.getElementById('searchActive').value;
    renderList(bankSoal, bankSel, 'bank', 'bankList', fb);
    renderList(activeSoal, activeSel, 'active', 'activeList', fa);
    document.getElementById('bankCount').textContent = `${bankSoal.length} soal`;
    document.getElementById('activeCount').textContent = `${activeSoal.length} soal`;
    document.getElementById('bankSelLabel').textContent = `${bankSel.size} dipilih`;
    document.getElementById('activeSelLabel').textContent = `${activeSel.size} dipilih`;
    document.getElementById('sbActive').textContent = `${activeSoal.length} soal aktif`;
    document.getElementById('sbBank').textContent = `${bankSoal.length} soal di bank`;

    updateSelAllBtn('bank');
    updateSelAllBtn('active');
}

function updateSelAllBtn(side) {
    const btn = document.getElementById(side === 'bank' ? 'selAllBank' : 'selAllActive');
    const sel = side === 'bank' ? bankSel : activeSel;
    const soal = side === 'bank' ? bankSoal : activeSoal;
    if (!btn) return;
    const allSelected = soal.length > 0 && soal.every(s => sel.has(s.id));
    if (allSelected) {
        btn.textContent = 'Batalkan Semua';
        btn.classList.add('is-cancel');
    } else {
        btn.textContent = 'Pilih Semua';
        btn.classList.remove('is-cancel');
    }
}

function toggle(side, id) {
    const sel = side === 'bank' ? bankSel : activeSel;
    sel.has(id) ? sel.delete(id) : sel.add(id);
    render();
}

function toggleSelectAll(side) {
    const btn = document.getElementById(side === 'bank' ? 'selAllBank' : 'selAllActive');
    const sel = side === 'bank' ? bankSel : activeSel;
    const soal = side === 'bank' ? bankSoal : activeSoal;
    const allSelected = soal.length > 0 && soal.every(s => sel.has(s.id));

    if (allSelected) {
        soal.forEach(s => sel.delete(s.id));
    } else {
        soal.forEach(s => sel.add(s.id));
    }
    render();
}

function moveToActive() {
    if (!bankSel.size) return;
    const moving = bankSoal.filter(s => bankSel.has(s.id));
    activeSoal = [...activeSoal, ...moving];
    bankSoal = bankSoal.filter(s => !bankSel.has(s.id));
    bankSel.clear(); render();
}

function moveToBank() {
    if (!activeSel.size) return;
    const moving = activeSoal.filter(s => activeSel.has(s.id));
    bankSoal = [...bankSoal, ...moving];
    activeSoal = activeSoal.filter(s => !activeSel.has(s.id));
    activeSel.clear(); render();
}

function saveSettings() {
    const activeQuestionIds = activeSoal.map(s => s.id);
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfInput ? csrfInput.value : '';

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            questions: activeQuestionIds
        })
    })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json()
        })
        .then(data => {
            if (data.success) {
                showToast('success', `Tersimpan ${activeSoal.length} soal aktif pada periode ini.`);
            } else {
                showToast('error', `Gagal menyimpan: ${data.error || 'Terjadi kesalahan'}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('error', 'Gagal terhubung ke server.');
        });
}

/* ── Search ── */
document.getElementById('searchBank').addEventListener('input', () => render());
document.getElementById('searchActive').addEventListener('input', () => render());

render();