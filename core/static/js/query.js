function closeFileList() {
  var fileList = document.querySelector('.file-list');
  fileList.style.display = 'none';
  var closeButton = document.querySelector('.close-button');
  closeButton.style.display = 'block';
  // 清除 div 元素中的内容
  fileList.innerHTML = '';
}