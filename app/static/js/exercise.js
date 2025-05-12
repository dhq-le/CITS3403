document.addEventListener("DOMContentLoaded", async function () {
  const form = document.querySelector("form");
  const muscleSelect = document.querySelector("select[name='muscle']");
  const heading = document.getElementById("exercise-heading");

  try {
    const response = await fetch("/static/data/exercises.json");
    if (!response.ok) {
      throw new Error(`Failed to load JSON file: ${response.status}`);
    }
    const allData = await response.json();
    // Populate the dropdown with the group of muscle names
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
        const card = document.createElement("section");
        card.className = "card";

        // Create card header
        const header = document.createElement("div");
        header.className = "card-header";
        header.innerHTML = `<a href="/log?exercise=${encodeURIComponent(exercise.name)}" class="card-header-link"><h2>${exercise.name ?? 'Unnamed Exercise'}</h2></a>`;
        card.appendChild(header);

        // Create card body
        const body = document.createElement("div");
        body.className = "card-body";
        
        // since there is no gifs available, we will use images but switch them in a short period to illustrate a gif.
        if (Array.isArray(exercise.image) && exercise.image.length > 0) {
          const img = document.createElement("img");
          img.src = exercise.image[0];
          img.alt = exercise.name;
          img.className = "card-img";
          let i = 0;
          setInterval(() => {
            i = (i + 1) % exercise.image.length;
            img.src = exercise.image[i];
          }, 700);
          body.appendChild(img);
        }

        // Build details list
        const detailsList = document.createElement("ul");
        detailsList.innerHTML = `
          <li><strong>Equipment:</strong> ${exercise.equipment ?? 'N/A'}</li>
          <li><strong>Calories/rep:</strong> ${exercise.calories_burned_per_rep ?? 'N/A'}</li>
          <li><strong>Details:</strong> ${exercise.details ?? 'No description available.'}</li>
        `;
        body.appendChild(detailsList);

        card.appendChild(body);
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

        