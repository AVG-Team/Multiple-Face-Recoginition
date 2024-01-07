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
            document.getElementById('time-camera').classList.remove("hidden");
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
        //    content.style = "margin-top: 250px";

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

    function loadingShow() {
        const loadingDiv = document.getElementById("background-loading");
        loadingDiv.classList.add("showLoading")
    }

    function loadingHide() {
        const loadingDiv = document.getElementById("background-loading");
        loadingDiv.classList.add("hideLoading")
    }

    upload.addEventListener("click", () => {
        if (capturedDataURL) {
            loadingShow();
            const blob = dataURItoBlob(capturedDataURL);

            const formData = new FormData();
            formData.append('file', blob, 'captured_image.png');

            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    loadingHide();
                    setTimeout(function () {
                        document.getElementById("background-loading").classList.remove('showLoading');
                    }, 2000);
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
                    loadingHide();
                    alert("Error when uploading: " + error);
                    console.error('Error when uploading: ', error);
                });
        }
    })


    function flipVideo() {
        cameraOutput.style.transform = cameraFront ? "scaleX(-1)" : "scaleX(1)";
    }


    var timerElement = document.querySelector('.timer');

    function updateTimer() {
        let currentTime = new Date();
        let hours = currentTime.getHours().toString().padStart(2, '0');
        let minutes = currentTime.getMinutes().toString().padStart(2, '0');
        let seconds = currentTime.getSeconds().toString().padStart(2, '0');

        let formattedTime = hours + ':' + minutes + ':' + seconds;
        timerElement.textContent = formattedTime;
    }

    // Update the timer every second
    setInterval(updateTimer, 1000);

    // Optionally, you can call updateTimer once to set the initial value
    updateTimer();


    document.getElementById('link_camera').addEventListener('click', function () {
        document.getElementById('camera_tab').classList.remove('hidden');
        document.getElementById('upload_tab').classList.add('hidden');
    });

    document.getElementById('link_upload').addEventListener('click', function () {
        document.getElementById('upload_tab').classList.remove('hidden');
        document.getElementById('camera_tab').classList.add('hidden');
    });

    const open = document.querySelector('.container');
    const close = document.querySelector('.close');
    let tl = gsap.timeline({defaults: {duration: 1, ease: 'expo.inOut'}});
    open.addEventListener('click', () => {
        if (tl.reversed()) {
            tl.play();
        } else {
            tl.to('.nav_animation', {right: 0})
                .to('.nav_animation', {height: '120vh'}, '-=.1')
                .to('.nav_animation ul li a', {opacity: 1, pointerEvents: 'all', stagger: .2}, '-=.8')
                .to('.close', {opacity: 1, pointerEvents: 'all'}, "-=.8")
                .to('.nav_animation h2', {opacity: 1}, '-=1');
        }
    });

    close.addEventListener('click', () => {
        tl.reverse();
        document.getElementById('camera_output').classList.add('hidden');
    });

    const typewriter = document.getElementById('typewriter');
    const text = "Hệ thống điểm danh Hutech"
    let index = 0;

    function type() {
        if (index < text.length) {
            typewriter.innerHTML = text.slice(0, index) + '<span class="blinking-cursor">|</span>';
            index++;
            setTimeout(type, Math.random() * 150 + 50);
        } else {
            typewriter.innerHTML = text.slice(0, index) + '<span class="blinking-cursor">|</span>';
        }
    }

    // start typing
    type();

    document.addEventListener('DOMContentLoaded', function () {
        const ulElement = document.querySelector('.nav_animation ul');
        const divToToggle = document.querySelector('.nav_animation div[style="margin-bottom: 0px;"]');
        let lastScrollPosition = 0;

        ulElement.addEventListener('scroll', function () {
            const currentScrollPosition = ulElement.scrollTop;

            if (currentScrollPosition > lastScrollPosition) {
                // Scrolling down
                divToToggle.classList.add('hidden');
            } else {
                // Scrolling up
                divToToggle.classList.remove('hidden');
            }

            lastScrollPosition = currentScrollPosition;
        });
    });
});
