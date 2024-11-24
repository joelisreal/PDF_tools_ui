// uiManager.js
export class UIManager {
    static addMoreFilesFunctionality() {
        const content = document.getElementById('dropArea');
        const sideTools = document.createElement('div');
        sideTools.classList.add('side-tools');
        content.appendChild(sideTools);

        const addMoreFiles = document.getElementById('add-more-files');
        addMoreFiles.style.display = 'block';

        const spanTxt = document.createElement('span');
        spanTxt.classList.add('tooltip');
        spanTxt.setAttribute('id', 'side-tools-upload-txt');
        spanTxt.appendChild(document.createTextNode('Add more files'));

        sideTools.appendChild(addMoreFiles);
        sideTools.appendChild(spanTxt);
        sideTools.style.border = "dashed green";
    }
}