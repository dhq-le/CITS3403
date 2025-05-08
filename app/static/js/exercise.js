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
      const list = document.querySelector("#exercise-list");
      list.innerHTML = ""; // Clear previous results
      data.forEach(exercise => {
        const li = document.createElement("li");
        li.innerHTML = `
          <strong>${exercise.name ?? 'Unnamed Exercise'}</strong><br>
          <em>Equipment:</em> ${exercise.equipment ?? 'N/A'}<br>
          <em>Calories/min:</em> ${exercise.calories_burned_per_min ?? 'N/A'}<br>
          <em>Details:</em> ${exercise.details ?? 'No description available.'}
        `;
        list.appendChild(li);
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