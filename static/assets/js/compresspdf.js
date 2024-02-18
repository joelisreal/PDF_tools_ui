function compressFunctionality(objectUrls) {
    var compressBtn = document.createElement('a');
    compressBtn.setAttribute('id', 'compress-pdf');
    compressBtn.setAttribute('href', 'javascript:;');

    var content = document.getElementById('dropArea');
    content.appendChild(compressBtn);
    
    var spanTxt = document.createElement('span');
    // spanTxt.setAttribute(createTextNode('Compress PDF')); 
    spanTxt.appendChild(document.createTextNode('Compress PDF'));
    compressBtn.appendChild(spanTxt);

    compressBtnStatus = true;

    document.getElementById('compress-pdf').addEventListener('click', function() {
        callCompressPdf(objectUrls);
    });
}

function callCompressPdf(objectUrls) {
    // Send a GET request to the /compress endpoint when button clicked
    // $.get('/compress', function (data) {
    //     // alert(data);
    // });
    window.location.href = '/compress';
}
