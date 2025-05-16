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
  const rangeSelector = document.getElementById('compareTimeRange');
  let chartInstance;

  cards.forEach(card => {
    card.addEventListener('click', () => {
      const friend = card.dataset.username;
      const range = rangeSelector?.value || 'month';

      fetch(`/api/calories?friend=${friend}&range=${range}`)
        .then(res => res.json())
        .then(data => {
          if (data.error) {
            console.error("API error:", data.error);
            return;
          }

          const userData = data.user;
          const friendData = data.friend;

          // Generate labels using appropriate format based on range
          const labels = userData.map(entry => {
            const d = new Date(entry.date);
            if (range === 'month') {
              return d.toLocaleDateString('en-AU', { day: '2-digit' });
            } else if (range === 'year') {
              return d.toLocaleDateString('en-AU', { day: '2-digit', month: 'short' });
            } else {
              return d.toLocaleDateString('en-AU', { day: '2-digit', month: 'short', year: 'numeric' });
            }
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

  // Re-fetch data if time range changes
  if (rangeSelector) {
    rangeSelector.addEventListener('change', () => {
      const activeFriendCard = document.querySelector('.friend-row[data-username="' + nameDisplay.textContent + '"]');
      if (activeFriendCard) {
        activeFriendCard.click(); // re-trigger chart for current friend
      }
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
