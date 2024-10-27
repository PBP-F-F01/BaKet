document.addEventListener('DOMContentLoaded', function () {
    if (!(document.getElementById("reply-button") === null)){
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
    }

    // Kalo login user mah pasti bisa update
    document.getElementById("edit-content").addEventListener("input", function() {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";

        if (this.value.trim() === "") {
            document.getElementById("confirm-edit-button").disabled = true;
            document.getElementById("confirm-edit-button").classList.add("opacity-50", "cursor-not-allowed");
            document.getElementById("confirm-edit-button").classList.remove("hover:bg-[#0081B0]");
        } else {
            document.getElementById("confirm-edit-button").disabled = false;
            document.getElementById("confirm-edit-button").classList.remove("opacity-50", "cursor-not-allowed");
            document.getElementById("confirm-edit-button").classList.add("hover:bg-[#0081B0]");
        }
    });

    document.getElementById("options-button").addEventListener("click", (e) => {
        document.getElementById("options-menu").classList.toggle("hidden");
    });

    document.getElementById("delete-post-button").addEventListener("click", () => {
        document.getElementById("delete-modal").classList.remove("hidden");
        document.getElementById("options-menu").classList.add("hidden");
    });

    document.getElementById("cancel-delete-button").addEventListener("click", () => {
        document.getElementById("delete-modal").classList.add("hidden");
    });

    document.getElementById("edit-post-button").addEventListener("click", () => {
        document.getElementById("edit-modal").classList.remove("hidden");
        document.getElementById("options-menu").classList.add("hidden");
    });

    document.getElementById("cancel-edit-button").addEventListener("click", () => {
        document.getElementById("edit-modal").classList.add("hidden");
    });

    document.addEventListener("click", (event) => {
        if (!document.getElementById("options-button").contains(event.target) && !document.getElementById("options-menu").contains(event.target)) {
            document.getElementById("options-menu").classList.add("hidden");
        }
    });
});