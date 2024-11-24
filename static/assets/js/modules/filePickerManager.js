// filePickerManager.js
import { state } from './state.js';
import { UIManager } from './uiManager.js';
import { PDFHandler } from './pdfHandler.js';
import { FileUploader } from './fileUploader.js';
import { compressFunctionality } from '../compresspdf.js';

export class FilePickerManager {
    static initializeFilePickers() {
        const pickFiles = document.getElementById('pickfiles');
        if (pickFiles) {
            pickFiles.addEventListener('click', () => this.fileAdderButton(pickFiles));
        }

        const addMoreFiles = document.getElementById('add-more-files');
        addMoreFiles.addEventListener('click', () => this.fileAdderButton(addMoreFiles));
    }

    static fileAdderButton(button) {
        const fileInput = this.createFileInput();
        document.body.appendChild(fileInput);
        fileInput.click();
        fileInput.parentNode.removeChild(fileInput);
    }

    static createFileInput() {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.multiple = 'multiple';
        fileInput.accept = 'application/pdf';
        fileInput.style.display = 'none';
        fileInput.addEventListener('change', this.handleFileSelection);
        return fileInput;
    }

    static handleFileSelection(e) {
        if (!state.addMoreFilesFunctionalityExecuted) {
            UIManager.addMoreFilesFunctionality();
            const files = e.target.files;
            Array.from(files).forEach(file => {
                if (file.type === 'application/pdf') {
                    const objectUrl = URL.createObjectURL(file);
                    state.objectUrls.push(objectUrl);
                }
            });
            compressFunctionality(state.objectUrls);
            state.addMoreFilesFunctionalityExecuted = true;
        }

        Array.from(e.target.files).forEach(file => {
            if (file.type === 'application/pdf') {
                PDFHandler.fileHandler(file);
            }
        });
        FileUploader.uploadFile(Array.from(e.target.files));
    }
}