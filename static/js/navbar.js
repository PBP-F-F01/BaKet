function highlightNavbar() {
  const currentPath = window.location.pathname.replace(/\/$/, '');
  console.log("Current path:", currentPath);

  /* NAVBAR LINKS */
  const navbarLinks = document.querySelectorAll('#navbar a');

  // Highlight main navbar links
  navbarLinks.forEach(link => {
    if (link.id === 'login-link') return;
    const linkPath = link.getAttribute('href').replace(/\/$/, '');

    console.log("Checking navbar link path:", linkPath); // Debug

    if (currentPath.startsWith(linkPath) && linkPath !== '') {
      // Add blue, remove gray
      link.classList.add('text-[#01aae8]');
      link.classList.remove('text-[#c8c8c8]');

      console.log("Setting navbar link to blue:", link); // Debug
    } else {
      // Add gray, remove blue
      link.classList.add('text-[#c8c8c8]');
      link.classList.remove('text-[#01aae8]');

      console.log("Setting navbar link to gray:", link); // Debug
    }
  });

  /* DROPDOWN LINKS */
  const dropdownLinks = document.querySelectorAll('#dropdown-menu a');

  // Highlight dropdown links
  dropdownLinks.forEach(link => {
    const linkPath = link.getAttribute('href').replace(/\/$/, '');

    console.log("Checking dropdown link path:", linkPath); // Debug

    if (currentPath.startsWith(linkPath) && linkPath !== '') {
      // Add blue, remove gray
      link.classList.add('text-[#01aae8]');
      link.classList.remove('text-neutral-600');

      console.log("Setting dropdown link to blue:", link); // Debug
    } else {
      // Add gray, remove blue
      link.classList.add('text-neutral-600');
      link.classList.remove('text-[#01aae8]');

      console.log("Setting dropdown link to gray:", link); // Debug
    }
  });
}

// Run the function immediately
highlightNavbar();
