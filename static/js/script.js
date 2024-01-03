const indicator = document.querySelector('.nav-indicator-wrapper');
const items = document.querySelectorAll('.nav-item');

function handleIndicator(el) {
    items.forEach(item => {
        item.classList.remove('is-active');
    });


    indicator.style.width = `${el.offsetWidth}px`;
    indicator.style.left = `${el.offsetLeft}px`;

    el.classList.add('is-active');
}

function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(',')[1]);
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const intArray = new Uint8Array(arrayBuffer);

    for (let i = 0; i < byteString.length; i++) {
        intArray[i] = byteString.charCodeAt(i);
    }

    return new Blob([arrayBuffer], {type: mimeString});
}

items.forEach((item) => {
    item.addEventListener('click', (e) => {
        handleIndicator(item)
    });

    item.classList.contains('is-active') && handleIndicator(item);
});

let cameraFront = true;

document.addEventListener('DOMContentLoaded', function () {
    const openCameraButton = document.getElementById('open_camera');
    const cameraOutput = document.getElementById('camera_output');
    const captureButton = document.getElementById('capture_button');
    const captureArrow = document.getElementById('capture_arrow');
    const capturedImage = document.getElementById('captured_image');
    const upload = document.getElementById('upload_button');
    const folder = document.getElementById('folder_open');
    const body = document.getElementsByTagName('body');
    const content = document.querySelector(".content");

    let capturedDataURL = '';

    openCameraButton.addEventListener('click', async () => {
        try {
            body[0].classList.add("center");

            console.log(123);
            cameraOutput.classList.remove("hidden");
            const stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: "environment"}});

            cameraOutput.srcObject = stream;
            captureButton.classList.remove("hidden");
            captureArrow.classList.remove("hidden");
            flipVideo();
            openCameraButton.classList.add("hidden");
        } catch (error) {
            alert("Cannot open camera")
            console.error('Cannot open camera: ', error);
        }
    });

    captureButton.addEventListener("click", () => {
        content.style = "margin-bottom:200px";

        const canvas = document.createElement('canvas');
        canvas.width = cameraOutput.videoWidth;
        canvas.height = cameraOutput.videoHeight;

        const context = canvas.getContext('2d');
        context.translate(cameraFront ? canvas.width : 0, 0);
        context.scale(cameraFront ? -1 : 1, 1);
        context.drawImage(cameraOutput, 0, 0, canvas.width, canvas.height);

        const imageURL = canvas.toDataURL('image/png');
        capturedDataURL = canvas.toDataURL('image/png');

        capturedImage.src = imageURL;
        capturedImage.classList.remove("hidden");
        upload.classList.remove("hidden");
        upload.classList.add("w-fit");
    })
    captureArrow.addEventListener("click", async () => {
        let stream;
        if (cameraFront) {
            cameraFront = false;
            stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: "user"}});

        } else {
            cameraFront = true;
            stream = await navigator.mediaDevices.getUserMedia({video: {facingMode: "environment"}});
        }

        flipVideo();
        cameraOutput.srcObject = stream;
    })

    upload.addEventListener("click", () => {
        if (capturedDataURL) {
            const blob = dataURItoBlob(capturedDataURL);

            const formData = new FormData();
            formData.append('file', blob, 'captured_image.png');

            console.log(formData, capturedDataURL, blob)

            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    if ('error' in data) {
                        alert("Error when uploading: " + data.error);
                        console.error('Error when uploading: ', data.error);
                    } else {
                        alert("Uploaded successfully: " + data.message);
                        console.log('Uploaded successfully: ', data.message);

                        folder.classList.remove("hidden");
                        folder.href = "/attendances?q=" + data.folder;
                    }
                    console.log(data)
                })
                .catch(error => {
                    alert("Error when uploading: " + error);
                    console.error('Error when uploading: ', error);
                });
        }
    })

    function flipVideo() {
        cameraOutput.style.transform = cameraFront ? "scaleX(-1)" : "scaleX(1)";
    }
});
