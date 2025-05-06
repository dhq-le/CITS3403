document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const muscleId = document.querySelector("select[name='muscle']").value;

    try {
      const response = await fetch("/api/start_course", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("input[name='csrf_token']").value
        },
        body: JSON.stringify({ muscle_id: muscleId })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      const list = document.querySelector("#exercise-list");
      list.innerHTML = "";

      if (Array.isArray(data.exercises) && data.exercises.length > 0) {
        data.exercises.forEach(ex => {
          const item = document.createElement("li");
          item.innerHTML = `
            <strong>${ex.name ?? 'Unnamed exercise'}</strong><br>
            ${ex.instructions?.trim() || 'No instructions available.'}
          `;
          list.appendChild(item);
        });
      } else {
        const item = document.createElement("li");
        item.textContent = "No exercises found for this muscle group.";
        list.appendChild(item);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      const debug = document.querySelector("#debug-message");
      if (debug) {
        debug.textContent = "Something went wrong. See console for details.";
      }
    }
  });
});