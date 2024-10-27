function navbar() {
    const navbar = document.getElementById('navbar');
    const html = `<a href="/" class="text-[#c8c8c8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Beranda </a>
    <a href="/catalogue" class="text-[#c8c8c8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Catalogue</a>
    <a href="/feeds" class="text-[#c8c8c8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Forum</a>
    <a href="/articles" class="text-[#c8c8c8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Article</a>
    <a href="/wishlist" class="text-[#01aae8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Wishlist</a>
    
    <!-- Cart Icon with Cart Count -->
      <a href="{% url 'view_cart' %}" class="relative text-[#01aae8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">
        <img src="{% static 'images/cart_icon.svg' %}" alt="Cart" class="h-5 inline-block">
        <span id="cart-count" class="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
          {{ cart_count }}
        </span>
      </a>`;
  navbar.innerHTML = html;
  }
  
  function dropdown() {
  const dropdown = document.getElementById('dropdown-menu');
  const html = `<div class="p-4">
    <div class="flex flex-col">
      <a href="/" class="text-neutral-600 text-sm mb-4 font-semibold font-['Raleway']">Beranda </a>
      <a href="/catalogue" class="text-neutral-600 text-sm mb-4 font-semibold font-['Raleway']">Catalogue</a>
      <a href="/feeds" class="text-neutral-600 text-sm mb-4 font-semibold font-['Raleway']">Forum</a>
      <a href="/articles" class="text-neutral-600 text-sm mb-4 font-semibold font-['Raleway']">Article</a>
      <a href="/wishlist" class="text-[#01aae8] text-sm font-semibold font-['Raleway']">Wishlist</a>
  
      <!-- Cart Icon in Mobile Dropdown -->
        <a href="/cart" class="relative text-[#01aae8] text-sm font-semibold font-['Raleway']">
          <img src="{% static 'images/cart_icon.svg' %}" alt="Cart" class="h-5 inline-block">
          <span id="cart-count-mobile" class="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
            {{ cart_count }}
          </span>
        </a>
    </div>
  </div>`;
  dropdown.innerHTML = html;
  }
  
  // navbar();
  function highlightNavbar() {
    const currentPath = window.location.pathname.replace(/\/$/, ''); // Remove trailing slash if present
    console.log("Current path:", currentPath);
  
    // Select all navbar and dropdown links
    const navbarLinks = document.querySelectorAll('#navbar a, #dropdown-menu a');
  
    navbarLinks.forEach(link => {
      const linkPath = link.getAttribute('href').replace(/\/$/, ''); // Remove trailing slash if present
      console.log("Checking link path:", linkPath); // Debug: log each link path
  
      // Check if the link path matches the current path
      if (linkPath === currentPath || (currentPath === '/' && linkPath === '')) {
        link.classList.add('text-[#01aae8]'); // Add blue color for active page
        link.classList.remove('text-[#c8c8c8]'); // Remove gray color
        console.log("Setting link to blue:", link); // Log active link for confirmation
      } else {
        link.classList.add('text-[#c8c8c8]'); // Set gray for non-active links
        link.classList.remove('text-[#01aae8]'); // Ensure blue is removed for non-active links
        console.log("Setting link to gray:", link); // Log non-active link
      }
    });
  }
  
  // Run the function immediately
  highlightNavbar();
  dropdown();