
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('uploadForm');
  const progress = document.querySelector('.progress');
  const progressBar = document.getElementById('progressBar');
  const result = document.getElementById('result');
  const downloadLink = document.getElementById('downloadLink');
  const fileInput = document.getElementById('fileInput');
  const fileLabel = document.getElementById('fileLabel');

  fileInput.addEventListener('change', function () {
    if (fileInput.files.length > 0) {
      fileLabel.innerText = '📁 ' + fileInput.files[0].name;
    } else {
      fileLabel.innerText = '📂 Chọn file MP3 hoặc MP4';
    }
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    result.classList.add('hidden');
    progress.classList.remove('hidden');
    progressBar.style.width = '0%';
    progressBar.textContent = '0%';

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/convert', true);

    xhr.upload.onprogress = function (e) {
      if (e.lengthComputable) {
        const percent = Math.round((e.loaded / e.total) * 100);
        progressBar.style.width = percent + '%';
        progressBar.textContent = percent + '%';
      }
    };

    xhr.onload = function () {
      if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        if (data.download_url) {
          downloadLink.href = data.download_url;
          result.classList.remove('hidden');
        } else {
          alert(data.error || 'Lỗi không xác định.');
        }
      } else {
        alert('Lỗi trong quá trình chuyển đổi.');
      }
      progress.classList.add('hidden');
    };

    xhr.onerror = function () {
      alert('Không thể kết nối đến máy chủ.');
      progress.classList.add('hidden');
    };

    xhr.send(formData);
  });
});
