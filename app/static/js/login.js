// static/login.js
document.addEventListener('DOMContentLoaded', function() {
  var toPwdBtn = document.getElementById('to-password');
  var stepUser = document.getElementById('step-username');
  var stepPwd  = document.getElementById('step-password');
  var usernameInput = document.getElementById('usernameInput');
  var usernameDisplay = document.getElementById('usernameDisplay');

  toPwdBtn.addEventListener('click', function() {
    var u = usernameInput.value.trim();
    if (!u) {
      alert('please enter a valid username.');
      return;
    }
    usernameDisplay.textContent = u;
    stepUser.style.display = 'none';
    stepPwd.style.display  = 'block';
  });
});
