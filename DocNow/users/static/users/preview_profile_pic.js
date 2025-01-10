
        const photoInput = document.querySelector('input[type="file"]');
        const photoPreview = document.getElementById('photoPreview');

        photoInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    photoPreview.src = e.target.result;
                    photoPreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                photoPreview.style.display = 'none';
            }
        });
