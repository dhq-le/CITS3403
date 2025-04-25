document.addEventListener('DOMContentLoaded', () => {
	const sidebar = document.getElementById('sidebarMenu');
	const menuButton = document.getElementById('menu-button');
	const menuIcon = document.getElementById('menu-icon');
	const main = document.getElementById('main');


	function toggleSidebar() {
		sidebar.classList.toggle('collapsed');
		menuButton.classList.toggle('collapsed');
		menuIcon.classList.toggle('rotate');

		// Only adjust layout on desktop
		if (window.innerWidth >= 768) {
			main.classList.toggle('expanded');

		}
	}

	menuButton.addEventListener('click', toggleSidebar);


	function setVhUnit() {
		let vh = window.innerHeight * 0.01;
		document.documentElement.style.setProperty('--vh', `${vh}px`);
	}

	window.addEventListener('resize', setVhUnit);
	window.addEventListener('load', setVhUnit);

	function updateIconName() {
		if (window.innerWidth < 768) { // This is for mobile vs desktop
			menuIcon.setAttribute('name', 'menu');  // Change to 'menu' if width is less than 768px
		} else {
				menuIcon.setAttribute('name', 'chevrons-right');  // Revert to 'chevrons-right' if width is greater than or equal to 768px
		}
	}

	// Run the function when the page loads
	window.addEventListener('load', updateIconName);

	// Run the function whenever the window is resized
	window.addEventListener('resize', updateIconName);
});
