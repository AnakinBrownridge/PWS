#!/usr/bin/env python3
"""
PWS - Polymorphic Window System
Fullscreen desktop shell with app launching and auto-layout.
Run with: python3 main.py
"""

import os
import sys
import time
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional
import tkinter as tk
from tkinter import messagebox


@dataclass
class AppWindow:
    app_id: str
    title: str
    icon: str
    command: List[str]
    priority: int
    accent: str = "accent"
    active: bool = False
    frame: Optional[tk.Frame] = None
    process: Optional[subprocess.Popen] = None


class PWSDesktop:
    APPS = [
        {"id": "browser", "title": "Browser", "icon": "⌂", "cmd": ["firefox"], "priority": 100},
        {"id": "terminal", "title": "Terminal", "icon": "❯", "cmd": ["xterm"], "priority": 78},
        {"id": "editor", "title": "Editor", "icon": "✎", "cmd": ["gedit"], "priority": 82},
        {"id": "files", "title": "Files", "icon": "▤", "cmd": ["nautilus"], "priority": 65},
        {"id": "settings", "title": "Settings", "icon": "⚙", "cmd": ["gedit"], "priority": 58},
    ]

    LAYOUTS = [
        {"x": 0.024, "y": 0.04, "w": 0.56, "h": 0.9},
        {"x": 0.6, "y": 0.04, "w": 0.36, "h": 0.46},
        {"x": 0.6, "y": 0.54, "w": 0.36, "h": 0.42},
        {"x": 0.024, "y": 0.6, "w": 0.34, "h": 0.34},
        {"x": 0.38, "y": 0.6, "w": 0.2, "h": 0.34},
    ]

    COLORS = {
        "bg_0": "#0b1020",
        "bg_1": "#101827",
        "bg_2": "#1b2437",
        "panel": "#111723",
        "surface": "#0a0e15",
        "border": "#a4c3ff2e",
        "text": "#edf6ff",
        "text_soft": "#b2bfd9",
        "accent": "#7dd3fc",
        "accent_warm": "#f9a8d4",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("PWS")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg=self.COLORS["bg_1"])

        self.apps: List[AppWindow] = []
        self.time_var = tk.StringVar()

        self.setup_ui()
        self.setup_keyboard()
        self.update_time()
        self.check_processes()

    def setup_ui(self):
        main = tk.Frame(self.root, bg=self.COLORS["bg_1"])
        main.pack(fill="both", expand=True)

        topbar = tk.Frame(main, bg="#0e121c", height=58)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="PWS", bg="#0e121c", fg=self.COLORS["text"],
                font=("Arial", 12, "bold")).pack(side="left", padx=(18, 8), pady=10)
        tk.Label(topbar, text="Polymorphic Workspace", bg="#0e121c", fg=self.COLORS["text_soft"],
                font=("Arial", 9)).pack(side="left", pady=10)

        spacer = tk.Frame(topbar, bg="#0e121c")
        spacer.pack(side="left", expand=True)

        tk.Label(topbar, text="● auto-layout  ● quickshell", bg="#0e121c", fg=self.COLORS["accent"],
                font=("Arial", 8)).pack(side="left", padx=20, pady=10)

        tk.Label(topbar, textvariable=self.time_var, bg="#0e121c", fg=self.COLORS["text"],
                font=("Arial", 11, "bold")).pack(side="right", padx=(0, 18), pady=10)

        desktop = tk.Frame(main, bg=self.COLORS["bg_1"])
        desktop.pack(fill="both", expand=True)

        dock = tk.Frame(desktop, bg="#101827", width=100)
        dock.pack(side="left", fill="y")
        dock.pack_propagate(False)

        self.dock_buttons = {}
        for app in self.APPS:
            btn = tk.Button(
                dock, text=app["icon"], bg="#1e293b", fg=self.COLORS["text"],
                font=("Arial", 16), bd=0, relief="flat", width=3, height=2,
                command=lambda aid=app["id"]: self.launch_app(aid)
            )
            btn.pack(padx=8, pady=8)
            self.dock_buttons[app["id"]] = btn

        panel = tk.Frame(desktop, bg=self.COLORS["surface"])
        panel.pack(side="left", fill="both", expand=True, padx=18, pady=18)

        header = tk.Frame(panel, bg=self.COLORS["surface"])
        header.pack(fill="x", padx=8, pady=(0, 14))

        tk.Label(header, text="ACTIVE DESKTOP", bg=self.COLORS["surface"], fg=self.COLORS["text_soft"],
                font=("Arial", 7, "bold")).pack(anchor="w")
        tk.Label(header, text="Workspace 01", bg=self.COLORS["surface"], fg=self.COLORS["text"],
                font=("Arial", 20, "bold")).pack(anchor="w")

        self.workspace = tk.Frame(
            panel, bg=self.COLORS["bg_2"],
            highlightbackground=self.COLORS["border"], highlightthickness=1
        )
        self.workspace.pack(fill="both", expand=True)
        self.workspace.bind("<Configure>", lambda e: self.arrange_windows())

    def setup_keyboard(self):
        self.root.bind("<alt-Tab>", self.cycle_focus)
        self.root.bind("<Control-q>", self.quit_app)
        self.root.bind("<Escape>", self.quit_app)
        self.root.bind("<F11>", self.toggle_fullscreen)

        for i, app in enumerate(self.APPS):
            self.root.bind(f"<alt-{i+1}>", lambda e, aid=app["id"]: self.launch_app(aid))

    def toggle_fullscreen(self, event=None):
        current = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current)
        return "break"

    def cycle_focus(self, event=None):
        if not self.apps:
            return "break"
        self.apps = self.apps[1:] + self.apps[:1]
        for i, app in enumerate(self.apps):
            app.active = (i == 0)
        self.render_windows()
        return "break"

    def launch_app(self, app_id):
        app_def = next((a for a in self.APPS if a["id"] == app_id), None)
        if not app_def:
            return

        for app in self.apps:
            if app.app_id == app_id:
                self.apps.remove(app)
                self.apps.insert(0, app)
                for i, a in enumerate(self.apps):
                    a.active = (i == 0)
                self.render_windows()
                return

        if not shutil.which(app_def["cmd"][0]):
            messagebox.showwarning("App Not Found", f"{app_def['title']} is not installed.")
            return

        try:
            process = subprocess.Popen(
                app_def["cmd"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        except Exception as e:
            messagebox.showerror("Launch Failed", f"Failed to launch {app_def['title']}: {e}")
            return

        new_app = AppWindow(
            app_id=app_def["id"],
            title=app_def["title"],
            icon=app_def["icon"],
            command=app_def["cmd"],
            priority=app_def["priority"],
            process=process,
        )

        for app in self.apps:
            app.active = False

        self.apps.insert(0, new_app)
        new_app.active = True
        self.render_windows()

    def render_windows(self):
        for child in self.workspace.winfo_children():
            child.destroy()

        if not self.apps:
            return

        ordered = sorted(self.apps, key=lambda a: a.priority, reverse=True)
        ws_width = self.workspace.winfo_width()
        ws_height = self.workspace.winfo_height()

        if ws_width < 100 or ws_height < 100:
            self.root.after(100, self.render_windows)
            return

        for idx, app in enumerate(ordered):
            frame = tk.Frame(
                self.workspace, bg="#0e121c",
                highlightbackground=self.COLORS["accent"] if app.active else self.COLORS["border"],
                highlightthickness=2 if app.active else 1
            )

            titlebar = tk.Frame(frame, bg="#0a0f1a", height=34)
            titlebar.pack(fill="x")
            titlebar.pack_propagate(False)

            tk.Label(
                titlebar, text=app.title.upper(), bg="#0a0f1a", fg=self.COLORS["text_soft"],
                font=("Arial", 8, "bold")
            ).pack(side="left", padx=12, pady=8)

            content = tk.Frame(frame, bg="#111827")
            content.pack(fill="both", expand=True, padx=14, pady=14)

            for _ in range(3):
                row = tk.Frame(content, bg="#111827")
                row.pack(fill="x", pady=4)
                for _ in range(2):
                    box = tk.Frame(
                        row, bg="#1e293b",
                        highlightbackground=self.COLORS["accent"] if app.active else "#444",
                        highlightthickness=1
                    )
                    box.pack(side="left", fill="both", expand=True, padx=(0, 6))

            layout = self.LAYOUTS[min(idx, len(self.LAYOUTS) - 1)]
            x = int(layout["x"] * ws_width)
            y = int(layout["y"] * ws_height)
            w = int(layout["w"] * ws_width)
            h = int(layout["h"] * ws_height)

            frame.place(x=x, y=y, width=w, height=h)
            app.frame = frame

    def arrange_windows(self):
        self.render_windows()

    def update_time(self):
        self.time_var.set(time.strftime("%H:%M"))
        self.root.after(60000, self.update_time)

    def check_processes(self):
        alive = []
        for app in self.apps:
            if app.process is None or app.process.poll() is None:
                alive.append(app)

        if len(alive) != len(self.apps):
            self.apps = alive
            if self.apps:
                self.apps[0].active = True
            self.render_windows()

        self.root.after(2000, self.check_processes)

    def quit_app(self, event=None):
        for app in self.apps:
            if app.process:
                try:
                    app.process.terminate()
                    app.process.wait(timeout=2)
                except:
                    pass
        self.root.destroy()
        return "break"

    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    desktop = PWSDesktop(root)
    desktop.run()


if __name__ == "__main__":
    main()
