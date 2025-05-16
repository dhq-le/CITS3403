document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/calories')
      .then(res => res.json())
      .then(data => {
        const labels = data.map(entry => {
          const d = entry.date;
          return `${d.slice(6, 8)}/${d.slice(4, 6)}`;
        });
        const calories = data.map(entry => entry.calories);
  
        new Chart(document.getElementById('caloriesburntchart'), {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Calories Burnt',
              data: calories,
              fill: false,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.2
            }]
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
      });
  });
  
