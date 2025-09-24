// pROFILE PICTURE UPLOAD FUNCTION
const input = document.getElementById('profile-picture-input');
input.addEventListener('change', () => {
    if (input.files.length > 0) {
        document.getElementById('upload-form').submit();
    }
});


// USHEER PHOTOS 


document.addEventListener('DOMContentLoaded', () => {

    const profileForm = document.getElementById('profile-edit-form');
    if (profileForm) {

        // --- Logic for Live Image Preview ---
        const imageInputs = document.querySelectorAll('.image-upload-input');
        imageInputs.forEach(input => {
            input.addEventListener('change', (event) => {
                const file = event.target.files[0];
                if (!file) return;

                const slot = event.target.closest('.image-upload-slot');
                const preview = slot.querySelector('.image-preview');
                const prompt = slot.querySelector('.upload-prompt');
                const errorDiv = document.getElementById('image-upload-error');

                // Client-Side Validation
                if (!['image/jpeg', 'image/png'].includes(file.type)) {
                    errorDiv.textContent = 'Invalid file type. Please upload a JPG or PNG image.';
                    errorDiv.classList.remove('d-none');
                    event.target.value = ''; // Clear the invalid selection
                    return;
                }
                if (file.size > 5 * 1024 * 1024) { // 5MB
                    errorDiv.textContent = 'File is too large. Maximum size is 5MB.';
                    errorDiv.classList.remove('d-none');
                    event.target.value = ''; // Clear the invalid selection
                    return;
                }
                errorDiv.classList.add('d-none');

                // Show Preview
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    preview.classList.remove('d-none');
                    prompt.classList.add('d-none');
                };
                reader.readAsDataURL(file);
            });
        });
    }
});
