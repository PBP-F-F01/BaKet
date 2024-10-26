function highlightNavbar() {
  const currentPath = window.location.pathname.replace(/\/$/, '');
  console.log("Current path:", currentPath);

  /* NAVBAR LINKS */
  const navbarLinks = document.querySelectorAll('#navbar a');

  // Highlight main navbar links
  navbarLinks.forEach(link => {
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

// Function to fetch and update the cart count asynchronously
function fetchCartCount() {
  fetch('/cart/count/', {
    method: 'GET',
    headers: {
      'X-Requested-With': 'XMLHttpRequest' // Ensures Django recognizes it as an AJAX request
    }
  })
  .then(response => response.json())
  .then(data => {
    // Get cart count elements from the navbar (both desktop and mobile)
    const cartCountElement = document.getElementById('cart-count');
    const mobileCartCountElement = document.getElementById('cart-count-mobile');

    // Update the cart count in the navbar (desktop)
    if (cartCountElement) {
      cartCountElement.innerText = data.cart_count;  // Update the number of items
    }

    // Update the cart count in the navbar (mobile)
    if (mobileCartCountElement) {
      mobileCartCountElement.innerText = data.cart_count;  // Update the number of items
    }
  })
  .catch(error => {
    // console.error('Error fetching cart count:', error);  // Log any errors to the console
  });
}

// Run the functions when the page loads
document.addEventListener('DOMContentLoaded', () => {
  highlightNavbar();
  fetchCartCount();  // Fetch cart count on page load
});