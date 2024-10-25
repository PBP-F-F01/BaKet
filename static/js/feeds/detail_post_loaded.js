document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("reply-button").disabled = true;

    document.getElementById("reply-content").addEventListener("input", function() {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";    

        if (this.value.trim() === "") {
            document.getElementById("reply-button").disabled = true;
            document.getElementById("reply-button").classList.add("opacity-50", "cursor-not-allowed");
            document.getElementById("reply-button").classList.remove("hover:bg-[#0081B0]");
        } else {
            document.getElementById("reply-button").disabled = false;
            document.getElementById("reply-button").classList.remove("opacity-50", "cursor-not-allowed");
            document.getElementById("reply-button").classList.add("hover:bg-[#0081B0]");
        }
    });
});