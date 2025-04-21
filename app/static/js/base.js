function toggleSidebar() {
  const sidebar = document.getElementById('sidebarMenu');
  const menuButton = document.getElementById('menu-button');
  const main = document.getElementById('main');

  sidebar.classList.toggle('collapsed');
  menuButton.classList.toggle('collapsed');

  // Only adjust layout on desktop
  if (window.innerWidth >= 768) {
    main.classList.toggle('expanded');
  }
}

function setVhUnit() {
  let vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
}

window.addEventListener('resize', setVhUnit);
window.addEventListener('load', setVhUnit);

function updateIconName() {
  const menuButton = document.getElementById("menu-button");

  if (window.innerWidth < 768) {
    menuButton.setAttribute('name', 'menu');  // Change to 'menu' if width is less than 768px
  } else {
    menuButton.setAttribute('name', 'chevrons-right');  // Revert to 'menu-alt-left' if width is greater than or equal to 768px
  }
}

// Run the function when the page loads
window.addEventListener('load', updateIconName);

// Run the function whenever the window is resized
window.addEventListener('resize', updateIconName);