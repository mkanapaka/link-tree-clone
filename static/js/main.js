document.addEventListener('DOMContentLoaded', () => {
    const profilePicture = document.getElementById('profile-picture');
    const fileInput = document.getElementById('profile_picture');
    const form = document.getElementById('profile-picture-form');
    
    if (!profilePicture.src || profilePicture.src.endsWith('default.jpg')) {
        // Fetch a random image from Unsplash only if no profile picture is set
        fetch('https://source.unsplash.com/random/300x300')
            .then(response => {
                profilePicture.src = response.url;
            })
            .catch(error => {
                console.error('Error fetching profile picture:', error);
                // Use a default image if fetching fails
                profilePicture.src = 'https://via.placeholder.com/300';
            });
    }

    // Add event listener to file input
    fileInput.addEventListener('change', (event) => {
        if (event.target.files.length > 0) {
            // Automatically submit the form when a file is selected
            form.submit();
        }
    });
});
