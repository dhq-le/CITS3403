document.addEventListener('DOMContentLoaded', function () {
  // Focus on add friend input
  const input = document.querySelector('.friend-input');
  if (input) input.focus();

  // Fade out all flash messages after 5 seconds
  const flashes = document.querySelectorAll('.flash');
  if (flashes.length) {
    setTimeout(() => {
      flashes.forEach(el => el.classList.add('fade-out'));
    }, 5000);
  }

  // Chart Overlay Logic
  const cards = document.querySelectorAll('.friend-row');
  const overlay = document.getElementById('comparisonOverlay');
  const closeBtn = document.getElementById('closeOverlay');
  const nameDisplay = document.getElementById('friendNameDisplay');
  const ctx = document.getElementById('comparisonChart');
  let chartInstance;

  cards.forEach(card => {
    card.addEventListener('click', () => {
      const friend = card.dataset.username;

      fetch(`/api/calories?friend=${friend}`)
        .then(res => res.json())
        .then(data => {
          if (data.error) {
            console.error("API error:", data.error);
            return;
          }

          const userData = data.user;
          const friendData = data.friend;

          const labels = userData.map(entry => {
            const d = entry.date;
            return `${d.slice(6, 8)}/${d.slice(4, 6)}`;
          });

          const userCalories = userData.map(e => e.calories);
          const friendCalories = friendData.map(e => e.calories);

          if (chartInstance) {
            chartInstance.destroy();
          }

          chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
              labels: labels,
              datasets: [
                {
                  label: "You",
                  data: userCalories,
                  borderColor: 'rgb(75, 192, 192)',
                  tension: 0.2
                },
                {
                  label: friend,
                  data: friendCalories,
                  borderColor: "rgb(192, 42, 75)",
                  tension: 0.2
                }
              ]
            },
            options: {
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });

          nameDisplay.textContent = friend;
          overlay.classList.add('active');
        });
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      overlay.classList.remove('active');
    });
  }

  // Add Friend Modal Logic
  const openBtn = document.getElementById('openAddFriendModal');
  const modal = document.getElementById('addFriendModal');
  const closeModalBtn = document.getElementById('closeAddFriendModal');

  if (openBtn && modal && closeModalBtn) {
    openBtn.onclick = () => {
      modal.classList.add('active');
    };
    closeModalBtn.onclick = () => {
      modal.classList.remove('active');
    };
    window.onclick = (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
      }
    };
  }
});
