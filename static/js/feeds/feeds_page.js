function navbar() {
  const navbar = document.getElementById('navbar');
  const html = `<a href="/" class="text-[#c8c8c8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Beranda </a>
  <a href="/catalogue" class="text-[#c8c8c8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Catalogue</a>
  <a href="/feeds" class="text-[#01aae8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Forum</a>
  <a href="/articles" class="text-[#c8c8c8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Article</a>
  <a href="#" class="text-[#c8c8c8] text-base font-bold font-['Raleway'] hover:text-[#01aae8]">Wishlist</a>`;
navbar.innerHTML = html;
}

function dropdown() {
const dropdown = document.getElementById('dropdown-menu');
const html = `<div class="p-4">
  <div class="flex flex-col">
    <a href="/" class="text-neutral-600 text-sm mb-4 font-semibold font-['Raleway']">Beranda </a>
    <a class="text-neutral-600 text-sm mb-4 font-semibold font-['Raleway']">Catalogue</a>
    <a href="/feeds" class="text-[#01aae8] text-sm mb-4 font-semibold font-['Raleway']">Forum</a>
    <a href="/articles" class="text-neutral-600 text-sm mb-4 font-semibold font-['Raleway']">Article</a>
    <a class="text-neutral-600 text-sm font-semibold font-['Raleway']">Wishlist</a>
  </div>
</div>`;
dropdown.innerHTML = html;
}

navbar();
dropdown();