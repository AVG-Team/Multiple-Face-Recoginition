const items = document.querySelectorAll('.img-item');
// for文
for (let i = 0; i < items.length; i++) {

    const keyframes = {
        opacity: [0, 1],
        translate: ['0 50px', 0],
        filter: ['blur(10px)', 'blur(0)'],
    };

    const options = {
        duration: 600,
        delay: i * 400,
        fill: 'forwards',
    };

    items[i].animate(keyframes, options);
}

// forEach文への書き換えもできる
items.forEach((item, i) => {

    const keyframes = {
        opacity: [0, 1],
        translate: ['0 50px', 0],
        filter: ['blur(10px)', 'blur(0)'],
    };

    const options = {
        duration: 600,
        delay: i * 400,
        fill: 'forwards',
    };

    item.animate(keyframes, options);
});
document.getElementById('export').addEventListener('click', uploadFile);
function uploadFile() {
    const value = document.getElementById('folder').value;
    var formData = new FormData();
    formData.append('key', '12345678');
    formData.append('q', value);
    console.log(value)

    // Gửi dữ liệu CSV lên máy chủ Python
    fetch('/attendance/export', {
        method: 'POST',
        body: formData
    })
        .then(response => response.blob())
        .then(blob => {
            // Tạo một URL Blob cho file CSV
            var url = window.URL.createObjectURL(blob);

            // Tạo một thẻ a để tạo liên kết tải xuống và kích vào nó
            var a = document.createElement('a');
            a.href = url;
            a.download = 'attendances.csv';
            document.body.appendChild(a);
            a.click();

            // Xóa thẻ a
            document.body.removeChild(a);

            // Giải phóng URL Blob
            window.URL.revokeObjectURL(url);
        });
}



