console.log("scripts.js jest załadowany i działa");

// Funkcja do śledzenia użytkownika
function followUser(event) {
    console.log("Follow button clicked"); // Dodaj log

    const userId = event.target.getAttribute("data-user-id");
    console.log("User ID (Follow):", userId);

    fetch(`/follow/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log("Follow response:", data);

        if (data.message) {
            const followButton = event.target;
            followButton.style.display = "none";
            const unfollowButton = followButton.nextElementSibling;
            unfollowButton.style.display = "inline-block";

            const followersCount = document.getElementById('followers-count');
            const followingCount = document.getElementById('following-count');
            
            if (followersCount) followersCount.innerText = data.followers_count;
            if (followingCount) followingCount.innerText = data.following_count;
        } else {
            console.error("No message in response", data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Funkcja do przestania śledzenia użytkownika
function unfollowUser(event) {
    console.log("Unfollow button clicked");

    const userId = event.target.getAttribute("data-user-id");
    console.log("User ID (Unfollow):", userId);

    fetch(`/unfollow/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log("Unfollow response:", data);

        if (data.message) {
            const unfollowButton = event.target;
            unfollowButton.style.display = "none";
            const followButton = unfollowButton.previousElementSibling;
            followButton.style.display = "inline-block";

            const followersCount = document.getElementById('followers-count');
            const followingCount = document.getElementById('following-count');
            
            if (followersCount) followersCount.innerText = data.followers_count;
            if (followingCount) followingCount.innerText = data.following_count;
        } else {
            console.error("No message in response", data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Nasłuchiwanie na kliknięcia przycisków Follow/Unfollow
document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM załadowany");

    // Przycisk Follow
    const followButtons = document.querySelectorAll(".follow-btn");
    followButtons.forEach(button => {
        console.log("Nasłuchuję na follow button");
        button.addEventListener("click", followUser);
    });

    // Przycisk Unfollow
    const unfollowButtons = document.querySelectorAll(".unfollow-btn");
    unfollowButtons.forEach(button => {
        console.log("Nasłuchuję na unfollow button");
        button.addEventListener("click", unfollowUser);
    });

    // ★★★ Nowa funkcja: Like/Unlike
    const likeButtons = document.querySelectorAll(".like-button");
    likeButtons.forEach(button => {
        button.addEventListener("click", () => {
            const postId = button.dataset.postId;

            fetch(`/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                // Aktualizacja liczby lajków
                const likesCounter = document.querySelector(`#likes-count-${postId}`);
                if (likesCounter) likesCounter.innerText = data.total_likes;

                // Zmieniamy tekst przycisku
                button.innerText = data.liked ? 'Unlike' : 'Like';
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

// Funkcja do pobrania CSRF cookie (standard Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
