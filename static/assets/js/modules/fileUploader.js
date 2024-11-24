export class FileUploader {
    static uploadFile(files) {
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));

        $.ajax({
            type: 'POST',
            url: '/upload',
            data: formData,
            contentType: false,
            processData: false,
            success: (data) => {
                console.log(data);
                alert(data.message);
                console.log("Uploaded file:", data.filename);
            },
            error: (err) => {
                alert("File upload failed.");
                console.error(err);
            }
        });
    }
}