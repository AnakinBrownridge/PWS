# PWS

Polymorphic (automatic window organization) Window System. A CSS-styled WM which comes with its own Quickshell-inspired shell that can also be styled.

This repository now includes a lightweight browser-based prototype of the idea: a desktop shell that auto-arranges windows using a CSS-driven layout engine and a polished desktop UI.

## What is included

- A desktop shell mockup inspired by Quickshell and CSS-styled tiling environments
- A small layout engine that automatically places windows based on priority and workspace size
- A dark, modern theme with a dock, top bar, and window chrome
- A working static demo that can be opened directly in a browser

## Run it

Open `index.html` in any modern browser.

If you want to serve it locally instead of opening the file directly, you can run:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Project structure

- `index.html` – shell layout
- `styles.css` – desktop and window styling
- `app.js` – automatic window arrangement logic

## Concept

PWS treats window placement as a live layout problem rather than a fixed tile grid. The system prefers a primary focus window, then fills the remaining space with supporting windows whose sizes adapt to the current workspace and the active app priorities.
