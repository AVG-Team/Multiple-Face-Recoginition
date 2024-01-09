window.addEventListener("load", () => {
    const upload = new UploadModal("#upload");
});

class UploadModal {
    filename = "";
    isUploading = false;
    progress = 0;
    progressTimeout = null;
    state = 0;

    constructor(el) {
        this.el = document.querySelector(el);
        this.el?.addEventListener("click", this.action.bind(this));
        this.el?.querySelector("#file")?.addEventListener("change", this.fileHandle.bind(this));
    }

    action(e) {
        this[e.target?.getAttribute("data-action")]?.();
        this.stateDisplay();
    }

    cancel() {
        this.isUploading = false;
        this.progress = 0;
        this.progressTimeout = null;
        this.state = 0;
        this.stateDisplay();
        this.progressDisplay();
        this.fileReset();
    }

    fail() {
        this.isUploading = false;
        this.progress = 0;
        this.progressTimeout = null;
        this.state = 2;
        this.stateDisplay();
    }

    file() {
        this.el?.querySelector("#file").click();
    }

    fileDisplay(name = "") {
        // update the name
        this.filename = name;

        const fileValue = this.el?.querySelector("[data-file]");
        if (fileValue) fileValue.textContent = this.filename;

        // show the file
        this.el?.setAttribute("data-ready", this.filename ? "true" : "false");
    }

    fileHandle(e) {
        return new Promise(() => {
            const {target} = e;
            if (target?.files.length) {
                let reader = new FileReader();
                reader.onload = e2 => {
                    this.fileDisplay(target.files[0].name);
                };
                reader.readAsDataURL(target.files[0]);
            }
        });
    }

    fileReset() {
        const fileField = this.el?.querySelector("#file");
        if (fileField) fileField.value = null;
        this.fileDisplay();
    }

    progressDisplay() {
        const progressValue = this.el?.querySelector("[data-progress-value]");
        const progressFill = this.el?.querySelector("[data-progress-fill]");
        const progressTimes100 = Math.floor(this.progress * 100);

        if (progressValue) progressValue.textContent = `${progressTimes100}%`;
        if (progressFill) progressFill.style.transform = `translateX(${progressTimes100}%)`;
    }

    async progressLoop() {
        this.progressDisplay();

        if (this.isUploading) {
            if (this.progress === 0) {
            }
            // …or continue with progress
            if (this.progress < 1) {
                console.log(this.progress)
                if (this.progress === 0.09) {
                    await uploadImg(this.el?.querySelector("#file").files[0]);
                }
                this.progress += 0.01;
                this.progressTimeout = setTimeout(this.progressLoop.bind(this), 50);
            } else if (this.progress >= 1) {
                this.progressTimeout = setTimeout(() => {
                    if (this.isUploading) {
                        this.success();
                        this.stateDisplay();
                        this.progressTimeout = null;
                    }
                }, 250);
            }
        }
    }

    stateDisplay() {
        this.el?.setAttribute("data-state", `${this.state}`);
    }

    success() {
        this.isUploading = false;
        this.state = 3;
        this.stateDisplay();
    }

    upload() {
        if (!this.isUploading) {
            this.isUploading = true;
            this.progress = 0;
            this.state = 1;
            this.progressLoop();
        }
    }
}

const close_btn = document.getElementById("close_button");
const previewImage = document.getElementById('preview');
close_btn.addEventListener("click", () => {
    previewImage.src = null;
    previewImage.classList.add("hidden");
    document.body.style.height = "100vh";
});

async function uploadImg(fileUpload) {
    try {
        const file = fileUpload;
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data)
            alert("Uploaded successfully: " + data.message);
            console.log('Uploaded successfully: ', data.message);


            const open = document.getElementById("folder_open");
            console.log(open)
            open.href = "/attendances?q=" + data.folder;
        } else {
            alert("Error when uploading: " + data.error);
            console.error('Error when uploading: ', data.error);
        }
    } catch (e) {
        alert("Error when uploading: " + e);
        console.error('Error when uploading: ', e);
    }

}

document.getElementById('file').addEventListener('change', function (event) {
    const fileInput = event.target;
    previewImage.classList.remove("hidden");
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            previewImage.src = e.target.result;
        };

        reader.readAsDataURL(fileInput.files[0]);
    }
    document.body.style.height = "200vh";
});
