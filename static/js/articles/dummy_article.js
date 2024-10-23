document.querySelector("#like-button").addEventListener("click", async (e) => {
    e.preventDefault();
    console.log("like button clicked");
    const button = document.querySelector("#like-button");
    const likeCount = document.querySelector("#like-count");

    if (button.classList.contains("selected")) {
        button.classList.remove("selected");
        button.classList.remove("text-[#01aae8]");
        button.classList.add("text-[#c8c8c8]");
        button.classList.add("hover:text-[#01aae8]");
        likeCount.innerText = parseInt(likeCount.innerText) - 1;
    }
    else {
        button.classList.add("selected");
        button.classList.remove("text-[#c8c8c8]");
        button.classList.add("text-[#01aae8]");
        button.classList.remove("hover:text-[#01aae8]");
        likeCount.innerText = parseInt(likeCount.innerText) + 1;
    }
});

document.querySelector("#like-button").addEventListener("touchend", async (e) => {
    e.preventDefault();
    console.log("like button clicked");
    const button = document.querySelector("#like-button");
    const likeCount = document.querySelector("#like-count");

    if (button.classList.contains("selected")) {
        button.classList.remove("selected");
        button.classList.remove("text-[#01aae8]");
        button.classList.add("text-[#c8c8c8]");
        button.classList.add("hover:text-[#01aae8]");
        likeCount.innerText = parseInt(likeCount.innerText) - 1;
    }
    else {
        button.classList.add("selected");
        button.classList.remove("text-[#c8c8c8]");
        button.classList.add("text-[#01aae8]");
        button.classList.remove("hover:text-[#01aae8]");
        likeCount.innerText = parseInt(likeCount.innerText) + 1;
    }
});