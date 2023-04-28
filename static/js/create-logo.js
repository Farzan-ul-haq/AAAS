    // logic related to publish section
    const fileUploadButton = document.querySelector('.btn-upload-file');
    const fileUploadInput = document.querySelector('#downloadable_file');
    const progressBar = document.querySelector('.progress-bar');
    const filename = document.querySelector('.filename');

    fileUploadButton.addEventListener('click', handleFileSelect);
    fileUploadInput.addEventListener('change', handleFileUpload);

    function handleFileSelect(event) {
        event.preventDefault();
        fileUploadInput.click();
    }

    function handleFileUpload(event) {        
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onloadstart = () => {
            progressBar.style.display = 'block';
            fileUploadButton.style.display = 'none';
        };

        reader.onprogress = (progressEvent) => {
            if (progressEvent.lengthComputable) {
                const progress = (progressEvent.loaded / progressEvent.total) * 100;
                progressBar.style.width = progress + '%';
            }
        };

        reader.onload = () => {
            progressBar.style.width = '100%';
            progressBar.style.display = 'none';
            fileUploadButton.style.display = 'block';
            filename.textContent = file.name;
        };

        reader.readAsDataURL(file);
    }