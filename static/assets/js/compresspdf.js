// if (compressBtnStatus) {
// document.getElementById('compress-pdf').addEventListener('click', function() {
//     console.log(234);
//     callCompressPdf();
// });
// }

// $(document).ready(function() {
//     $('#compress-pdf').click(function() {
//         $.post('/compress', function(data) {
//             alert(data);  // Display a message or handle the response as needed
//         });
//     });
// });

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
        console.log(234);
        console.log(objectUrls);
        callCompressPdf(objectUrls);
    });
}

function callCompressPdf(objectUrls) {
    // Send a POST request to the /compress endpoint with the objectUrls as data
    // $.post('/compress', { objectUrls: objectUrls }, function(data) {
    //     alert(data);  // Display a message or handle the response as needed
    // });
    // $.get('/compress', function (data) {
    //     // alert(data);
    // });
    window.location.href = '/compress';
    // Send a POST request to the /compress endpoint with the objectUrls as data
    // $.ajax({
    //     type: 'POST',
    //     contentType: 'application/json;charset=UTF-8',
    //     url: '/compress',
    //     data: JSON.stringify({ objectUrls: objectUrls }),
    //     success: function(data) {
    //         alert(data);  // Display a message or handle the response as needed
    //     },
    //     error: function(error) {
    //         console.error('Error:', error);
    //     }
    // });
}

// $(document).ready(function() {
//     $('#compress-pdf').click(function() {
//         $.post('/compress', function(data) {
//             alert(data);  // Display a message or handle the response as needed
//         });
//     });
// });