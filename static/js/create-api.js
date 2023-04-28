const container = document.getElementById('jsoneditor');
const options = {
    mode: 'code', 
    indentation: 2, 
    search: false, 
    mainMenuBar: false,
    navigationBar: false, 
    statusBar: false, 
    enableSort: false, 
    enableTransform: false, 
    enableClipboard: false,
    ajv: null, 
    schema: null 
}
const editor = new JSONEditor(container, options);

editor.set();

// Endpoints 
const endpointsContainer = document.getElementById('e_body');
const eRequestType = document.getElementById("endpoint_request_type");
const eUrl = document.getElementById("endpoint_url");
const eDesc = document.getElementById("endpoint_desc");
const eDescView = document.getElementById('e_desc_view');
const eTestDataView = document.getElementById('e_test_data_view');
const errorMessage = document.querySelector('small.error');

let EDIT_VIEW = false;
let EDITING_INDEX = null;

const endpoints = [];

resetDescViewFields()
resetModalFields();

function renderEndpoints() {
    while (endpointsContainer.firstChild) {
        endpointsContainer.removeChild(endpointsContainer.firstChild);
    }

    endpoints.forEach((endpoint, idx) => addEndpointToDom(createEndpointElement(endpoint, idx)));
}

function createEndpoint() {
    if (EDIT_VIEW) {
        updateEndpoint(EDITING_INDEX);
        EDITING_INDEX = null;
        EDIT_VIEW= false;
        return;
    }

    if (!eUrl.value || !eDesc.value) {
        errorMessage.style.display = 'block';
        return;
    }

    errorMessage.style.display = 'none';

    const newEndpoint = {
        method: eRequestType.value,
        url: eUrl.value,
        description: eDesc.value,
    }

    try {
        newEndpoint.testData = editor.get(); 
        newEndpoint.testDataJSON = editor.getText(); 
        console.log(editor.getText())
    } catch {
        newEndpoint.testData = null;
        newEndpoint.testDataJSON = ''; 
    }

    endpoints.push(newEndpoint);
    resetModalFields();
    renderEndpoints();

    $('#e_modal').modal('hide')
}

function addEndpointToDom(endpointEl) {
    endpointsContainer.innerHTML+=endpointEl;
}

function createEndpointElement(endpoint, idx) {
    const {method, url, description, testDataJSON} = endpoint;
    return `
        <tr data-index="${idx}" class="endpoint-item ${method}">
            <td onclick="showEndpointInfo(${idx})">
                <span class="badge badge-primary ${method}">${method}</span>
                ${url}
                <input type="text" name="endpoint_request_type" value="${method}" hidden>
                <input type="text" name="endpoint_url" value="${url}" hidden>
                <textarea hidden name='enpoint_desc'>${description}</textarea>
                <textarea hidden name='enpoint_test'>${testDataJSON}</textarea>
            </td>
            <td style="text-align:end; padding-top:15px;">
                <span><i class="fa fa-solid fa-trash" onclick='deleteEndpoint(${idx})'></i></span>
                <button class="btn-edit" data-toggle="modal" data-target=".bd-example-modal-lg" onclick='openModal(${idx})'>
                    <span><i class="fa fa-solid fa-pencil"></i></span>
                </button>
            </td>
        </tr>
    `
}

function openModal(idx) {
    const {method, url, description, testData} = endpoints[idx];

    EDIT_VIEW = true;
    EDITING_INDEX = idx;

    eRequestType.value = method;
    eUrl.value = url;
    eDesc.value = description;

    if (testData) {
        editor.set(testData);
        return;
    }
    editor.set();
}

function updateEndpoint(idx) {
    if (!eUrl.value || !eDesc.value) {
        errorMessage.style.display = 'block';
        return;
    }
    errorMessage.style.display = 'none';

    const updatedEndpoint = {
        method: eRequestType.value,
        url: eUrl.value,
        description: eDesc.value
    }

    try {
        updatedEndpoint.testData = editor.get(); 
        newEndpoint.testDataJSON = editor.getText(); 
    } catch {
        updatedEndpoint.testData = null;
        newEndpoint.testDataJSON = ''; 
    }

    endpoints[idx] = updatedEndpoint;
    renderEndpoints();
    resetModalFields();
    resetDescViewFields();
    
    $('#e_modal').modal('hide');
}

function resetModalFields() {
    eUrl.value = '';
    eDesc.value = '';
    editor.set();
}

function resetDescViewFields() {
    eDescView.value = '';
    eTestDataView.value = '';
}

function showEndpointInfo(idx) {
    eDescView.value = endpoints[idx].description;
    if (endpoints[idx].testData) {
        eTestDataView.value = JSON.stringify(endpoints[idx].testData, null, 2);
        return;
    }

    eTestDataView.value = '';
}

function deleteEndpoint(idx) {
    endpoints.splice(idx, 1);
    resetDescViewFields();
    renderEndpoints();
}