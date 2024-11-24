import { DropAreaManager } from './modules/dropAreaManager.js';
import { FilePickerManager } from './modules/filePickerManager.js';

document.addEventListener('DOMContentLoaded', () => {
    new DropAreaManager('dropArea');
    FilePickerManager.initializeFilePickers();
});