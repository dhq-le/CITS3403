document.addEventListener('DOMContentLoaded', function() {
  // 聚焦到添加好友输入框
  var input = document.querySelector('.friend-input');
  if (input) input.focus();

  // 5秒后淡出所有 flash
  var flashes = document.querySelectorAll('.flash');
  if (flashes.length) {
    setTimeout(function() {
      flashes.forEach(function(el) {
        el.classList.add('fade-out');
      });
    }, 5000);
  }
});
