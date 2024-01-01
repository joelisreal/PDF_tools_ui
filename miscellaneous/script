/*         const fileInput = document.getElementById('pdf-file-input');
        const canvas = document.getElementById('pdf-canvas');
        const ctx = canvas.getContext('2d');
        let pdfDoc = null;

        fileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            const reader = new FileReader();

            reader.onload = function (event) {
                const typedarray = new Uint8Array(event.target.result);
                displayPdf(typedarray);
            };

            reader.readAsArrayBuffer(file);

            e.preventDefault(); // Prevent default form submission behavior

        });

        async function displayPdf(pdfData) {
            pdfDoc = await pdfjsLib.getDocument({ data: pdfData }).promise;
            renderPdf(1); // Display the first page by default
        }

        async function renderPdf(pageNumber) {
            const page = await pdfDoc.getPage(pageNumber);
            const scale = 1.5;
            const viewport = page.getViewport({ scale });

            canvas.height = viewport.height;
            canvas.width = viewport.width;

            const renderContext = {
                canvasContext: ctx,
                viewport: viewport
            };

            await page.render(renderContext).promise;
        }

        // Your logic for capturing mouse events to select a rectangular area goes here... */

        // Get references to the file input element and the iframe
        // var fileInput = document.getElementById('pdf-file-input');
        // var iframe = document.getElementById('pdf-iframe');

        // // Handle the file upload event
        // fileInput.addEventListener('change', function(e) {
        //     var file = e.target.files[0];
        //     if (file.type == "application/pdf") {
        //         var objectUrl = URL.createObjectURL(file);
        //         iframe.src = objectUrl;
        //     }
        // });
      /*   document.getElementById('uploadForm').addEventListener('submit', function(event) {
            event.preventDefault();
            var fileInput = document.getElementById('pdf-file-input');
            var pdfViewer = document.getElementById('pdf-iframe');
            var file = fileInput.files[0];
            if (file.type == "application/pdf") {
                // var objectUrl = URL.createObjectURL(file);
                //iframe.src = objectUrl; 
                const reader = new FileReader();
                reader.onload = function (event) {
                    pdfViewer.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        }) */