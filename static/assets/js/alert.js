function showAlert(icon, message) {
    Swal.fire({
        icon: icon,
        title: message,
        showConfirmButton: false,
        timer: 1800,
        timerProgressBar: true,
        allowOutsideClick: false
    });
}