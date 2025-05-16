document.addEventListener('DOMContentLoaded', function () {
  const ctx = document.getElementById('caloriesburntchart')?.getContext('2d');
  if (!ctx) return; // silently fail

  let chart;


  function fetchAndRender(range) {
    fetch(`/api/calories?range=${range}`)
      .then(res => res.json())
      .then(data => {
        const labels = data.map(entry => {
          const d = new Date(entry.date);

          if (range === 'month') {
            return d.toLocaleDateString('en-AU', { day: '2-digit' });
          } else if (range === 'year') {
            return d.toLocaleDateString('en-AU', { day: '2-digit', month: 'short' });
          } else {
            // 'all' or default — include year for clarity
            return d.toLocaleDateString('en-AU', { day: '2-digit', month: 'short', year: 'numeric' });
          }
        });

        const calories = data.map(entry => entry.calories);

        if (chart) chart.destroy();

        chart = new Chart(ctx, {
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
  }

  fetchAndRender('month');

  document.getElementById('timeRange').addEventListener('change', function () {
    fetchAndRender(this.value);
  });
});


    
