function navbar() {
    const navbar = document.getElementById('navbar');
    const html = `<a href="/" class="text-[#c8c8c8] text-lg font-bold font-['Raleway'] hover:text-[#01aae8]">Beranda </a>
          <a href="/catalogue" class="text-[#01aae8] text-lg font-bold font-['Raleway'] hover:text-[#01aae8]">Catalogue</a>
          <a href="/feeds" class="text-[#c8c8c8] text-lg font-bold font-['Raleway'] hover:text-[#01aae8]">Forum</a>
          <a href="/articles" class="text-[#c8c8c8] text-lg font-bold font-['Raleway'] hover:text-[#01aae8]">Article</a>
          <a class="text-[#c8c8c8] text-lg font-bold font-['Raleway'] hover:text-[#01aae8]">Wishlist</a>`;
  navbar.innerHTML = html;
}
navbar();