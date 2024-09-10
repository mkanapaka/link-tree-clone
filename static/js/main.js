document.addEventListener('DOMContentLoaded', () => {
    const profilePicture = document.getElementById('profile-picture');
    
    // Fetch a random image from Unsplash
    fetch('https://source.unsplash.com/random/300x300')
        .then(response => {
            profilePicture.src = response.url;
        })
        .catch(error => {
            console.error('Error fetching profile picture:', error);
            // Use a default image if fetching fails
            profilePicture.src = 'https://via.placeholder.com/300';
        });
});
