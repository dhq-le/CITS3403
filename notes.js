document.addEventListener('DOMContentLoaded', () => {
    const noteList = document.querySelector('.note-list');
  
    // Simulate data loading delay
    setTimeout(() => {
      // Replace skeleton with real content
      noteList.classList.remove('skeleton');
      noteList.innerHTML = `
        <p>Attitude and committed to lifting and cardio daily</p>
        <p>Inspiring others in the gym</p>`;
  
      // Now reattach the event listener to the new Add Note button
      const addNoteBtn = noteList.querySelector('button');
      const noteTextarea = noteList.querySelector('textarea');
  
      addNoteBtn.addEventListener('click', () => {
        const note = noteTextarea.value.trim();
        if (note !== '') {
          const p = document.createElement('p');
          p.textContent = note;
          noteList.insertBefore(p, noteTextarea);
          noteTextarea.value = '';
        }
      });
    }, 3000); // 1.5 second fake loading
  });