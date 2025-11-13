document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('image');
    const preview = document.getElementById('preview');
    const filenameSpan = document.getElementById('filename');
    const resetBtn = document.getElementById('reset-btn');
    const form = document.getElementById('upload-form');
    const spinner = document.getElementById('loading-spinner');

    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            filenameSpan.textContent = file.name;
            const reader = new FileReader();
            reader.onload = function(event) {
                preview.src = event.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            filenameSpan.textContent = '';
            preview.src = '';
        }
    });

    resetBtn.addEventListener('click', function() {
        form.reset();
        preview.src = '';
        filenameSpan.textContent = '';
        spinner.style.display = 'none';
    });

    form.addEventListener('submit', function() {
        spinner.style.display = 'flex';
    });
});

