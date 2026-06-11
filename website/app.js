const load = (key, fallback) => JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback));
const save = (key, value) => localStorage.setItem(key, JSON.stringify(value));

let tasks = load('tasks', []);

const taskForm = document.getElementById('taskForm');
const taskTitle = document.getElementById('UserAbsence');
const taskType = document.getElementById('taskType');
const taskDue = document.getElementById('absentDate');
const taskDoneSel = document.getElementById('proof');
const taskYear = document.getElementById('yearLevel');
const taskList = document.getElementById('taskList');
const installBtn = document.getElementById('installBtn');

const statSubjects = document.getElementById('statSubjects');
const statTasks = document.getElementById('statTasks');
const statDueSoon = document.getElementById('statDueSoon');
const statDonePct = document.getElementById('statDonePct');

function renderTasks() {
  taskList.innerHTML = tasks
    .sort((a, b) => (a.due || '').localeCompare(b.due || ''))
    .map(task => {
      const due = task.due ? new Date(task.due).toLocaleDateString() : 'No date';
      return `
      <li>
        <div>
          <strong>${task.title}</strong>
          <div>Type: ${task.type}</div>
          <div>Year level: ${task.yearLevel}</div>
          <div>Date: ${due}</div>
          <div>Proof: ${task.proof ? 'Yes' : 'No'}</div>
        </div>
        <div>
          <button class="remove" data-remove-task="${task.id}">Delete</button>
        </div>
      </li>`;
    })
    .join('');

  const total = tasks.length;
  const unexplained = tasks.filter(t => !t.proof).length;
  const explained = tasks.filter(t => t.proof).length;
  const attendancePct = total ? Math.round(((total - unexplained) / total) * 100) : 0;

  statSubjects.textContent = total;
  statTasks.textContent = unexplained;
  statDueSoon.textContent = explained;
  statDonePct.textContent = `${attendancePct}%`;
}

taskForm.addEventListener('submit', e => {
  e.preventDefault();
  const title = taskTitle.value.trim();
  if (!title) return;

  const id = crypto.randomUUID();
  const item = {
    id,
    title,
    type: taskType.value,
    yearLevel: taskYear.value,
    due: taskDue.value || null,
    proof: taskDoneSel.value === 'true'
  };

  tasks.push(item);
  save('tasks', tasks);
  taskTitle.value = '';
  taskDue.value = '';
  taskDoneSel.value = 'false';
  renderTasks();
});

taskList.addEventListener('click', e => {
  const removeId = e.target.dataset.removeTask;
  if (!removeId) return;
  tasks = tasks.filter(task => task.id !== removeId);
  save('tasks', tasks);
  renderTasks();
});

let deferredPrompt = null;
window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault();
  deferredPrompt = e;
  if (installBtn) installBtn.hidden = false;
});

if (installBtn) {
  installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    await deferredPrompt.userChoice;
    installBtn.hidden = true;
  });
}

renderTasks();
