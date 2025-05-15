function deleteWorkout(workoutId) {
	if (!confirm("Are you sure you want to delete this workout?")) return;

	fetch(`/delete_workout/${workoutId}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': '{{ csrf_token() }}'  // Only if CSRF protection is enabled
		}
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			const card = document.getElementById(`workout-${workoutId}`);
			if (card) {
				// Optional fade out animation
				card.style.transition = 'opacity 0.5s ease';
				card.style.opacity = 0;
				setTimeout(() => card.remove(), 500);
			}
		} else {
			alert("Error deleting workout: " + (data.error || "Unknown error"));
		}
	})
	.catch(err => {
		console.error("Delete failed", err);
		alert("Error sending delete request.");
	});
}