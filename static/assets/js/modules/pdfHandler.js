import { WORKER_URL } from './constants.js';

export class PDFHandler {
    static async fileHandler(file) {
        const objectUrl = URL.createObjectURL(file);
        this.hideInitialElements();
        this.setupPDFDisplay();

        try {
            pdfjsLib.GlobalWorkerOptions.workerSrc = WORKER_URL;
            const pdfDoc = await pdfjsLib.getDocument(objectUrl).promise;
            await this.renderFirstPage(pdfDoc);
        } catch (err) {
            console.error('Error loading PDF document:', err);
        }
    }

    static hideInitialElements() {
        document.getElementById('pickfiles').style.display = 'none';
        document.querySelector('.upload-droptxt').style.display = 'none';
        document.querySelector('.tool-header').style.display = 'none';
    }

    static setupPDFDisplay() {
        const content = document.getElementById('dropArea');
        content.classList.add('file-selected');
    }

    static async renderFirstPage(pdfDoc) {
        const uploadDiv = document.getElementById('upload');
        uploadDiv.classList.add('file-selected');

        const page = await pdfDoc.getPage(1);
        const viewport = page.getViewport({ scale: 1.5 });

        const pageDiv = this.createPageDiv(1);
        const canvas = this.createCanvas(viewport);
        pageDiv.appendChild(canvas);
        
        this.addCloseButton(pageDiv);
        uploadDiv.appendChild(pageDiv);

        await page.render({
            canvasContext: canvas.getContext('2d'),
            viewport: viewport
        }).promise;
    }

    static createPageDiv(pageNumber) {
        const pageDiv = document.createElement('div');
        pageDiv.classList.add('pdf-page', 'file-selected');
        pageDiv.setAttribute('data-page-number', pageNumber);
        if (pageNumber === 1) pageDiv.classList.add('active');
        return pageDiv;
    }

    static createCanvas(viewport) {
        const canvas = document.createElement('canvas');
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        return canvas;
    }

    static addCloseButton(pageDiv) {
        const span = document.createElement('span');
        span.setAttribute('id', 'closeButton');
        span.classList.add('exit-button');
        span.appendChild(document.createTextNode('X'));
        span.addEventListener('click', () => pageDiv.remove());
        pageDiv.appendChild(span);
    }
}