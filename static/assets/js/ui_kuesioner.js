function showToast(icon, message) {

    Swal.fire({
        toast: true,
        position: 'top-end',

        icon: icon,
        title: message,

        showConfirmButton: false,

        timer: 3000,
        timerProgressBar: true,

        didOpen: (toast) => {

            toast.addEventListener(
                'mouseenter',
                Swal.stopTimer
            );

            toast.addEventListener(
                'mouseleave',
                Swal.resumeTimer
            );
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

    captureBtn.disabled = true;
    captureBtn.innerHTML =
        'Memproses...';

    fetch(
        '/capture/',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image: imageData,
                question_id: questionId
            })
        }
    ).then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.success) {
                captureBtn.innerHTML =
                    '✓ Berhasil';
                if (data.next_question) {
                    window.location.href =
                        '/kuesioner/' +
                        data.next_question +
                        '/';
                } else {
                    window.location.href =
                        '/dashboard-user/';
                }
            } else {
                captureBtn.disabled = false;
                captureBtn.innerHTML =
                    'Capture Ekspresi';
                showToast(
                    'eror',
                    data.message
                );
            }
        })

        .catch(error => {
            captureBtn.disabled = false;
            captureBtn.innerHTML =
                'Capture Ekspresi';
            showToast('eror', 'Terjadi Kesalahan');
            console.error(error);
        });
}
captureBtn.innerHTML =
    '<span class="spinner"></span> Memproses...';