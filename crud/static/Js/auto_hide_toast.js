document.addEventListener('DOMContentLoaded', function () {
    const toastContainer = document.getElementById('toast-container');
    if (toastContainer) {
        setTimeout(() => {
            toastContainer.style.display = 'none';
        }, 3000); // Auto-dismiss after 3 seconds
    }
});