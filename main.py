#!/usr/bin/env python3
import tkinter as tk
from tkinter import font
import math
import random

class Window:
    def __init__(self, window_id, title, priority, accent='accent'):
        self.id = window_id
        self.title = title
        self.priority = priority
        self.accent = accent
        self.active = False
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.frame = None

class PWS:
    def __init__(self, root):
        self.root = root
        self.root.title("PWS - Polymorphic Window System")
        self.root.geometry("1220x760")
        
        # Colors
        self.colors = {
            'bg_0': '#0b1020',
            'bg_1': '#101827',
            'bg_2': '#1b2437',
            'panel': '#111723',
            'surface': '#0a0e15',
            'border': '#a4c3ff2e',
            'text': '#edf6ff',
            'text_soft': '#b2bfd9',
            'accent': '#7dd3fc',
            'accent_warm': '#f9a8d4',
            'shadow': '#030712a6',
        }
        
        self.windows = [
            Window('browser', 'Browser', 100, 'accent'),
            Window('terminal', 'Terminal', 78, 'warm'),
            Window('editor', 'Editor', 82, 'accent'),
            Window('notes', 'Notes', 65, 'warm'),
            Window('media', 'Media', 58, 'accent'),
        ]
        self.windows[0].active = True
        
        self.setup_ui()
        self.focus_rotation_index = 0
        self.rotate_focus()
        
    def setup_ui(self):
        # Main shell
        self.root.configure(bg=self.colors['bg_1'])
        
        # Top bar
        topbar = tk.Frame(self.root, bg='#0e121c', height=58)
        topbar.pack(side=tk.TOP, fill=tk.X)
        topbar.pack_propagate(False)
        
        brand = tk.Label(topbar, text="PWS", bg='#0e121c', fg=self.colors['text'],
                        font=('Inter', 10, 'bold'))
        brand.pack(side=tk.LEFT, padx=18, pady=10)
        
        # Desktop grid
        desktop = tk.Frame(self.root, bg=self.colors['bg_1'])
        desktop.pack(fill=tk.BOTH, expand=True)
        
        # Dock
        dock = tk.Frame(desktop, bg='#10163422', width=86)
        dock.pack(side=tk.LEFT, fill=tk.Y)
        dock.pack_propagate(False)
        
        for i in range(5):
            btn = tk.Button(dock, width=4, height=2, bg='#1e293b', fg=self.colors['text'],
                           font=('Inter', 14), relief=tk.FLAT, bd=0)
            btn.pack(padx=12, pady=7)
            if i == 0:
                btn.configure(bg='#38bdf8', fg='#000')
        
        # Workspace panel
        workspace_panel = tk.Frame(desktop, bg=self.colors['surface'])
        workspace_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=18, pady=18)
        
        # Workspace header
        header = tk.Frame(workspace_panel, bg=self.colors['surface'])
        header.pack(fill=tk.X, padx=8, pady=(0, 14))
        
        tk.Label(header, text="ACTIVE DESKTOP", font=('Inter', 7), fg=self.colors['text_soft'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        tk.Label(header, text="Workspace 01", font=('Inter', 18, 'bold'), fg=self.colors['text'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        # Workspace container
        self.workspace = tk.Frame(workspace_panel, bg=self.colors['bg_2'], relief=tk.SOLID, bd=1)
        self.workspace.pack(fill=tk.BOTH, expand=True)
        self.workspace.configure(highlightbackground=self.colors['border'], highlightthickness=1)
        
        # Render initial windows
        self.render_windows()
        
        self.root.bind('<Configure>', lambda e: self.on_resize())
        
    def render_windows(self):
        # Clear existing
        for widget in self.workspace.winfo_children():
            widget.destroy()
        
        ordered = sorted(self.windows, key=lambda w: w.priority, reverse=True)
        
        for idx, win in enumerate(ordered):
            self.render_window(win, idx)
    
    def render_window(self, win, index):
        frame = tk.Frame(self.workspace, bg='#0e121c', relief=tk.SOLID, bd=1)
        frame.place(x=0, y=0, width=200, height=150)
        
        # Title bar
        titlebar = tk.Frame(frame, bg='#0a0f1a', height=34)
        titlebar.pack(fill=tk.X)
        titlebar.pack_propagate(False)
        
        title_label = tk.Label(titlebar, text=win.title.upper(), font=('Inter', 8),
                              fg=self.colors['text_soft'], bg='#0a0f1a')
        title_label.pack(padx=12, pady=8)
        
        # Content
        content = tk.Frame(frame, bg='#111827')
        content.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
        
        for _ in range(3):
            row = tk.Frame(content, bg='#111827')
            row.pack(fill=tk.BOTH, expand=True, pady=5)
            for _ in range(2):
                box = tk.Frame(row, bg='#1e293b', relief=tk.SOLID, bd=1,
                             highlightbackground=self.colors['border'])
                box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)
        
        win.frame = frame
        self.arrange_windows()
    
    def arrange_windows(self):
        workspace_width = self.workspace.winfo_width()
        workspace_height = self.workspace.winfo_height()
        
        if workspace_width < 2 or workspace_height < 2:
            return
        
        ordered = sorted(self.windows, key=lambda w: w.priority, reverse=True)
        
        layouts = [
            {'x': 0.024, 'y': 0.04, 'w': 0.56, 'h': 0.9},
            {'x': 0.6, 'y': 0.04, 'w': 0.36, 'h': 0.46},
            {'x': 0.6, 'y': 0.54, 'w': 0.36, 'h': 0.42},
            {'x': 0.024, 'y': 0.6, 'w': 0.34, 'h': 0.34},
            {'x': 0.38, 'y': 0.6, 'w': 0.2, 'h': 0.34},
        ]
        
        for idx, win in enumerate(ordered):
            if win.frame:
                pos = layouts[min(idx, len(layouts)-1)]
                x = int(pos['x'] * workspace_width)
                y = int(pos['y'] * workspace_height)
                w = int(pos['w'] * workspace_width)
                h = int(pos['h'] * workspace_height)
                win.frame.place(x=x, y=y, width=w, height=h)
    
    def on_resize(self):
        self.arrange_windows()
    
    def rotate_focus(self):
        # Rotate active window
        current = self.windows[0]
        self.windows.append(self.windows.pop(0))
        
        for idx, win in enumerate(self.windows):
            win.active = (idx == 0)
        
        self.render_windows()
        self.root.after(5000, self.rotate_focus)

if __name__ == '__main__':
    root = tk.Tk()
    app = PWS(root)
    root.mainloop()
