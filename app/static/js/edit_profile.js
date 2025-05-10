function previewProfilePic(event) {
    const reader = new FileReader();
    reader.onload = function() {
      const img = document.getElementById('profilePicPreview');
      img.src = reader.result;
    };
    reader.readAsDataURL(event.target.files[0]);
  }