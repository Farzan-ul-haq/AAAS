// Logic related to overall form, steps, progress bar
const mainForm = document.querySelector('#updateForm')
const forms = [...document.querySelectorAll('.form-step-inputs')];
const formSteps = [...document.querySelectorAll('.form-step-item')];
const continuteButtons = [...document.querySelectorAll('.form-btn')].slice(0, 4);

let currentStep = 1;

continuteButtons.forEach((continuteButton) => {
    continuteButton.addEventListener('click', handleFormContinue);
});

formSteps.forEach((formStep) => {
    formStep.addEventListener('click', handleStepSelection);
});

mainForm.addEventListener('submit', handleSubmit);

function handleStepSelection(event) {
    const step = +event.currentTarget.dataset.step;
    
    displayStep(step);
}


function handleFormContinue(event) {
    event.preventDefault();
    const isFormValid = validateStep(currentStep - 1);

    if (!isFormValid) {
        alert('Please fill all the fields');
        return;
    }

    currentStep+=1;
    forms[currentStep-1].dataset.triggered = true;

    displayStep(currentStep);
}

function displayStep(step) {
    if (forms[step-1].dataset.triggered !== 'true') return;

    removeAllSteps('completed');
    removeAllSteps('selected');

    currentStep = step;

    formSteps.forEach((formStep) => {
        // Do not update classList if user has not reached to this step yet
        if (+formStep.dataset.step > currentStep) return;

        // Add "selected" class only on the step user has clicked on
        if (+formStep.dataset.step === step) {
            formStep.classList.add('selected');
            return;
        }

        // Add "completed" class to all the other steps
        formStep.classList.add('completed');
    })

    formToDisplay(step);
}

function removeAllSteps(status) {
    formSteps.forEach((formStep) => {
        if (formStep.classList.contains(status)) {
            formStep.classList.remove(status);
        }
    })
}

function formToDisplay(step) {
    hideAllForms();
    forms[step-1].classList.remove('hidden');
}

function hideAllForms() {
    forms.forEach((form) => {
        if (!form.classList.contains('hidden')) {
            form.classList.add('hidden');
        }
    })
}

function validateStep(step) {
    const inputs = [...forms[step].querySelectorAll('input')];
    const textAreas = [...forms[step].querySelectorAll('textarea')];

    for (let input of inputs) {
        if (input.classList.contains('tag-input')) {
            console.log(input.classList.contains('tag-input'))
            if (tags < 3) return false;
            continue;
        }
        if (!input.value) return false;
    }

    for (let textArea of textAreas) {
        if (!textArea.value) return true;
    }

    return true;
}

// Form Submission
function handleSubmit(event) {
    event.preventDefault();

    if (currentStep < 5) return;
    const isFormValid = validateStep(currentStep - 1);

    if (!isFormValid) {
        alert('Please fill all the fields');
        return;
    }

    const _images = images.map((image, idx) => {
        return {
            data: image,
            isPrimary: thumbnails[idx].classList.contains('primary'),
        }
    })

    const _tags = [...tagsContainer.children].splice(0, tags).map((tag) => {
        return [...tag.children][0].innerText;
    });

    const form = event.target;
    const imagesInput = createNewInput('images', JSON.stringify(_images));
    const tagsInput = createNewInput('tags', JSON.stringify(_tags));
    form.appendChild(imagesInput);
    form.appendChild(tagsInput);

    form.submit();
}


function createNewInput(name, value) {
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;

    return input;
}
// Logic related to tags
const tagsContainer = document.querySelector('.tags-container');
const tagInput = document.querySelector('.tag-input');
let tags = 0;

tagInput.value = '';

tagInput.addEventListener('input', updateInputWidth);
tagInput.addEventListener('keydown', addNewTag);
tagsContainer.addEventListener('click', selectTagInput);

// The width of input field will dynamically
// change based on the length of it's value
function updateInputWidth(event) {
    tagInput.style.width = tagInput.value.length * 2 + "vw";
}

function selectTagInput(event) {
    tagInput.select();
}

function addNewTag(event) {
    // If key is other than "Enter" --> Return
    // Enter key code --> 13
    if (event.keyCode !== 13) return;

    // preventing the form to trigerring the "Continue" button
    event.preventDefault();

    // If the input field is empty --> Return
    if (!tagInput.value) return;

    const newTag = createTag(tagInput.value);
    newTag.addEventListener('click', deleteTag);
    tagsContainer.insertBefore(newTag, tagInput);
    tagInput.value = '';
    tags+=1;
}

function createTag(text) {
    const tag = document.createElement('div');
    tag.classList.add('tag');
    tag.innerHTML = `
        <span class="tag-text">${text}</span>
        <span>X</span>
    `;

    return tag;
}

function deleteTag(event) {
    event.currentTarget.remove();
    tags-=1;
}
// Logic relatead to image gallery
const imageInput = document.querySelector('[name="thumbnail-input"]');
const thumbnails = [...document.querySelectorAll('.thumbnail')];
const imageUploadButtons = [...document.querySelectorAll('.thumbnail > .thumbnail-placeholder > button')];
const imageDeleteButtons = [...document.querySelectorAll('.btn-delete-thumbnail')];
const imageEls = [...document.querySelectorAll('.thumbnail-image > img')];
const imageContainers = [...document.querySelectorAll('.thumbnail-image')];
const imageDropZones = [...document.querySelectorAll('.thumbnail-placeholder')]

const images = [];

imageContainers.forEach((imageContainer, idx) => 
    imageContainer.addEventListener('click', setPrimaryImage(idx)))

imageUploadButtons.forEach((btn) =>
    btn.addEventListener('click', handleSelectImage));

imageDeleteButtons.forEach((btn, idx) =>
    btn.addEventListener('click', handleImageDelete(idx)));

imageInput.addEventListener('change', (event) => {
    handleImageUpload(event.target.files[0]);
});

imageDropZones.forEach((imageDropZone) =>
    imageDropZone.addEventListener('drop', (event) => {
        event.preventDefault();
        handleImageUpload(event.dataTransfer.files[0]);
    }));

imageDropZones.forEach((imageDropZone) =>
    imageDropZone.addEventListener('dragover', (event) =>
        event.preventDefault()));

thumbnails.forEach((thumbnail) =>
    thumbnail.addEventListener('drop', (event) =>
        event.preventDefault()));

thumbnails.forEach((thumbnail) =>
    thumbnail.addEventListener('dragover', (event) =>
        event.preventDefault()));

function handleImageDelete(imageIdx) {
    return (event) => {
        event.preventDefault();
        images.splice(imageIdx, 1);
        updatePrimaryImage(imageIdx);
        removeImageSrcs();
        displayImages();
        updateThumbnailStates();
    };
}

function updatePrimaryImage(idx) {
    if (thumbnails[idx].classList.contains('primary')) {
        if (idx > 0) {
            thumbnails[idx].classList.remove('primary');
            thumbnails[idx-1].classList.add('primary');
            return;
        }
        thumbnails[idx].classList.add('primary');
        return;
    }

    const primaryIdx = thumbnails.findIndex((thumbnail) => thumbnail.classList.contains('primary'));

    if (primaryIdx < 1) return;

    thumbnails[primaryIdx].classList.remove('primary');
    thumbnails[primaryIdx-1].classList.add('primary');
}

function setPrimaryImage(idx) {
    return (event) => {
        removeStates('primary', thumbnails);
        thumbnails[idx].classList.add('primary');
    };
}

function handleSelectImage(event) {
    event.preventDefault();
    imageInput.click();
}

function handleImageUpload(file) {
    const reader = new FileReader();
    reader.onload = () => {
        images.push(reader.result);
        updateThumbnailStates();
        displayImages();
    };
    reader.readAsDataURL(file);
}

function displayImages() {
    if (!images.length) return;

    images.forEach((image, idx) => {
        imageEls[idx].src = image;
    })
}

function removeImageSrcs() {
    imageEls.forEach((img) => {
        img.src = '';
    });
}

function updateThumbnailStates() {
    removeStates('active', thumbnails);
    removeStates('uploaded', thumbnails);

    if (!images.length) {
        thumbnails[0].classList.add('active');
        return;
    }

    thumbnails.forEach((thumbnail, idx) => {
        if (idx < images.length) {
            thumbnail.classList.add('uploaded');
            return;
        }
        if (idx === images.length) {
            thumbnail.classList.add('active');
            return;
        }
    })
}

function removeStates(state, elements) {
    elements.forEach((element) => {
        if (element.classList.contains(state)) {
            element.classList.remove(state);
        }
    });
}