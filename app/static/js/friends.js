document.addEventListener('DOMContentLoaded', function () {
  // 聚焦到添加好友输入框
  var input = document.querySelector('.friend-input');
  if (input) input.focus();

  // 5秒后淡出所有 flash
  var flashes = document.querySelectorAll('.flash');
  if (flashes.length) {
    setTimeout(function () {
      flashes.forEach(function (el) {
        el.classList.add('fade-out');
      });
    }, 5000);
  }

  const cards = document.querySelectorAll('.friend-card');
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

          const ctx = document.getElementById('comparisonChart');
          if (!ctx) {
            console.error("Comparison chart not found");
            return;
          }

          new Chart(ctx, {
            type: 'line',
            data: {
              labels: labels,
              datasets: [
                {
                  label: "You",
                  data: userCalories,
                  borderColor: "blue",
                  tension: 0.2
                },
                {
                  label: friend,
                  data: friendCalories,
                  borderColor: "red",
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

          document.getElementById('comparison-graph-section').style.display = 'block';
        });
    });
  });
});
