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

// logic related to publish section
const trailFileUploadButton = document.querySelector('.btn-upload-trail-file');
const trailFileUploadInput = document.querySelector('#trail_version');
const trailProgressBar = document.querySelector('.progress-bar2');
const trailFilename = document.querySelector('.trail-filename');

trailFileUploadButton.addEventListener('click', handleTrailFileSelect);
trailFileUploadInput.addEventListener('change', handleTrailFileUpload);

function handleTrailFileSelect(event) {
    event.preventDefault();
    trailFileUploadInput.click();
}

function handleTrailFileUpload(event) {        
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onloadstart = () => {
        trailProgressBar.style.display = 'block';
        trailFileUploadButton.style.display = 'none';
    };

    reader.onprogress = (progressEvent) => {
        if (progressEvent.lengthComputable) {
            const progress = (progressEvent.loaded / progressEvent.total) * 100;
            trailProgressBar.style.width = progress + '%';
        }
    };

    reader.onload = () => {
        trailProgressBar.style.width = '100%';
        trailProgressBar.style.display = 'none';
        trailFileUploadButton.style.display = 'block';
        trailFilename.textContent = file.name;
    };

    reader.readAsDataURL(file);
}