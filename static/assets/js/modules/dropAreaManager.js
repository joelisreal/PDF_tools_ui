// dropAreaManager.js
import { state } from './state.js';
import { UIManager } from './uiManager.js';
import { PDFHandler } from './pdfHandler.js';
import { FileUploader } from './fileUploader.js';

export class DropAreaManager {
    constructor(dropAreaId) {
        this.dropArea = document.getElementById(dropAreaId);
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.dropArea.addEventListener(eventName, this.preventDefaults, false);
        });

        this.dropArea.addEventListener('dragenter', () => this.dropArea.classList.add('highlight'));
        this.dropArea.addEventListener('dragleave', () => this.dropArea.classList.remove('highlight'));
        this.dropArea.addEventListener('drop', this.handleDrop.bind(this), false);
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleDrop(e) {
        this.preventDefaults(e);
        this.dropArea.classList.remove('highlight');

        if (!state.addMoreFilesFunctionalityExecuted) {
            UIManager.addMoreFilesFunctionality();
            const files = e.dataTransfer.files;
            this.processDroppedFiles(files);
            state.addMoreFilesFunctionalityExecuted = true;
        }

        const files = e.dataTransfer.files;
        Array.from(files).forEach(file => {
            if (file.type === 'application/pdf') {
                PDFHandler.fileHandler(file);
            }
        });
        FileUploader.uploadFile(Array.from(files));
    }

    processDroppedFiles(files) {
        Array.from(files).forEach(file => {
            if (file.type === 'application/pdf') {
                const objectUrl = URL.createObjectURL(file);
                state.objectUrls.push(objectUrl);
            }
        });
        compressFunctionality(state.objectUrls);
    }
}