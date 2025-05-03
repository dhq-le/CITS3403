

document.addEventListener('DOMContentLoaded', () => {
  const listContainer = document.querySelector('.friends-list');
  const messageContainer = document.querySelector('#friends-list .card-body p');

  // Fetch friends data from a JSON endpoint
  fetch('/api/friends')
    .then(response => {
      if (!response.ok) {
        throw new Error(`Network response was not OK (${response.status})`);
      }
      return response.json();
    })
    .then(data => {
      // Clear any placeholder message
      if (messageContainer) {
        messageContainer.textContent = '';
      }
      // Populate list
      data.forEach(friend => {
        const li = document.createElement('li');
        li.className = 'friend-entry';
        li.textContent = friend.friend_username;
        listContainer.appendChild(li);
      });
      // If no friends, show the "no friends" message
      if (data.length === 0 && messageContainer) {
        messageContainer.textContent = 'You have no friends yet.';
      }
    })
    .catch(error => {
      console.error('Error fetching friends:', error);
      if (messageContainer) {
        messageContainer.textContent = 'Error loading friends.';
      }
    });
});