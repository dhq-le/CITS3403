document.addEventListener("DOMContentLoaded", async function () {
  const form = document.querySelector("form");
  const muscleSelect = document.querySelector("select[name='muscle']");
  const heading = document.getElementById("exercise-heading");

  try {
    const response = await fetch("/static/data/exercise.json");
    if (!response.ok) {
      throw new Error(`Failed to load JSON file: ${response.status}`);
    }
    const allData = await response.json();
    // Populate the dropdown
    Object.keys(allData).forEach(muscle => {
      const option = document.createElement("option");
      option.value = muscle;
      option.textContent = muscle.charAt(0).toUpperCase() + muscle.slice(1);
      muscleSelect.appendChild(option);
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const muscleId = muscleSelect.value;
      const data = allData[muscleId] || [];

      heading.textContent = `Exercises for ${muscleId.charAt(0).toUpperCase() + muscleId.slice(1)}`;
      const container = document.querySelector("#exercise-list");
      container.innerHTML = ""; // Clear previous results
      data.forEach(exercise => {
        const card = document.createElement("div");
        card.className = "exercise-card";

        const detailDiv = document.createElement("div");
        detailDiv.className = "exercise-details";
        detailDiv.innerHTML = `
          <strong>${exercise.name ?? 'Unnamed Exercise'}</strong><br>
          <em>Equipment:</em> ${exercise.equipment ?? 'N/A'}<br>
          <em>Calories/min:</em> ${exercise.calories_burned_per_min ?? 'N/A'}<br>
          <em>Details:</em> ${exercise.details ?? 'No description available.'}
        `;
        
        // since there is no gifs available, we will use images but switch them in a short period to illustrate a gif.
        if (Array.isArray(exercise.image) && exercise.image.length > 0) {
          const img = document.createElement("img");
          img.src = exercise.image[0];
          img.alt = exercise.name;
          let i = 0;
          setInterval(() => {
            i = (i + 1) % exercise.image.length;
            img.src = exercise.image[i];
          }, 700);
          card.appendChild(img);
        }

        card.appendChild(detailDiv);
        container.appendChild(card);
      });
    });
  } catch (error) {
    console.error("Fetch error:", error);
    const debug = document.querySelector("#debug-message");
    if (debug) {
      debug.textContent = "Something went wrong. See console for details.";
    }
  }
});