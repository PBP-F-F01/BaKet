async function getComment(article_id) {
    try {
        const response = await fetch(`/articles/json/comment/${article_id}/`, {
            headers: {
                'X-CSRFToken': csrf_token
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching comments:', error);
        return []; // or some other default value
    }
}

async function refreshComments(article_id) {
    const commentSectionDesktop = document.querySelector(".desktop").querySelector('.comment-section');
    const comments = await getComment(article_id);
    let html = "";
    if (comments.length === 0) {
        html += `<p class="text-gray-500 text-center mt-4">No comments yet</p>`;
    }
    else {
        comments.forEach(c => {
            const content = parseContent(c.content);
            html += `<div class="mt-4 comment" comment-id="${c.id}">
                    <p class="text-left mb-2 break-words">
                        <span class="font-bold">${c.author}</span> - <span class="text-gray-500">${c.time}`;
            
            if (c.has_edited) {
                html += `<span class="text-gray-500"> (edited)</span>`;
            }
            
            html += `</span>
                    </p>
                    <p class="text-left break-words leading-7 content">
                        ${content}
                    </p>
                    <div class="flex items-center cursor-default flex-wrap like">`;
            
            if (c.is_like) {
                html += `<span comment-like-id="${c.id}" class="material-icons m-1 text-[#01aae8] hover:text-[#15a1d4] like-button">thumb_up</span>`;
            }
            else {
                html += `<span comment-like-id="${c.id}" class="material-icons m-1 text-[#c8c8c8] hover:text-[#01aae8] like-button">thumb_up</span>`;
            }
            
            html += ` <span class="like-count">${c.like_count}</span>`;

            if (c.can_edit) {
                html += `<span edit-id="${c.id}" class="material-icons ml-5 m-1 text-[#01aae8] hover:text-[#15a1d4] edit-button">edit</span>
                        <span delete-id="${c.id}" class="material-icons m-1 text-[#ff0000] hover:text-[#ff3737] delete-button">delete</span>`;
            }

            html += `</div>
                </div>`;
        });
    }
    commentSectionDesktop.innerHTML = html;

    const commentSectionMobile = document.querySelector(".mobile").querySelector('.comment-section');

    html = "";
    if (comments.length === 0) {
        html += `<p class="text-gray-500 text-center mt-4">No comments yet</p>`;
    }
    else {
        comments.forEach(c => {
            const content = parseContent(c.content);
            html += `<div class="mt-4 comment" comment-id="${c.id}">
                    <p class="text-left mb-2 break-words">
                        <span class="font-bold">${c.author}</span> - <span class="text-gray-500">${c.time}`;
            
            if (c.has_edited) {
                html += `<span class="text-gray-500"> (edited)</span>`;
            }
            
            html += `</span>
                    </p>
                    <p class="text-left break-words leading-7 content">
                        ${content}
                    </p>
                    <div class="flex items-center cursor-default flex-wrap like">`;

            if (c.is_like) {
                html += `<span comment-like-id="${c.id}" class="material-icons m-1 text-[#01aae8] hover:text-[#15a1d4] like-button">thumb_up</span>`;
            }
            else {
                html += `<span comment-like-id="${c.id}" class="material-icons m-1 text-[#c8c8c8] hover:text-[#01aae8] like-button">thumb_up</span>`;
            }

            html += ` <span class="like-count">${c.like_count}</span>`;

            if (c.can_edit) {
                html += `<span edit-id="${c.id}" class="material-icons ml-5 m-1 text-[#01aae8] hover:text-[#15a1d4] edit-button">edit</span>
                        <span delete-id="${c.id}" class="material-icons m-1 text-[#ff0000] hover:text-[#ff3737] delete-button">delete</span>`;
            }

            html += `</div>
                </div>`;
        });
    }

    commentSectionMobile.innerHTML = html;

    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', async () => {
            const commentId = button.getAttribute('edit-id');
            const commentElement = button.parentElement.parentElement;
            const contentElement = commentElement.querySelector('.content');
            const originalContent = contentElement.textContent.trim();

            // Create a textarea to edit the comment
            const textarea = document.createElement('textarea');
            textarea.value = originalContent;
            textarea.classList.add('border', 'border-gray-300', 'rounded-md', 'p-2', 'w-full', 'h-20', 'hover:border-[#171e2a]', 'text-black');
            contentElement.innerHTML = '';
            contentElement.appendChild(textarea);

            // Hide the edit, delete, and like buttons
            button.classList.add('hidden');
            const deleteButton = commentElement.querySelector('.delete-button');
            deleteButton.classList.add('hidden');
            const likeButton = commentElement.querySelector('.like-button');
            likeButton.classList.add('hidden');

            // Create a save button
            const saveButton = document.createElement('button');
            saveButton.textContent = 'Save';
            saveButton.classList.add('bg-[#01aae8]', 'hover:bg-[#15a1d4]', 'text-white', 'font-semibold', 'py-2', 'px-4', 'rounded-[10px]', 'use-poppins', 'm-1', 'mt-2', 'self-end');
            commentElement.appendChild(saveButton);

            // Create a cancel button
            const cancelButton = document.createElement('button');
            cancelButton.textContent = 'Cancel';
            cancelButton.classList.add('bg-[#ff0000]', 'hover:bg-[#ff3737]', 'text-white', 'font-semibold', 'py-2', 'px-4', 'rounded-[10px]', 'use-poppins', 'm-1', 'mt-2', 'self-end', 'ml-2');
            commentElement.appendChild(cancelButton);

            // Add an event listener to the save button
            saveButton.addEventListener('click', async () => {
                const newContent = textarea.value;
                const response = await fetch(`/articles/update_comment/${commentId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token,
                    },
                    body: JSON.stringify({ content: newContent }),
                });

                if (response.ok) {
                    contentElement.innerHTML = newContent;
                    saveButton.remove();
                    cancelButton.remove();
                    button.classList.remove('hidden');
                    deleteButton.classList.remove('hidden');
                    likeButton.classList.remove('hidden');
                } 
                else {
                    console.error('Error updating comment:', response.statusText);
                    contentElement.innerHTML = originalContent;
                    saveButton.remove();
                    cancelButton.remove();
                    button.classList.remove('hidden');
                    deleteButton.classList.remove('hidden');
                    likeButton.classList.remove('hidden');
                }
            });

            // Add an event listener to the cancel button
            cancelButton.addEventListener('click', () => {
                contentElement.innerHTML = originalContent;
                saveButton.remove();
                cancelButton.remove();
                button.classList.add('hidden');
                deleteButton.classList.add('hidden');
                likeButton.classList.remove('hidden');
            });
        });
    });

    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', async event => {
            // Get the comment ID from the delete button
            const commentId = event.target.getAttribute('delete-id');

            // Confirm deletion with the user
            const confirmDelete = confirm('Are you sure you want to delete this comment?');

            if (confirmDelete) {
            // Send a DELETE request to the server to delete the comment
                try {
                    const response = await fetch(`/articles/delete_comment/${commentId}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': csrf_token,
                        },
                    });

                    if (response.ok) {
                        // Refresh the comments after deletion
                        refreshComments(article_id);
                    } 
                    else {
                        console.error('Failed to delete comment:', response.status);
                    }
                } 
                catch (error) {
                    console.error('Error deleting comment:', error);
                }
            }
        });
    });
}

function cleanTime() {
    const created_at = document.body.querySelectorAll(".created_at");

    created_at.forEach(c => {
        c.innerHTML = getTime(c.innerHTML);
    });
}

function cleanContent() {
    const content = document.body.querySelectorAll(".content");

    content.forEach(c => {
        c.innerHTML = parseContent(c.innerHTML);
    });
}

async function addCommentDesktop() {
    const commentText = document.getElementById("comment-input-desktop").querySelector("textarea").value;

    const response = await fetch(`/articles/add_comment/${article_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ content: commentText }),
    });

    if (response.ok) {
        document.getElementById("comment-input-desktop").querySelector("textarea").value = "";
        refreshComments(article_id);
    }
    else {
        console.error("Failed to post comment");
        const errorMessage = await response.text();
        alert(`Error posting comment: ${errorMessage}. Please try again.`);
    }
}

async function addCommentMobile() {
    const commentText = document.getElementById("comment-input-mobile").querySelector("textarea").value;

    const response = await fetch(`/articles/add_comment/${article_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ content: commentText }),
    });

    if (response.ok) {
        document.getElementById("comment-input-mobile").querySelector("textarea").value = "";
        refreshComments(article_id);
    }
    else {
        console.error("Failed to post comment: ", response.status);
        const errorMessage = await response.text();
        alert(`Error posting comment: ${errorMessage}. Please try again.`);
    }
}

async function colorLike() {
    if (!user.is_anonymous) {
        const has_like = await fetch(`/articles/json/isLikeArticle/${article_id}/`).then(res => res.json());
        if (has_like.is_like) {
            const likeArticleDesktopButton = document.querySelector(".desktop").querySelector(".like-desktop").querySelector(".like-button");
            likeArticleDesktopButton.classList.add("selected");
            likeArticleDesktopButton.classList.remove("text-[#c8c8c8]");
            likeArticleDesktopButton.classList.add("text-[#01aae8]");
            likeArticleDesktopButton.classList.remove("hover:text-[#01aae8]");

            const likeArticleMobile = document.querySelector(".mobile").querySelector(".like-mobile").querySelector(".like-button");
            likeArticleDesktopButton.classList.add("selected");
            likeArticleDesktopButton.classList.remove("text-[#c8c8c8]");
            likeArticleDesktopButton.classList.add("text-[#01aae8]");
            likeArticleDesktopButton.classList.remove("hover:text-[#01aae8]");
        }
        const commentSection = document.querySelector(".desktop").querySelectorAll(".comment");
        if (commentSection) {
            commentSection.forEach(async element => {
               const commentId = element.getAttribute('comment-id');
               const has_like = await fetch(`/articles/json/isLikeComment/${commentId}/`).then(res => res.json());
               if (has_like.is_like) {
                    document.querySelectorAll(`.comment[comment-id=${commentId}]`).forEach(like => {
                        likeButton = like.querySelector(".like-button");
                        likeButton.classList.add("selected");
                        likeButton.classList.remove("text-[#c8c8c8]");
                        likeButton.classList.add("text-[#01aae8]");
                        likeButton.classList.remove("hover:text-[#01aae8]");
                    });
                }
            });
        }
    }
}

function addLikeListener() {
    if (!user.is_anonymous) {
        const likeArticleDesktop = document.querySelector(".desktop").querySelector(".like-desktop");
        const likeArticleMobile = document.querySelector(".mobile").querySelector(".like-mobile");

        likeArticleDesktop.querySelector(".like-button").addEventListener("click", async e => {
            e.preventDefault();
            const has_like = await fetch(`/articles/json/isLikeArticle/${article_id}/`).then(res => res.json());
            await fetch(`/articles/likeArticle/${article_id}/`);
            if (has_like.is_like) {
                const button = likeArticleDesktop.querySelector(".like-button");
                const count = likeArticleDesktop.querySelector(".like-count");
                button.classList.remove("selected");
                button.classList.remove("text-[#01aae8]");
                button.classList.add("text-[#c8c8c8]");
                button.classList.add("hover:text-[#01aae8]");
                count.innerHTML = parseInt(count.innerHTML) - 1;
                likeArticleMobile.querySelector(".like-count").innerHTML = parseInt(likeArticleMobile.querySelector(".like-count").innerHTML) - 1;
            }
            else {
                const count = likeArticleDesktop.querySelector(".like-count");
                const button = likeArticleDesktop.querySelector(".like-button");
                button.classList.add("selected");
                button.classList.remove("text-[#c8c8c8]");
                button.classList.add("text-[#01aae8]");
                button.classList.remove("hover:text-[#01aae8]");
                count.innerHTML = parseInt(count.innerHTML) + 1;
                likeArticleMobile.querySelector(".like-count").innerHTML = parseInt(likeArticleMobile.querySelector(".like-count").innerHTML) + 1;
            }
        });

        likeArticleMobile.querySelector(".like-button").addEventListener("touchend", async e => {
            e.preventDefault();
            const has_like = await fetch(`/articles/json/isLikeArticle/${article_id}/`).then(res => res.json());
            await fetch(`/articles/likeArticle/${article_id}/`);
            if (has_like.is_like) {
                const button = likeArticleMobile.querySelector(".like-button");
                const count = likeArticleMobile.querySelector(".like-count");
                button.classList.remove("selected");
                button.classList.remove("text-[#01aae8]");
                button.classList.add("text-[#c8c8c8]");
                button.classList.add("hover:text-[#01aae8]");
                count.innerHTML = parseInt(count.innerHTML) - 1;
                likeArticleDesktop.querySelector(".like-count").innerHTML = parseInt(likeArticleDesktop.querySelector(".like-count").innerHTML) - 1;
            }
            else {
                const count = likeArticleMobile.querySelector(".like-count");
                const button = likeArticleMobile.querySelector(".like-button");
                button.classList.add("selected");
                button.classList.remove("text-[#c8c8c8]");
                button.classList.add("text-[#01aae8]");
                button.classList.remove("hover:text-[#01aae8]");
                count.innerHTML = parseInt(count.innerHTML) + 1;
                likeArticleDesktop.querySelector(".like-count").innerHTML = parseInt(likeArticleDesktop.querySelector(".like-count").innerHTML) + 1;
            }
        });
        const commentDesktop = document.querySelector(".desktop").querySelectorAll(".comment");
        if (commentDesktop) {
            commentDesktop.forEach((element) => {
                const commentId = element.getAttribute('comment-id');
                element.querySelector(".like-button").addEventListener("click", async e => {
                    e.preventDefault();
                    const has_like = await fetch(`/articles/json/isLikeComment/${commentId}/`).then(res => res.json());
                    await fetch(`/articles/likeComment/${commentId}/`);
                    if (has_like.is_like) {
                        const button = element.querySelector(".like-button");
                        const count = element.querySelector(".like-count");
                        button.classList.remove("selected");
                        button.classList.remove("text-[#01aae8]");
                        button.classList.add("text-[#c8c8c8]");
                        button.classList.add("hover:text-[#01aae8]");
                        count.innerHTML = parseInt(count.innerHTML) - 1;
                    }
                    else {
                        const count = element.querySelector(".like-count");
                        const button = element.querySelector(".like-button");
                        button.classList.add("selected");
                        button.classList.remove("text-[#c8c8c8]");
                        button.classList.add("text-[#01aae8]");
                        button.classList.remove("hover:text-[#01aae8]");
                        count.innerHTML = parseInt(count.innerHTML) + 1;
                    }
                });
            });
        }
        const commentMobile = document.querySelector(".mobile").querySelectorAll(".comment");
        if (commentMobile) {
            commentMobile.forEach((element) => {
                const commentId = element.getAttribute('comment-id');
                element.querySelector(".like-button").addEventListener("touchend", async e => {
                    e.preventDefault();
                    const has_like = await fetch(`/articles/json/isLikeComment/${commentId}/`).then(res => res.json());
                    await fetch(`/articles/likeComment/${commentId}/`);
                    if (has_like.is_like) {
                        const button = element.querySelector(".like-button");
                        const count = element.querySelector(".like-count");
                        button.classList.remove("selected");
                        button.classList.remove("text-[#01aae8]");
                        button.classList.add("text-[#c8c8c8]");
                        button.classList.add("hover:text-[#01aae8]");
                        count.innerHTML = parseInt(count.innerHTML) - 1;
                    }
                    else {
                        const count = element.querySelector(".like-count");
                        const button = element.querySelector(".like-button");
                        button.classList.add("selected");
                        button.classList.remove("text-[#c8c8c8]");
                        button.classList.add("text-[#01aae8]");
                        button.classList.remove("hover:text-[#01aae8]");
                        count.innerHTML = parseInt(count.innerHTML) + 1;
                    }
                });
            });
        }
    }
}

async function start() {
    await refreshComments(article_id);
    addLikeListener();
    colorLike();
}