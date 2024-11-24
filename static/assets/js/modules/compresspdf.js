import { state } from './state.js';

export function compressFunctionality(objectUrls) {
    var compressBtn = document.createElement('a');
    compressBtn.setAttribute('id', 'compress-pdf');
    compressBtn.setAttribute('href', 'javascript:;');

    var content = document.getElementById('dropArea');
    content.appendChild(compressBtn);
    
    var spanTxt = document.createElement('span');
    spanTxt.appendChild(document.createTextNode('Compress PDF'));
    compressBtn.appendChild(spanTxt);

    state.compressBtnStatus = true;

    document.getElementById('compress-pdf').addEventListener('click', function() {
        callCompressPdf(objectUrls);
    });
}

function callCompressPdf(objectUrls) {
    // Send a GET request to the /compress endpoint when button clicked
    $.get('/compress', function (data) {
        alert("Compressed PDF is ready for download");
        if (data.redirect_to) {
            window.location.href = data.redirect_to;
        }
    });
}
