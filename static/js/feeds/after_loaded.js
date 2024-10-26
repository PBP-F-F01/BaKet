document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchForm').addEventListener('submit', function (event) {
        event.preventDefault();
        const query = document.getElementById('searchInput').value;
        if (query) {
            alert('Searching for: ' + query);
            // TODO: Implement search functionality
            // For search: window.location.href = `/search/?q=${encodeURIComponent(query)}`;
        } else {
            alert("Search query cannot be empty!");
        }
    });

    document.getElementById('searchInput').addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            document.getElementById('searchForm').dispatchEvent(new Event('submit'));  // Trigger form submission
        }
    });

    document.getElementById('your-posts').addEventListener('click', function () {
        window.location.href = "/feeds/tabs/your/";
    });

    document.getElementById('discover').addEventListener('click', function () {
        window.location.href = "/feeds/tabs/all/";
    });

    document.getElementById("post-content").addEventListener("input", function() {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";

        if (this.value.trim() === "") {
            document.getElementById("post-button").disabled = true;
            document.getElementById("post-button").classList.add("opacity-50", "cursor-not-allowed");
            document.getElementById("post-button").classList.remove("hover:bg-[#0081B0]");
        } else {
            document.getElementById("post-button").disabled = false;
            document.getElementById("post-button").classList.remove("opacity-50", "cursor-not-allowed");
            document.getElementById("post-button").classList.add("hover:bg-[#0081B0]");
        }
    });
});