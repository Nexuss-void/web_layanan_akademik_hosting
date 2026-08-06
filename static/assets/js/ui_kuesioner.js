function showToast(icon, message) {
    Swal.fire({
        icon: icon,
        title: message,
        position: 'center',
        showConfirmButton: false,
        timer: 1500,
        timerProgressBar: true,
        allowOutsideClick: false,
        allowEscapeKey: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
}

// Start camera
(async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        document.getElementById('videoFeed').srcObject = stream;
    } catch (e) {
        document.querySelector('.video-frame').style.background = '#1e293b';
    }
})();

function captureImage() {

    const video =
        document.getElementById('videoFeed');
    const canvas =
        document.getElementById('canvas');
    const previewCanvas =
        document.getElementById('capturedCanvas');
    const captureBtn =
        document.getElementById('captureBtn');

    canvas.width =
        video.videoWidth;
    canvas.height =
        video.videoHeight;
    canvas
        .getContext('2d')
        .drawImage(
            video,
            0,
            0
        );

    previewCanvas.width =
        canvas.width;
    previewCanvas.height =
        canvas.height;
    previewCanvas
        .getContext('2d')
        .drawImage(
            canvas,
            0,
            0
        );

    document
        .getElementById('previewWrap')
        .style.display = 'block';
    const imageData =
        canvas.toDataURL('image/png');
    const questionId =
        document
            .getElementById('question')
            .dataset
            .questionId;
    const pathParts = window.location.pathname.split('/').filter(Boolean);
    const currentStep = parseInt(pathParts[2] || 0, 10);
    const periodId = pathParts[1];
    const csrfToken = getCookie('csrftoken') || (document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '');

    captureBtn.disabled = true;
    captureBtn.innerHTML =
        '<span class="spinner"></span> Memproses...';

    fetch(
        '/capture/',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: imageData,
                question_id: questionId,
                period_id: periodId,
                current_step: currentStep
            })
        }
    ).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP Error Status: ${response.status}`);
        }
        return response.json();
    })
        .then(data => {
            console.log(data);
            if (data.success) {
                captureBtn.innerHTML =
                    '✓ Berhasil';
                if (data.is_completed) {
                    window.location.href =
                        '/dashboard-user/';
                } else {
                    window.location.href =
                        '/kuesioner/' +
                        data.period +
                        '/' +
                        data.next_step +
                        '/';
                }
            } else {
                captureBtn.disabled = false;
                captureBtn.innerHTML =
                    'Capture Gambar';
                showToast(
                    'error',
                    data.message
                );
            }
        })

        .catch(error => {
            captureBtn.disabled = false;
            captureBtn.innerHTML =
                'Capture Gambar';
            showToast('error', 'Terjadi Kesalahan');
            console.error(error);
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}