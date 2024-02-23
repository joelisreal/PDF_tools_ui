// List of all object urls
var objectUrls = [];
// Get the drop area
const dropArea = document.getElementById('dropArea');
var compressBtnStatus = false;
// Prevent default behavior to allow drop
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight drop area on drag enter
dropArea.addEventListener('dragenter', () => {
    dropArea.classList.add('highlight');
});

// Remove highlight on drag leave
dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('highlight');
});

var addMoreFilesFunctionalityExecuted = false;
// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false);


function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();

    dropArea.classList.remove('highlight');

    if (!addMoreFilesFunctionalityExecuted) {
        addMoreFilesFunctionality();
        // Need to pass object url to compress call
        const files = e.dataTransfer.files;
        // var objectUrls = [];
        for (const file of files) {
            if (file.type === 'application/pdf') {
                var objectUrl = URL.createObjectURL(file);// + "#view=FitH";
                objectUrls.push(objectUrl);
            }
        }
        compressFunctionality(objectUrls);
        addMoreFilesFunctionalityExecuted = true;
    }

    // Handle dropped files
    const files = e.dataTransfer.files;
    for (const file of files) {
        if (file.type === 'application/pdf') {
            fileHandler(file);
            console.log(file);
            uploadFile(file);
        }
    }

}

// Get the file input element when clicked on if it exits
if (document.getElementById('pickfiles')) {
    var pickFiles = document.getElementById('pickfiles');
    pickFiles.addEventListener('click', function() {
        fileAdderButton(pickFiles);
    });
} else {
    console.log('No file input element with id pickfiles');
}


var addMoreFiles = document.getElementById('add-more-files');
document.getElementById('add-more-files').addEventListener('click', function() {
    fileAdderButton(addMoreFiles);
});

// Function to add a file input element to the page and trigger a click event
function fileAdderButton(filesClick) {
// Create a new file input element
var fileInput = document.createElement('input');
fileInput.type = 'file';
fileInput.multiple = 'multiple'; // Allow selecting multiple files
// fileInput.multiple = true;
// fileInput.setAttribute('multiple');
fileInput.accept = 'application/pdf'; // Allow only PDF files
fileInput.style.display = 'none';

// Add an event listener for when a file is selected
fileInput.addEventListener('change', function(e) {
    // // TODO: Handle the file selection
        if (!addMoreFilesFunctionalityExecuted) {
            addMoreFilesFunctionality();
            // Need to pass object url to compress call
            const files = e.target.files;
            for (const file of files) {
                if (file.type === 'application/pdf') {
                    var objectUrl = URL.createObjectURL(file);// + "#view=FitH";
                    objectUrls.push(objectUrl);
                }
            }
            compressFunctionality(objectUrls);
            addMoreFilesFunctionalityExecuted = true;
        }
    // }
    // Get the selected files
    const files = e.target.files;

    // Handle each selected file
    for (const file of files) {
        if (file.type === 'application/pdf') {
            fileHandler(file);
            uploadFile(file);
        }
    }
});
// Add the file input element to the body
    // This is necessary for the click event to work
    document.body.appendChild(fileInput);

    // Trigger the click event
    fileInput.click();

    // Remove the file input element after the dialog is opened
    // This is necessary to ensure that a new file input element is created each time
    fileInput.parentNode.removeChild(fileInput);
}


    

// functionality for add more files button including hover with tooltip
function addMoreFilesFunctionality() {
    var content = document.getElementById('dropArea');
    var sideTools = document.createElement('div');
    sideTools.classList.add('side-tools');
    content.appendChild(sideTools);

    // var compressPdf = 
    var addMoreFiles = document.getElementById('add-more-files');
    addMoreFiles.style.display = 'block';
    // addMoreFiles.style.border = "dashed blue";
    var spanTxt = document.createElement('span');
    spanTxt.classList.add('tooltip');
    spanTxt.setAttribute('id', 'side-tools-upload-txt');
    spanTxt.appendChild(document.createTextNode('Add more files'));
    // Make sure tooltip is after the button as sibling elements
    sideTools.appendChild(addMoreFiles);
    sideTools.appendChild(spanTxt);

    sideTools.style.border = "dashed green";
}

// Function to handle the dropped PDF file
function fileHandler(file) {
    // TODO: Handle the dropped PDF file
            // For example, display the file in the upload area
            // displayPDF(file);
            var objectUrl = URL.createObjectURL(file);// + "#view=FitH";

                    // Print the object URL to the console
                    console.log(objectUrl);
                    // Hide the button
                    document.getElementById('pickfiles').style.display = 'none';

                    // Hide the drop text
                    document.querySelector('.upload-droptxt').style.display = 'none';

                    toolHeader = document.querySelector('.tool-header');
                    toolHeader.style.display = 'none';

                    // Add class to apply styles when file is selected
                    var content = document.getElementById('dropArea');
                    content.classList.add('file-selected');

                    // Initialize the PDFJS library
                    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.7.570/pdf.worker.min.js';

                    // Load the PDF
                    pdfjsLib.getDocument(objectUrl).promise.then(function(pdfDoc) {

                        // Function to render a specific page
                        function renderPage(pdfDoc) {

                            var uploadDiv = document.getElementById('upload');
                                    uploadDiv.classList.add('file-selected');
                            var drag = false;
                            for (let pageNumber = 1; pageNumber <= 1; pageNumber++) {
                                pdfDoc.getPage(pageNumber).then(function(page) {
                                    var viewport = page.getViewport({ scale: 1.5 });

                    
                                    var pageDiv = document.createElement('div');
                                    pageDiv.classList.add('pdf-page');
                                    pageDiv.setAttribute('data-page-number', pageNumber); // Assign page number to the div
                                    if (pageNumber === 1) {
                                        pageDiv.classList.add('active');
                                    }
                                    pageDiv.classList.add('file-selected');
                                    uploadDiv.appendChild(pageDiv);
                                    

                                    // Create a new canvas for this page
                                    var canvas = document.createElement('canvas');
                                    var context = canvas.getContext('2d');
                                    canvas.height = viewport.height;
                                    canvas.width = viewport.width;
                                    pageDiv.appendChild(canvas);
                                             
                                    var span = document.createElement('span');
                                    span.setAttribute('id', 'closeButton');
                                    span.classList.add('exit-button');
                                    span.appendChild(document.createTextNode('X'));
                                    pageDiv.appendChild(span);
                                    span.addEventListener('click', function() {
                                        pageDiv.remove();
                                    });

                                    // Render the page into the canvas
                                    var renderContext = {
                                        canvasContext: context,
                                        viewport: viewport
                                    };

                                    page.render(renderContext).promise.then(() => {
                                        console.log(`Page ${pageNumber} rendered`);
                                    });


                                });
                            }
                        }
                        renderPage(pdfDoc);
                  

                    }).catch(err => {
                        console.error('Error loading PDF document:', err);
                    });
}
function displayPDF(file) {
    const reader = new FileReader();
    reader.onload = function(event) {
        const uploadDiv = document.getElementById('upload');
        const objectUrl = event.target.result;

        const pdfViewer = document.createElement('iframe');
        pdfViewer.src = objectUrl;
        pdfViewer.width = '100%';
        pdfViewer.height = '500px'; // Adjust as needed
        pdfViewer.style.border = '1px solid black';

        uploadDiv.appendChild(pdfViewer);
    };
    reader.readAsDataURL(file);
}

// File upload logic
function uploadFile(file) {
    console.log(file);
    var formData = new FormData();
    formData.append('file', file);

    $.ajax({
        type: 'POST',
        url: '/upload',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            // alert(data);
        }
    });
}


