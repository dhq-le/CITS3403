function toggleSidebar() {
  const sidebar = document.getElementById('sidebarMenu');
  const main = document.getElementById('main');

  sidebar.classList.toggle('collapsed');

  // Only adjust layout on desktop
  if (window.innerWidth >= 768) {
    main.classList.toggle('expanded');
  }
}