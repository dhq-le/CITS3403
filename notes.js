document.addEventListener('DOMContentLoaded', () => {
  const noteList = document.getElementById('note-list');
  const noteInput = document.getElementById('note-input');
  const addNoteBtn = document.getElementById('add-note-btn');

  // Simulate data loading delay
  setTimeout(() => {
    noteList.classList.remove('skeleton');
    noteList.innerHTML = `
      <p>Attitude and committed to lifting and cardio daily</p>
      <p>Inspiring others in the gym</p>
    `;
  }, 3000); // Simulate 3 seconds delay

  // Add new note on button click
  addNoteBtn.addEventListener('click', () => {
    const note = noteInput.value.trim();
    if (note !== '') {
      const p = document.createElement('p');
      p.textContent = note;
      noteList.appendChild(p);
      noteInput.value = '';
    }
  });
});