# UI/UX Pro Max Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `templates/index.html` with a "Midnight Studio" design: glassmorphism cells, SVG stroke-draw animations, result modal with confetti, turn indicator pills, and full accessibility — while preserving all backend API behavior.

**Architecture:** Single file (`templates/index.html`) with all CSS and JS inline. No external dependencies except Google Fonts (Inter). Each task produces a working, runnable app state committed to git.

**Tech Stack:** HTML5, CSS3 (custom properties, backdrop-filter, keyframe animations), vanilla JS (fetch, DOM), Flask session (server-side board, unchanged).

---

## File Structure

| Action | Path | Responsibility |
|---|---|---|
| Modify | `templates/index.html` | Full rewrite: HTML structure, inline CSS, inline JS |
| No change | `app.py` | Backend unchanged |

All 8 tasks modify only `templates/index.html`. Each task is a complete, additive step — the app is runnable after every commit.

---

## Running the App (reference)

```bash
pip install flask
python app.py
# Open http://127.0.0.1:5000
```

---

## Task 1: Foundation — HTML skeleton, CSS tokens, title

**Files:**
- Modify: `templates/index.html` (replace entire file)

- [ ] **Step 1: Replace `templates/index.html` with the foundation skeleton**

This sets up CSS custom properties, Inter font, base layout, and gradient title. All other tasks will add components inside `<div class="app">` and CSS/JS blocks.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Tic-Tac-Toe</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg:           #0d0d14;
      --surface:      rgba(255, 255, 255, 0.04);
      --border:       rgba(255, 255, 255, 0.08);
      --accent-x:     #7c3aed;
      --accent-o:     #06b6d4;
      --accent-x-glow: rgba(124, 58, 237, 0.35);
      --accent-o-glow: rgba(6, 182, 212, 0.35);
      --text-primary: #f1f5f9;
      --text-muted:   #64748b;
      --radius-cell:  16px;
      --radius-pill:  100px;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: var(--bg);
      font-family: 'Inter', 'Segoe UI', sans-serif;
      color: var(--text-primary);
      padding: 1.5rem;
    }

    .app {
      width: 100%;
      max-width: 420px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1.4rem;
    }

    h1 {
      font-size: clamp(1.5rem, 5vw, 2rem);
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      background: linear-gradient(135deg, var(--accent-x) 0%, var(--accent-o) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .sr-only {
      position: absolute;
      width: 1px; height: 1px;
      padding: 0; margin: -1px;
      overflow: hidden;
      clip: rect(0,0,0,0);
      white-space: nowrap;
      border: 0;
    }
  </style>
</head>
<body>
  <div class="app">
    <h1>Tic&#8209;Tac&#8209;Toe</h1>
    <!-- components added in Tasks 2–8 -->
  </div>

  <div aria-live="assertive" class="sr-only" id="announce"></div>

  <script>
    // JS added in Tasks 2–8
  </script>
</body>
</html>
```

- [ ] **Step 2: Verify in browser**

Run `python app.py`, open `http://127.0.0.1:5000`.  
Expected: Black page, gradient "TIC‑TAC‑TOE" title centered. No console errors.

- [ ] **Step 3: Commit**

```bash
git add templates/index.html
git commit -m "feat: foundation — CSS tokens, Inter font, base layout"
```

---

## Task 2: Mode Toggle (segmented control)

**Files:**
- Modify: `templates/index.html` — add CSS block, HTML block, JS function

- [ ] **Step 1: Add CSS for the segmented toggle**

Inside `<style>`, append after the `.sr-only` rule:

```css
/* ── Mode Toggle ── */
.mode-toggle {
  position: relative;
  display: flex;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  padding: 4px;
  gap: 0;
}

.mode-option {
  position: relative;
  z-index: 1;
  flex: 1;
  padding: 0.45rem 1.2rem;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: color 0.2s;
  white-space: nowrap;
}

.mode-option[aria-checked="true"] { color: var(--text-primary); }

.mode-pill {
  position: absolute;
  top: 4px; bottom: 4px; left: 4px;
  width: calc(50% - 4px);
  background: rgba(124, 58, 237, 0.25);
  border: 1px solid var(--accent-x);
  border-radius: var(--radius-pill);
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  pointer-events: none;
}

.mode-pill.right { transform: translateX(100%); }
```

- [ ] **Step 2: Add HTML for the toggle**

Inside `<div class="app">`, after `<h1>`:

```html
<div class="mode-toggle" role="radiogroup" aria-label="Game mode">
  <button class="mode-option" role="radio" aria-checked="true" id="pvp-btn" onclick="setMode('pvp')">2 Players</button>
  <button class="mode-option" role="radio" aria-checked="false" id="ai-btn" onclick="setMode('ai')">vs AI</button>
  <div class="mode-pill" id="mode-pill"></div>
</div>
```

- [ ] **Step 3: Add JS for mode switching**

Inside `<script>`:

```javascript
let mode = 'pvp';

function setMode(m) {
  mode = m;
  const pvpBtn = document.getElementById('pvp-btn');
  const aiBtn  = document.getElementById('ai-btn');
  const pill   = document.getElementById('mode-pill');
  pvpBtn.setAttribute('aria-checked', m === 'pvp');
  aiBtn.setAttribute('aria-checked',  m === 'ai');
  pill.classList.toggle('right', m === 'ai');
  const oLabel = document.getElementById('o-label');
  const oBadgeLabel = document.getElementById('badge-o-label');
  if (oLabel)       oLabel.textContent      = m === 'ai' ? 'AI' : 'Player O';
  if (oBadgeLabel)  oBadgeLabel.textContent = m === 'ai' ? 'AI' : 'Player O';
  reset();
}
```

- [ ] **Step 4: Verify in browser**

Expected:
- Segmented control renders with "2 Players" selected (violet pill on left).
- Clicking "vs AI" slides pill to the right smoothly.
- Clicking "2 Players" slides it back.
- No console errors.

- [ ] **Step 5: Commit**

```bash
git add templates/index.html
git commit -m "feat: mode toggle segmented control with sliding pill"
```

---

## Task 3: Scoreboard (glass cards with pop animation)

**Files:**
- Modify: `templates/index.html` — add CSS, HTML, JS

- [ ] **Step 1: Add CSS for scoreboard**

Append inside `<style>`:

```css
/* ── Scoreboard ── */
.scoreboard {
  display: flex;
  gap: 0.75rem;
  width: 100%;
}

.score-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  padding: 0.75rem 0.5rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.score-label {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.score-value {
  font-size: 1.8rem;
  font-weight: 700;
  line-height: 1;
  transition: transform 0.15s;
}

.score-card.x  .score-value { color: var(--accent-x); }
.score-card.draw .score-value { color: var(--text-muted); }
.score-card.o  .score-value { color: var(--accent-o); }

@keyframes scorePop {
  0%   { transform: scale(1); }
  40%  { transform: scale(1.45); }
  100% { transform: scale(1); }
}

.score-value.pop { animation: scorePop 0.22s ease-out forwards; }
```

- [ ] **Step 2: Add HTML for scoreboard**

Inside `<div class="app">`, after the mode toggle:

```html
<div class="scoreboard" role="region" aria-label="Scores">
  <div class="score-card x">
    <div class="score-label" id="x-label">Player X</div>
    <div class="score-value" id="score-x" aria-live="polite">0</div>
  </div>
  <div class="score-card draw">
    <div class="score-label">Draws</div>
    <div class="score-value" id="score-draw" aria-live="polite">0</div>
  </div>
  <div class="score-card o">
    <div class="score-label" id="o-label">Player O</div>
    <div class="score-value" id="score-o" aria-live="polite">0</div>
  </div>
</div>
```

- [ ] **Step 3: Add JS for score tracking and pop animation**

Inside `<script>`, after the mode variable:

```javascript
let scores = { X: 0, O: 0, draw: 0 };

function popScore(el) {
  el.classList.remove('pop');
  void el.offsetWidth; // force reflow to restart animation
  el.classList.add('pop');
  el.addEventListener('animationend', () => el.classList.remove('pop'), { once: true });
}

function updateScores() {
  const sx    = document.getElementById('score-x');
  const so    = document.getElementById('score-o');
  const sdraw = document.getElementById('score-draw');
  if (sx.textContent    !== String(scores.X))    { sx.textContent    = scores.X;    popScore(sx); }
  if (so.textContent    !== String(scores.O))    { so.textContent    = scores.O;    popScore(so); }
  if (sdraw.textContent !== String(scores.draw)) { sdraw.textContent = scores.draw; popScore(sdraw); }
}
```

- [ ] **Step 4: Verify in browser**

Expected:
- Three glass cards render side-by-side: "Player X | 0", "Draws | 0", "Player O | 0".
- X value is violet, O value is cyan.
- In AI mode, O card label updates to "AI".

- [ ] **Step 5: Commit**

```bash
git add templates/index.html
git commit -m "feat: scoreboard glass cards with pop animation on score update"
```

---

## Task 4: Turn Indicator (player pill badges)

**Files:**
- Modify: `templates/index.html` — add CSS, HTML, JS

- [ ] **Step 1: Add CSS for turn indicator**

Append inside `<style>`:

```css
/* ── Turn Indicator ── */
.turn-indicator {
  display: flex;
  gap: 0.75rem;
  width: 100%;
}

.player-badge {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  padding: 0.65rem 0.5rem;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: var(--surface);
  transition: background 0.25s, border-color 0.25s, box-shadow 0.25s, opacity 0.25s;
  opacity: 0.45;
}

.player-badge.active {
  opacity: 1;
}

.player-badge[data-player="X"].active {
  background: rgba(124, 58, 237, 0.12);
  border-color: var(--accent-x);
  box-shadow: 0 0 16px var(--accent-x-glow);
}

.player-badge[data-player="O"].active {
  background: rgba(6, 182, 212, 0.12);
  border-color: var(--accent-o);
  box-shadow: 0 0 16px var(--accent-o-glow);
}

.badge-symbol {
  font-size: 1.3rem;
  font-weight: 700;
  line-height: 1;
}

.player-badge[data-player="X"] .badge-symbol { color: var(--accent-x); }
.player-badge[data-player="O"] .badge-symbol { color: var(--accent-o); }

.badge-label {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.badge-status {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text-primary);
  min-height: 1em;
}

/* AI thinking dots */
@keyframes dotPulse {
  0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
  40%           { opacity: 1;   transform: scale(1); }
}

.ai-dots::before {
  content: '• • •';
  letter-spacing: 0.25em;
  display: inline-block;
}

.ai-thinking .ai-dots::before {
  animation: dotPulse 1.2s ease-in-out infinite;
}
```

- [ ] **Step 2: Add HTML for turn indicator**

Inside `<div class="app">`, after the scoreboard:

```html
<div class="turn-indicator" aria-label="Current turn">
  <div class="player-badge active" id="badge-x" data-player="X">
    <span class="badge-symbol">✕</span>
    <span class="badge-label">Player X</span>
    <span class="badge-status" id="badge-x-status">Your Turn</span>
  </div>
  <div class="player-badge" id="badge-o" data-player="O">
    <span class="badge-symbol">○</span>
    <span class="badge-label" id="badge-o-label">Player O</span>
    <span class="badge-status ai-dots" id="badge-o-status"></span>
  </div>
</div>
```

- [ ] **Step 3: Add JS for turn indicator updates**

Inside `<script>`:

```javascript
let currentPlayer = 'X';
let gameOver = false;

function setActiveBadge(player) {
  const bx = document.getElementById('badge-x');
  const bo = document.getElementById('badge-o');
  bx.classList.toggle('active', player === 'X');
  bo.classList.toggle('active', player === 'O');
  document.getElementById('badge-x-status').textContent = player === 'X' ? 'Your Turn' : '';
  document.getElementById('badge-o-status').textContent = player === 'O' ? 'Your Turn' : '';
}

function setAiThinking(thinking) {
  const bo = document.getElementById('badge-o');
  bo.classList.toggle('ai-thinking', thinking);
  if (thinking) {
    bo.classList.add('active');
    document.getElementById('badge-o-status').textContent = '';
    document.getElementById('badge-x-status').textContent = '';
  }
}
```

- [ ] **Step 4: Verify in browser**

Expected:
- Two badge pills side-by-side. X badge active (violet glow), O badge dimmed.
- In AI mode, switching to AI mode updates O badge label to "AI".
- No console errors.

- [ ] **Step 5: Commit**

```bash
git add templates/index.html
git commit -m "feat: turn indicator player badge pills with AI thinking dots"
```

---

## Task 5: Board — glass cells, ARIA, hover ghost, click feedback

**Files:**
- Modify: `templates/index.html` — add CSS, HTML, core JS game loop

- [ ] **Step 1: Add CSS for board and cells**

Append inside `<style>`:

```css
/* ── Board ── */
.board {
  display: grid;
  grid-template-columns: repeat(3, min(110px, 28vw));
  grid-template-rows:    repeat(3, min(110px, 28vw));
  gap: clamp(6px, 2vw, 10px);
}

.cell {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-cell);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
  transition: background 0.15s, border-color 0.15s, box-shadow 0.15s, transform 0.1s, opacity 0.3s;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

/* Hover ghost — color driven by data-current-player on .board */
.board[data-current-player="X"] .cell:not(.taken):hover {
  background: rgba(124, 58, 237, 0.1);
  border-color: rgba(124, 58, 237, 0.35);
}

.board[data-current-player="O"] .cell:not(.taken):hover {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.35);
}

.cell:not(.taken):active { transform: scale(0.92); }
.cell.taken { cursor: default; }

/* Winning state */
.cell.winner-cell {
  animation: winnerPulse 0.9s ease-in-out infinite alternate;
}

.cell.winner-cell[data-mark="X"] {
  background: rgba(124, 58, 237, 0.2);
  border-color: var(--accent-x);
}

.cell.winner-cell[data-mark="O"] {
  background: rgba(6, 182, 212, 0.2);
  border-color: var(--accent-o);
}

.cell.dim { opacity: 0.25; }

@keyframes winnerPulse {
  from { box-shadow: 0 0 0 rgba(124, 58, 237, 0); }
  to   { box-shadow: 0 0 20px rgba(124, 58, 237, 0.6); }
}

.cell.winner-cell[data-mark="O"] {
  animation-name: winnerPulseO;
}

@keyframes winnerPulseO {
  from { box-shadow: 0 0 0 rgba(6, 182, 212, 0); }
  to   { box-shadow: 0 0 20px rgba(6, 182, 212, 0.6); }
}

/* ── New Game Button ── */
.new-game-btn {
  width: 100%;
  padding: 0.8rem 2rem;
  background: var(--accent-x);
  color: #fff;
  border: none;
  border-radius: var(--radius-pill);
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

.new-game-btn:hover  { background: #6d28d9; }
.new-game-btn:active { transform: scale(0.97); }
```

- [ ] **Step 2: Add HTML for the board**

Inside `<div class="app">`, after the turn indicator:

```html
<div class="board" id="board" data-current-player="X"
     role="grid" aria-label="Tic-Tac-Toe board"></div>

<button class="new-game-btn" onclick="reset()">New Game</button>
```

- [ ] **Step 3: Add core JS — board init, renderBoard, handleClick, reset stub**

Inside `<script>` (add after existing JS):

```javascript
function buildBoard() {
  const board = document.getElementById('board');
  board.innerHTML = '';
  for (let i = 0; i < 9; i++) {
    const row = Math.floor(i / 3) + 1;
    const col = (i % 3) + 1;
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.setAttribute('role', 'gridcell');
    cell.setAttribute('tabindex', '0');
    cell.setAttribute('aria-label', `Row ${row}, Column ${col}, empty`);
    cell.dataset.index = i;
    cell.addEventListener('click', () => handleClick(i));
    cell.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleClick(i); }
    });
    board.appendChild(cell);
  }
}

function getCells() {
  return document.getElementById('board').querySelectorAll('.cell');
}

function renderBoard(boardData) {
  const cells = getCells();
  const boardEl = document.getElementById('board');
  cells.forEach((cell, i) => {
    const mark = boardData[i];
    cell.className = 'cell' + (mark ? ' taken' : '');
    cell.dataset.mark = mark || '';
    const row = Math.floor(i / 3) + 1;
    const col = (i % 3) + 1;
    cell.setAttribute('aria-label', `Row ${row}, Column ${col}, ${mark || 'empty'}`);
    if (!mark) cell.innerHTML = '';
  });
  boardEl.dataset.currentPlayer = currentPlayer;
}

async function handleClick(idx) {
  if (gameOver) return;
  const cells = getCells();
  const cell = cells[idx];
  if (cell.classList.contains('taken')) return;

  const boardEl = document.getElementById('board');
  boardEl.style.pointerEvents = 'none';

  if (mode === 'ai') setAiThinking(false);

  const res = await fetch('/move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ index: idx, player: currentPlayer }),
  });
  const data = await res.json();

  boardEl.style.pointerEvents = '';

  if (data.error) return;

  renderBoard(data.board);

  if (data.winner) {
    highlightWinner(data.combo);
    scores[data.winner]++;
    updateScores();
    gameOver = true;
    const msg = data.winner === 'O' && mode === 'ai' ? 'AI wins!' : `Player ${data.winner} wins!`;
    document.getElementById('announce').textContent = msg;
    showModal(data.winner, msg, false);
    return;
  }

  if (data.draw) {
    scores.draw++;
    updateScores();
    gameOver = true;
    document.getElementById('announce').textContent = "It's a draw!";
    showModal(null, "It's a Draw!", true);
    return;
  }

  if (mode === 'ai') {
    currentPlayer = 'X';
    setActiveBadge('X');
  } else {
    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    setActiveBadge(currentPlayer);
  }
  document.getElementById('board').dataset.currentPlayer = currentPlayer;
}

function highlightWinner(combo) {
  const cells = getCells();
  cells.forEach((cell, i) => {
    if (combo.includes(i)) {
      cell.classList.add('winner-cell');
    } else {
      cell.classList.add('dim');
    }
  });
}

async function reset() {
  const res = await fetch('/reset', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode }),
  });
  const data = await res.json();
  currentPlayer = 'X';
  gameOver = false;
  renderBoard(data.board);
  setActiveBadge('X');
  setAiThinking(false);
  document.getElementById('board').dataset.currentPlayer = 'X';
}

// Stub until Task 7
function showModal(winner, msg, isDraw) {
  console.log('showModal:', msg);
}

// Init on load
buildBoard();
reset();
```

- [ ] **Step 4: Verify in browser**

Expected:
- 3×3 glass grid renders.
- Hovering empty cells shows violet ghost (X's turn) or cyan ghost (O's turn).
- Clicking a cell logs "showModal" to console on win/draw.
- Cells shrink slightly on click (`scale(0.92)`).
- Winning cells glow and pulse; non-winners dim.
- Mode switching resets board.
- No console errors.

- [ ] **Step 5: Commit**

```bash
git add templates/index.html
git commit -m "feat: glass board cells, hover ghost, ARIA labels, core game loop"
```

---

## Task 6: SVG Stroke-Draw Animations for X and O

**Files:**
- Modify: `templates/index.html` — add CSS keyframes, JS SVG injection, update renderBoard

- [ ] **Step 1: Add CSS keyframes for stroke drawing**

Append inside `<style>`:

```css
/* ── SVG Draw Animations ── */
@keyframes drawLine {
  from { stroke-dashoffset: 85; }
  to   { stroke-dashoffset: 0; }
}

@keyframes drawCircle {
  from { stroke-dashoffset: 201; }
  to   { stroke-dashoffset: 0; }
}
```

- [ ] **Step 2: Add JS SVG factory functions**

Inside `<script>`, before `buildBoard`:

```javascript
function createXSvg() {
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('viewBox', '0 0 100 100');
  svg.setAttribute('width', '58%');
  svg.setAttribute('height', '58%');
  svg.setAttribute('aria-hidden', 'true');

  [[20,20,80,80,0],[80,20,20,80,80]].forEach(([x1,y1,x2,y2,delay]) => {
    const line = document.createElementNS(ns, 'line');
    line.setAttribute('x1', x1); line.setAttribute('y1', y1);
    line.setAttribute('x2', x2); line.setAttribute('y2', y2);
    line.setAttribute('stroke', 'var(--accent-x)');
    line.setAttribute('stroke-width', '8');
    line.setAttribute('stroke-linecap', 'round');
    line.setAttribute('stroke-dasharray', '85');
    line.setAttribute('stroke-dashoffset', '85');
    line.style.animation = `drawLine 0.25s ease forwards ${delay}ms`;
    svg.appendChild(line);
  });
  return svg;
}

function createOSvg() {
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('viewBox', '0 0 100 100');
  svg.setAttribute('width', '58%');
  svg.setAttribute('height', '58%');
  svg.setAttribute('aria-hidden', 'true');

  const circle = document.createElementNS(ns, 'circle');
  circle.setAttribute('cx', '50'); circle.setAttribute('cy', '50'); circle.setAttribute('r', '32');
  circle.setAttribute('fill', 'none');
  circle.setAttribute('stroke', 'var(--accent-o)');
  circle.setAttribute('stroke-width', '8');
  circle.setAttribute('stroke-linecap', 'round');
  circle.setAttribute('stroke-dasharray', '201');
  circle.setAttribute('stroke-dashoffset', '201');
  circle.style.animation = 'drawCircle 0.3s ease forwards';
  svg.appendChild(circle);
  return svg;
}
```

- [ ] **Step 3: Update `renderBoard` to inject SVGs**

Replace the `renderBoard` function with this version that injects SVGs for newly placed marks:

```javascript
function renderBoard(boardData) {
  const cells = getCells();
  const boardEl = document.getElementById('board');
  cells.forEach((cell, i) => {
    const mark = boardData[i];
    const row = Math.floor(i / 3) + 1;
    const col = (i % 3) + 1;
    cell.setAttribute('aria-label', `Row ${row}, Column ${col}, ${mark || 'empty'}`);

    if (!mark) {
      cell.className = 'cell';
      cell.dataset.mark = '';
      cell.innerHTML = '';
      return;
    }

    // Only inject SVG if not already present (avoids re-animating on re-render)
    if (cell.dataset.mark !== mark) {
      cell.className = 'cell taken';
      cell.dataset.mark = mark;
      cell.innerHTML = '';
      cell.appendChild(mark === 'X' ? createXSvg() : createOSvg());
    }
  });
  boardEl.dataset.currentPlayer = currentPlayer;
}
```

- [ ] **Step 4: Verify in browser**

Expected:
- Clicking a cell draws an X with two lines animating in sequence (violet strokes).
- O draws a circle animating from 12 o'clock clockwise (cyan stroke).
- Animation plays once per placement; re-renders don't re-animate existing marks.
- Winning cells still pulse after SVG is in place.
- No console errors.

- [ ] **Step 5: Commit**

```bash
git add templates/index.html
git commit -m "feat: SVG stroke-draw animations for X and O marks"
```

---

## Task 7: Result Modal (frosted glass, slide-up, confetti, focus trap)

**Files:**
- Modify: `templates/index.html` — add CSS, HTML, JS (replace `showModal` stub)

- [ ] **Step 1: Add CSS for the modal**

Append inside `<style>`:

```css
/* ── Result Modal ── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 1.5rem;
  opacity: 0;
  transition: opacity 0.25s;
}

.modal-overlay.visible {
  opacity: 1;
}

.modal-overlay[hidden] { display: none; }

.modal-card {
  position: relative;
  width: 100%;
  max-width: 340px;
  background: rgba(13, 13, 20, 0.88);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2.5rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.6);
  transform: scale(0.85) translateY(20px);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
}

.modal-overlay.visible .modal-card {
  transform: scale(1) translateY(0);
}

.modal-icon {
  font-size: 3.5rem;
  line-height: 1;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  text-align: center;
}

.modal-play-again {
  margin-top: 0.5rem;
  padding: 0.7rem 2.2rem;
  background: var(--accent-x);
  color: #fff;
  border: none;
  border-radius: var(--radius-pill);
  font-family: inherit;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

.modal-play-again:hover  { background: #6d28d9; }
.modal-play-again:active { transform: scale(0.96); }

/* ── Confetti ── */
.confetti-particle {
  position: absolute;
  top: -10px;
  border-radius: 3px;
  opacity: 0;
  animation: confettiFall linear forwards;
}

@keyframes confettiFall {
  0%   { opacity: 1;   transform: translateY(0)    rotate(0deg); }
  80%  { opacity: 1; }
  100% { opacity: 0;   transform: translateY(340px) rotate(720deg); }
}
```

- [ ] **Step 2: Add HTML for the modal**

Inside `<body>`, after `<div class="app">` (sibling, not inside `.app`):

```html
<div class="modal-overlay" id="modal-overlay"
     role="dialog" aria-modal="true" aria-labelledby="modal-title" hidden>
  <div class="modal-card" id="modal-card">
    <div class="modal-icon" id="modal-icon"></div>
    <h2 class="modal-title" id="modal-title"></h2>
    <button class="modal-play-again" id="modal-play-again">Play Again</button>
  </div>
</div>
```

- [ ] **Step 3: Add JS for modal show/hide, focus trap, confetti, and Play Again**

Inside `<script>`, replace the `showModal` stub with:

```javascript
const CONFETTI_COLORS = ['#7c3aed','#06b6d4','#f59e0b','#f472b6','#34d399','#818cf8'];

function launchConfetti(card) {
  for (let i = 0; i < 40; i++) {
    const p = document.createElement('div');
    p.className = 'confetti-particle';
    p.style.cssText = `
      left:${Math.random()*100}%;
      background:${CONFETTI_COLORS[Math.floor(Math.random()*CONFETTI_COLORS.length)]};
      animation-delay:${(Math.random()*0.45).toFixed(3)}s;
      animation-duration:${(0.85+Math.random()*0.65).toFixed(3)}s;
      width:${6+Math.floor(Math.random()*7)}px;
      height:${6+Math.floor(Math.random()*7)}px;
      transform:rotate(${Math.floor(Math.random()*360)}deg);
    `;
    card.appendChild(p);
  }
  setTimeout(() => card.querySelectorAll('.confetti-particle').forEach(p=>p.remove()), 1800);
}

function trapFocus(el) {
  const focusable = el.querySelectorAll('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])');
  const first = focusable[0];
  const last  = focusable[focusable.length - 1];
  el._trapHandler = e => {
    if (e.key !== 'Tab') return;
    if (e.shiftKey) {
      if (document.activeElement === first) { e.preventDefault(); last.focus(); }
    } else {
      if (document.activeElement === last)  { e.preventDefault(); first.focus(); }
    }
  };
  el.addEventListener('keydown', el._trapHandler);
}

function releaseFocus(el) {
  if (el._trapHandler) el.removeEventListener('keydown', el._trapHandler);
}

let _escHandler = null;
let _lastFocused = null;

function showModal(winner, msg, isDraw) {
  const overlay = document.getElementById('modal-overlay');
  const icon    = document.getElementById('modal-icon');
  const title   = document.getElementById('modal-title');
  const btn     = document.getElementById('modal-play-again');
  const card    = document.getElementById('modal-card');

  icon.textContent  = isDraw ? '🤝' : '🏆';
  title.textContent = msg;

  overlay.removeAttribute('hidden');
  // Force reflow before adding .visible so transition fires
  void overlay.offsetWidth;
  overlay.classList.add('visible');

  if (winner && !isDraw) launchConfetti(card);

  trapFocus(overlay);
  _lastFocused = document.activeElement;
  btn.focus();

  btn.onclick = () => closeModal(true);

  overlay.onclick = e => { if (e.target === overlay) closeModal(false); };

  _escHandler = e => { if (e.key === 'Escape') closeModal(false); };
  document.addEventListener('keydown', _escHandler);
}

function closeModal(doReset) {
  const overlay = document.getElementById('modal-overlay');
  releaseFocus(overlay);
  if (_escHandler) document.removeEventListener('keydown', _escHandler);

  overlay.classList.remove('visible');
  setTimeout(() => {
    overlay.setAttribute('hidden', '');
    if (_lastFocused) _lastFocused.focus();
  }, 300);

  if (doReset) reset();
}
```

- [ ] **Step 4: Verify in browser**

Expected:
- Win: modal slides up with 🏆 icon, winner text, confetti burst, "Play Again" focused.
- Draw: modal slides up with 🤝, "It's a Draw!", no confetti.
- Clicking "Play Again" closes modal and starts a new game.
- Clicking the backdrop closes modal without resetting.
- `Escape` key closes modal.
- Tab stays trapped inside modal while open.
- After close, focus returns to last focused element before modal.

- [ ] **Step 5: Commit**

```bash
git add templates/index.html
git commit -m "feat: result modal with slide-up animation, confetti on win, focus trap"
```

---

## Task 8: Accessibility + Reduced Motion + Mobile Polish

**Files:**
- Modify: `templates/index.html` — add reduced motion CSS, verify/fix ARIA, touch targets

- [ ] **Step 1: Add reduced motion media query**

Append inside `<style>` as the last CSS block:

```css
/* ── Reduced Motion ── */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-delay: 0.001ms !important;
    transition-duration: 0.001ms !important;
  }

  /* SVG draws: show final state instantly */
  .cell svg line,
  .cell svg circle {
    stroke-dashoffset: 0 !important;
  }

  /* No confetti */
  .confetti-particle { display: none !important; }
}

/* ── Mobile Safety ── */
@media (max-width: 380px) {
  .turn-indicator { gap: 0.4rem; }
  .scoreboard     { gap: 0.4rem; }
  .badge-label,
  .score-label    { font-size: 0.62rem; }
}
```

- [ ] **Step 2: Verify keyboard navigation end-to-end**

Open `http://127.0.0.1:5000`. Without touching the mouse:
- `Tab` to reach mode toggle options. `Enter` / `Space` to switch mode.
- `Tab` to reach board cells. Arrow key navigation is not required (each cell has `tabindex="0"`).
- `Enter` / `Space` on a cell to place a mark.
- On game end, modal receives focus automatically. `Tab` stays inside modal. `Escape` closes modal.

Expected: full game playable by keyboard alone.

- [ ] **Step 3: Verify touch targets on mobile**

In Chrome DevTools, set device to "iPhone SE" (375×667).  
Expected:
- All cells are ≥ 44×44px.
- Mode toggle buttons are ≥ 44px tall.
- "New Game" button spans full width.
- No horizontal scroll.
- Board fits without overflow.

- [ ] **Step 4: Verify reduced motion**

In Chrome DevTools → Rendering → "Emulate CSS media feature prefers-reduced-motion: reduce".  
Expected:
- Placing a mark shows X/O instantly (no draw animation).
- Scoreboard increments with no pop animation.
- Modal appears without slide-up animation.
- No confetti particles appear.

- [ ] **Step 5: Final smoke test (full game flows)**

Test all 4 flows manually:
1. **PvP win** — play until X wins. Modal appears with 🏆, score increments with pop, confetti fires, Play Again resets board.
2. **PvP draw** — fill board with no winner. Modal appears with 🤝, draw score pops.
3. **vs AI win** — AI is unbeatable via minimax; play toward a draw by default. Verify AI thinking dots appear briefly during AI computation.
4. **vs AI draw** — force a draw. Confirm identical draw modal.

Expected: All flows complete without console errors or UI desyncs.

- [ ] **Step 6: Commit**

```bash
git add templates/index.html
git commit -m "feat: reduced motion support, mobile polish, a11y keyboard nav verified"
```

---

## Self-Review vs Spec

| Spec Section | Covered by Task |
|---|---|
| CSS tokens (§3.1) | Task 1 |
| Inter font (§3.2) | Task 1 |
| Fluid layout, max-width 420px (§4) | Task 1 |
| Cell size min(110px, 28vw) (§5) | Task 5 |
| Backdrop-filter glass cells (§5) | Task 5 |
| SVG X stroke-draw (§5.1) | Task 6 |
| SVG O stroke-draw (§5.1) | Task 6 |
| Hover ghost via data-current-player (§5.2) | Task 5 |
| Click scale feedback (§5.3) | Task 5 |
| Winner glow + non-winner dim (§5.4) | Task 5 |
| Turn indicator pills (§6) | Task 4 |
| AI thinking dots (§6) | Task 4 |
| board pointer-events:none during AI (§6) | Task 5 |
| Result modal frosted glass (§7.2) | Task 7 |
| Modal slide-up animation (§7.2) | Task 7 |
| Modal emoji icon + title (§7.3) | Task 7 |
| Play Again → /reset (§7.3) | Task 7 |
| Backdrop click closes (§7.3) | Task 7 |
| Confetti on win (§7.4) | Task 7 |
| Modal ARIA dialog (§7.5) | Task 7 |
| Focus trap (§7.5) | Task 7 |
| Escape key closes (§7.5) | Task 7 |
| aria-live result announcement (§7.5) | Task 5 (announce el) + Task 7 |
| Score pop animation (§8) | Task 3 |
| O label → "AI" in AI mode (§8) | Task 3, 4 |
| Segmented mode toggle (§9) | Task 2 |
| New Game button (§10) | Task 5 |
| Cell ARIA labels (§11) | Task 5 |
| role=radiogroup on toggle (§11) | Task 2 |
| aria-live on scoreboard (§11) | Task 3 |
| WCAG AA contrast (§11) | white-on-violet/cyan throughout |
| prefers-reduced-motion (§12) | Task 8 |
| min(110px, 28vw) fluid cells (§13) | Task 5 |
| Touch targets ≥ 44px (§13) | Task 8 |
| No horizontal scroll ≥ 320px (§13) | Task 8 |
