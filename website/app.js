const load = (key, fallback) => JSON.parse(localStorage.getItem(key) || JSON.stringify(fallback));
const save = (key, value) => localStorage.setItem(key, JSON.stringify(value));

let subjects = load('subjects', []);
let tasks    = load('tasks', []);

const subjectForm  = document.getElementById('subjectForm');
const subjectName  = document.getElementById('subjectName');
const subjectList  = document.getElementById('subjectList');
const taskForm     = document.getElementById('taskForm');
const taskSubject  = document.getElementById('taskSubject');
const taskType     = document.getElementById('taskType');
const taskTitle    = document.getElementById('taskTitle');
const taskDue      = document.getElementById('taskDue');
const taskDoneSel  = document.getElementById('taskDone');
const taskList     = document.getElementById('taskList');
const filterSubject= document.getElementById('filterSubject');
const installBtn   = document.getElementById('installBtn');

const statSubjects = document.getElementById('statSubjects');
const statTasks    = document.getElementById('statTasks');
const statDueSoon  = document.getElementById('statDueSoon');
const statDonePct  = document.getElementById('statDonePct');
const typeClass = {
  'Homework': 'badge-homework',
  'Assessment': 'badge-assessment',
  'Study': 'badge-study'
};

function renderSubjects() {
  taskSubject.innerHTML = subjects.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
  filterSubject.innerHTML = `<option value="">All</option>` + subjects.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
  subjectList.innerHTML = subjects.map(s => `
    <li>
      <span>${s.name}</span>
      <button class="remove" data-remove-subject="${s.id}">Delete</button>
    </li>`).join('');
}

function renderTasks() {
  const filter = filterSubject.value;
  const view = filter ? tasks.filter(t => t.subjectId === filter) : tasks;

  taskList.innerHTML = view.sort((a,b)=> (a.due||'').localeCompare(b.due||''))
    .map(t => {
      const subject = subjects.find(s => s.id === t.subjectId)?.name || 'Unknown';
      const due = t.due ? new Date(t.due).toLocaleDateString() : 'No date';
      return `
      <li>
        <div>
          <strong>${t.title}</strong> <span class="badge badge-${t.type.toLowerCase().replace(/\s+/g,'-')}">${t.type}</span>
          <div class="meta">Subject: ${subject} • Due: ${due}</div>
        </div>
        <div>
          <button data-done="${t.id}">${t.done ? '✓ Done' : 'Mark Done'}</button>
          <button class="remove" data-remove-task="${t.id}">Delete</button>
        </div>
      </li>`;
    }).join('');

  renderDashboard();
}

function renderDashboard() {
  statSubjects.textContent = subjects.length;
  statTasks.textContent = tasks.length;
  const now = new Date();
  const soon = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 7);
  const dueSoon = tasks.filter(t => t.due && new Date(t.due) <= soon && !t.done).length;
  statDueSoon.textContent = dueSoon;
  const done = tasks.filter(t => t.done).length;
  statDonePct.textContent = tasks.length ? Math.round((done / tasks.length) * 100) + '%' : '0%';
}

subjectForm.addEventListener('submit', e => {
  e.preventDefault();
  const name = subjectName.value.trim();
  if (!name) return;
  const id = crypto.randomUUID();
  subjects.push({ id, name });
  save('subjects', subjects);
  subjectName.value = '';
  renderSubjects();
  renderTasks();
});

subjectList.addEventListener('click', e => {
  const id = e.target.dataset.removeSubject;
  if (!id) return;
  subjects = subjects.filter(s => s.id !== id);
  tasks = tasks.filter(t => t.subjectId !== id);
  save('subjects', subjects); save('tasks', tasks);
  renderSubjects(); renderTasks();
});

taskForm.addEventListener('submit', e => {
  e.preventDefault();
  if (!subjects.length) return alert('Add a subject first.');
  const id = crypto.randomUUID();
  tasks.push({
    id,
    subjectId: taskSubject.value,
    type: taskType.value,
    title: taskTitle.value.trim(),
    due: taskDue.value || null,
    done: taskDoneSel.value === 'true'
  });
  save('tasks', tasks);
  taskTitle.value = ''; taskDue.value = ''; taskDoneSel.value = 'false';
  renderTasks();
});

taskList.addEventListener('click', e => {
  const doneId = e.target.dataset.done;
  const removeId = e.target.dataset.removeTask;
  if (doneId) {
    const t = tasks.find(x => x.id === doneId);
    if (t) t.done = !t.done;
    save('tasks', tasks);
    renderTasks();
  }
  if (removeId) {
    tasks = tasks.filter(t => t.id !== removeId);
    save('tasks', tasks);
    renderTasks();
  }
});

filterSubject.addEventListener('change', renderTasks);

let deferredPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  installBtn.hidden = false;
});
installBtn.addEventListener('click', async () => {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  await deferredPrompt.userChoice;
  installBtn.hidden = true;
});

renderSubjects();
renderTasks();
