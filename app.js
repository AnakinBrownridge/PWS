const windows = [
  { id: 'browser', title: 'Browser', priority: 100, accent: 'accent', active: true },
  { id: 'terminal', title: 'Terminal', priority: 78, accent: 'warm' },
  { id: 'editor', title: 'Editor', priority: 82, accent: 'accent' },
  { id: 'notes', title: 'Notes', priority: 65, accent: 'warm' },
  { id: 'media', title: 'Media', priority: 58, accent: 'accent' }
];

const workspace = document.getElementById('workspace');

function renderWindow(windowData) {
  const el = document.createElement('article');
  el.className = `window ${windowData.active ? 'active' : ''}`;
  el.setAttribute('data-window', windowData.id);

  const content = `
    <div class="window-titlebar">
      <div class="window-controls">
        <span class="dot red"></span>
        <span class="dot yellow"></span>
        <span class="dot green"></span>
      </div>
      <span class="window-label">${windowData.title}</span>
    </div>
    <div class="window-body">
      <div class="window-content">
        <div class="row">
          <div class="box big ${windowData.accent}"></div>
          <div class="box big"></div>
        </div>
        <div class="row">
          <div class="box small"></div>
          <div class="box small warm"></div>
        </div>
        <div class="row">
          <div class="box small accent"></div>
          <div class="box small"></div>
        </div>
      </div>
    </div>
  `;

  el.innerHTML = content;
  return el;
}

function arrangeWindows() {
  const workspaceRect = workspace.getBoundingClientRect();
  const width = workspaceRect.width;
  const height = workspaceRect.height;

  const ordered = [...windows].sort((a, b) => b.priority - a.priority);
  const primary = ordered[0];
  const secondary = ordered.slice(1, 3);
  const tertiary = ordered.slice(3);

  const layouts = {
    primary: { x: 0.024, y: 0.04, w: 0.56, h: 0.9 },
    secondaryA: { x: 0.6, y: 0.04, w: 0.36, h: 0.46 },
    secondaryB: { x: 0.6, y: 0.54, w: 0.36, h: 0.42 },
    tertiaryA: { x: 0.024, y: 0.6, w: 0.34, h: 0.34 },
    tertiaryB: { x: 0.38, y: 0.6, w: 0.2, h: 0.34 }
  };

  const queue = [primary, ...(secondary || []), ...(tertiary || [])];

  queue.forEach((item, index) => {
    const element = workspace.querySelector(`[data-window="${item.id}"]`) || renderWindow(item);

    if (!element.parentNode) {
      workspace.appendChild(element);
    }

    let position = layouts.primary;

    if (index === 1) position = layouts.secondaryA;
    if (index === 2) position = layouts.secondaryB;
    if (index === 3) position = layouts.tertiaryA;
    if (index === 4) position = layouts.tertiaryB;

    element.style.left = `${position.x * width}px`;
    element.style.top = `${position.y * height}px`;
    element.style.width = `${position.w * width}px`;
    element.style.height = `${position.h * height}px`;
  });
}

workspace.innerHTML = '';
arrangeWindows();
window.addEventListener('resize', arrangeWindows);

setInterval(() => {
  const current = windows[0];
  windows.push(windows.shift());
  windows.forEach((windowData, index) => {
    windowData.active = index === 0;
  });

  const nextFocus = windows[0];
  const primary = workspace.querySelector('[data-window="' + current.id + '"]');
  const focusWindow = workspace.querySelector('[data-window="' + nextFocus.id + '"]');

  if (primary) primary.classList.remove('active');
  if (focusWindow) focusWindow.classList.add('active');

  arrangeWindows();
}, 5000);



















































































































































