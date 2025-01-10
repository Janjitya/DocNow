document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert'); 
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0'; 
            setTimeout(() => {
                alert.style.display = 'none'; 
            }, 500); 
        }, 5000); 
    });
});