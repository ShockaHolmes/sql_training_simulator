let currentLesson = null;

const sqlInput = document.getElementById('sql-input');
const feedback = document.getElementById('feedback');
const resultTable = document.getElementById('result-table');

function setFeedback(message, kind = '') {
  feedback.textContent = message;
  feedback.className = `feedback ${kind}`;
}

function renderTable(result) {
  resultTable.innerHTML = '';
  if (!result.ok) return;
  const thead = document.createElement('thead');
  const header = document.createElement('tr');
  result.columns.forEach(col => {
    const th = document.createElement('th');
    th.textContent = col;
    header.appendChild(th);
  });
  thead.appendChild(header);
  resultTable.appendChild(thead);

  const tbody = document.createElement('tbody');
  result.rows.forEach(row => {
    const tr = document.createElement('tr');
    result.columns.forEach(col => {
      const td = document.createElement('td');
      td.textContent = row[col] ?? '';
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  resultTable.appendChild(tbody);
}

function loadLesson(lesson) {
  currentLesson = lesson;
  document.getElementById('lesson-title').textContent = `${lesson.id}. ${lesson.title}`;
  const level = document.getElementById('lesson-level');
  level.textContent = lesson.level;
  level.className = `level ${lesson.level}`;
  document.getElementById('lesson-story').textContent = lesson.story;
  document.getElementById('lesson-goal').textContent = lesson.goal;
  document.getElementById('lesson-hint').textContent = lesson.hint;
  const steps = document.getElementById('lesson-steps');
  steps.innerHTML = '';
  lesson.steps.forEach(step => {
    const li = document.createElement('li');
    li.textContent = step;
    steps.appendChild(li);
  });
  sqlInput.value = lesson.starter_sql;
  document.getElementById('lesson-audio').hidden = true;
  setFeedback('Run the starter query, then improve it to match the goal.');
}

document.querySelectorAll('.lesson-card').forEach(button => {
  button.addEventListener('click', () => loadLesson(JSON.parse(button.dataset.lesson)));
});

document.getElementById('run-btn').addEventListener('click', async () => {
  const response = await fetch('/api/run', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({sql: sqlInput.value})
  });
  const result = await response.json();
  if (result.ok) {
    setFeedback(`Query succeeded. ${result.row_count} row(s) returned.`, 'good');
    renderTable(result);
  } else {
    resultTable.innerHTML = '';
    setFeedback(`Error: ${result.error} Hint: ${result.hint}`, 'bad');
  }
});

document.getElementById('check-btn').addEventListener('click', async () => {
  if (!currentLesson) {
    setFeedback('Choose a lesson before checking your answer.', 'bad');
    return;
  }
  const response = await fetch('/api/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({lesson_id: currentLesson.id, sql: sqlInput.value})
  });
  const result = await response.json();
  if (result.passed) {
    setFeedback(result.earned?.length ? `${result.message} New badge: ${result.earned.map(b => b.name).join(', ')}` : result.message, 'good');
    document.getElementById('completed-count').textContent = result.progress.completed.length;
    document.getElementById('xp-count').textContent = result.progress.xp;
  } else {
    setFeedback(result.message, 'bad');
  }
});

document.getElementById('audio-btn').addEventListener('click', async () => {
  if (!currentLesson) {
    setFeedback('Choose a lesson before using audio.', 'bad');
    return;
  }
  setFeedback('Requesting lesson audio...');
  const response = await fetch('/api/audio', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({lesson_id: currentLesson.id})
  });
  const result = await response.json();
  if (!result.ok) {
    setFeedback(result.message, 'bad');
    return;
  }
  const audio = document.getElementById('lesson-audio');
  audio.src = `data:${result.mime_type};base64,${result.audio_base64}`;
  audio.hidden = false;
  audio.play();
  setFeedback('Audio lesson ready.', 'good');
});

document.getElementById('reset-db').addEventListener('click', async () => {
  await fetch('/api/reset-db', {method: 'POST'});
  setFeedback('Database reset. Run your query again.', 'good');
});

const firstLesson = document.querySelector('.lesson-card');
if (firstLesson) loadLesson(JSON.parse(firstLesson.dataset.lesson));
