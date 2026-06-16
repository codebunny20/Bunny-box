# toolbox_ui.py
import subprocess
import sys
import json
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk


# ---------- paths ----------


BASE_DIR = Path(__file__).resolve().parent
TOOLS_DIR = BASE_DIR.parent / "tools"
SETTINGS_DIR = BASE_DIR / "settings"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "appearance_mode": "dark",
    "color_theme": "blue",
    "window_width": 400,
    "window_height": 600,
}


def _sanitize_settings(raw: dict) -> dict:
    settings = dict(DEFAULT_SETTINGS)

    appearance_mode = str(raw.get("appearance_mode", settings["appearance_mode"]))
    if appearance_mode not in {"system", "light", "dark"}:
        appearance_mode = settings["appearance_mode"]

    color_theme = str(raw.get("color_theme", settings["color_theme"]))
    if color_theme not in {"blue", "green", "dark-blue"}:
        color_theme = settings["color_theme"]

    width = raw.get("window_width", settings["window_width"])
    height = raw.get("window_height", settings["window_height"])

    try:
        width = int(width)
    except (TypeError, ValueError):
        width = settings["window_width"]

    try:
        height = int(height)
    except (TypeError, ValueError):
        height = settings["window_height"]

    width = max(320, min(1200, width))
    height = max(420, min(1000, height))

    settings["appearance_mode"] = appearance_mode
    settings["color_theme"] = color_theme
    settings["window_width"] = width
    settings["window_height"] = height
    return settings


def load_settings() -> dict:
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)

    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        data = {}

    return _sanitize_settings(data if isinstance(data, dict) else {})


def save_settings(settings: dict) -> None:
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    clean_settings = _sanitize_settings(settings)
    with SETTINGS_FILE.open("w", encoding="utf-8") as f:
        json.dump(clean_settings, f, indent=2)


def apply_settings_to_app(app: ctk.CTk, settings: dict) -> None:
    ctk.set_appearance_mode(settings["appearance_mode"])
    ctk.set_default_color_theme(settings["color_theme"])
    app.geometry(f"{settings['window_width']}x{settings['window_height']}")


# ---------- process launcher ----------

def show_output_popup(parent: ctk.CTk, title: str) -> tuple[ctk.CTkToplevel, ctk.CTkTextbox]:
    popup = ctk.CTkToplevel(parent)
    popup.title(title)
    popup.geometry("700x500")
    popup.grab_set()

    ctk.CTkLabel(
        popup,
        text=title,
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=(12, 6))

    output_box = ctk.CTkTextbox(popup, wrap="word")
    output_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    output_box.insert("end", "Running...\n")
    output_box.configure(state="disabled")

    ctk.CTkButton(
        popup,
        text="Close",
        fg_color="gray25",
        hover_color="gray35",
        command=popup.destroy
    ).pack(fill="x", padx=10, pady=(0, 10))

    return popup, output_box


def append_output(output_box: ctk.CTkTextbox, text: str) -> None:
    output_box.configure(state="normal")
    output_box.insert("end", text)
    output_box.see("end")
    output_box.configure(state="disabled")


def launch_powershell_with_popup(parent: ctk.CTk, script_path: Path) -> None:
    script_path = script_path.resolve()
    popup, output_box = show_output_popup(parent, script_path.stem)

    def worker() -> None:
        cmd = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script_path)
        ]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW,
            close_fds=True
        )

        assert process.stdout is not None
        for line in process.stdout:
            popup.after(0, append_output, output_box, line)

        return_code = process.wait()
        popup.after(0, append_output, output_box, f"\n[process exited with code {return_code}]\n")

    import threading
    threading.Thread(target=worker, daemon=True).start()


def launch_cmd_with_popup(parent: ctk.CTk, script_path: Path) -> None:
    script_path = script_path.resolve()
    popup, output_box = show_output_popup(parent, script_path.stem)

    def worker() -> None:
        cmd = ["cmd.exe", "/c", str(script_path)]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW,
            close_fds=True
        )

        assert process.stdout is not None
        for line in process.stdout:
            popup.after(0, append_output, output_box, line)

        return_code = process.wait()
        popup.after(0, append_output, output_box, f"\n[process exited with code {return_code}]\n")

    import threading
    threading.Thread(target=worker, daemon=True).start()


def launch_script(script_path: Path) -> None:
    """
    Launch any script type (.vbs, .cmd, .bat, .ps1) in a detached way
    so it keeps running even if the Python UI is closed.
    """
    # Ensure absolute path
    script_path = script_path.resolve()
    suffix = script_path.suffix.lower()

    # DETACHED_PROCESS makes it independent from this process
    DETACHED_PROCESS = 0x00000008
    CREATE_NEW_CONSOLE = 0x00000010

    if suffix == ".vbs":
        cmd = ["wscript.exe", str(script_path)]
        flags = DETACHED_PROCESS
    elif suffix in [".cmd", ".bat"]:
        return
    elif suffix == ".ps1":
        return
    else:
        return  # Unsupported file type

    subprocess.Popen(
        cmd,
        creationflags=flags,
        close_fds=True
    )


# ---------- UI ----------

def build_tools_list() -> list[Path]:
    """
    Return a sorted list of script files (.vbs, .cmd, .bat, .ps1) in /tools (top-level only).
    """
    if not TOOLS_DIR.exists():
        return []

    valid_extensions = {".vbs", ".cmd", ".bat", ".ps1"}
    return sorted(
        p for p in TOOLS_DIR.iterdir()
        if p.suffix.lower() in valid_extensions
    )


def build_folders_list() -> list[Path]:
    """
    Return a sorted list of sub-folders inside /tools.
    """
    if not TOOLS_DIR.exists():
        return []

    return sorted(p for p in TOOLS_DIR.iterdir() if p.is_dir())


def open_folder_picker(folder: Path, parent: ctk.CTk) -> None:
    """
    Open a top-level popup that lists all script files in a sub-folder.
    The user clicks one to launch it.
    """
    popup = ctk.CTkToplevel(parent)
    popup.title(folder.name)
    popup.geometry("320x400")
    popup.grab_set()  # modal

    ctk.CTkLabel(
        popup,
        text=folder.name,
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=(12, 6))

    scroll = ctk.CTkScrollableFrame(popup)
    scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    valid_extensions = {".vbs", ".cmd", ".bat", ".ps1"}
    scripts = sorted(
        p for p in folder.iterdir()
        if p.suffix.lower() in valid_extensions
    )

    if not scripts:
        ctk.CTkLabel(scroll, text="No scripts in this folder.").pack(pady=10)
    else:
        for script in scripts:
            btn = ctk.CTkButton(
                scroll,
                text=script.stem,
                command=lambda p=script: (
                    launch_powershell_with_popup(parent, p) if p.suffix.lower() == ".ps1" else launch_cmd_with_popup(parent, p) if p.suffix.lower() in [".cmd", ".bat"] else launch_script(p),
                    popup.destroy()
                )
            )
            btn.pack(fill="x", padx=8, pady=4)

    ctk.CTkButton(
        popup,
        text="Cancel",
        fg_color="gray25",
        hover_color="gray35",
        command=popup.destroy
    ).pack(fill="x", padx=10, pady=(0, 10))


def populate_tools(tools_frame: ctk.CTkScrollableFrame, parent: ctk.CTk) -> None:
    """
    Add all top-level script buttons and sub-folder buttons to tools_frame.
    """
    tools = build_tools_list()
    folders = build_folders_list()

    if not tools and not folders:
        ctk.CTkLabel(
            tools_frame,
            text=f"No scripts found in: {TOOLS_DIR}",
            anchor="w",
            justify="left"
        ).pack(padx=10, pady=10, fill="x")
        return

    # Top-level script files
    for tool_path in tools:
        btn = ctk.CTkButton(
            tools_frame,
            text=tool_path.stem,
            command=lambda p=tool_path: launch_powershell_with_popup(parent, p) if p.suffix.lower() == ".ps1" else launch_cmd_with_popup(parent, p) if p.suffix.lower() in [".cmd", ".bat"] else launch_script(p)
        )
        btn.pack(fill="x", padx=10, pady=5)

    # Sub-folders — shown as folder buttons with a  prefix
    for folder in folders:
        btn = ctk.CTkButton(
            tools_frame,
            text=f"📁  {folder.name}",
            fg_color="gray30",
            hover_color="gray40",
            command=lambda f=folder: open_folder_picker(f, parent)
        )
        btn.pack(fill="x", padx=10, pady=5)


def main() -> None:
    settings = load_settings()
    ctk.set_appearance_mode(settings["appearance_mode"])
    ctk.set_default_color_theme(settings["color_theme"])

    app = ctk.CTk()
    app.title("System Toolbox")
    app.geometry(f"{settings['window_width']}x{settings['window_height']}")

    # Root frame
    root_frame = ctk.CTkFrame(app)
    root_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Header row
    header_frame = ctk.CTkFrame(root_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 10))

    title_label = ctk.CTkLabel(
        header_frame,
        text="System Toolbox",
        font=ctk.CTkFont(size=20, weight="bold")
    )
    title_label.pack(side="left")

    def open_settings() -> None:
        dialog = ctk.CTkToplevel(app)
        dialog.title("Settings")
        dialog.geometry("360x320")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Appearance mode").pack(anchor="w", padx=12, pady=(12, 4))
        appearance_var = ctk.StringVar(value=settings["appearance_mode"])
        appearance_menu = ctk.CTkOptionMenu(
            dialog,
            values=["system", "light", "dark"],
            variable=appearance_var,
        )
        appearance_menu.pack(fill="x", padx=12)

        ctk.CTkLabel(dialog, text="Color theme").pack(anchor="w", padx=12, pady=(12, 4))
        theme_var = ctk.StringVar(value=settings["color_theme"])
        theme_menu = ctk.CTkOptionMenu(
            dialog,
            values=["blue", "green", "dark-blue"],
            variable=theme_var,
        )
        theme_menu.pack(fill="x", padx=12)

        size_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        size_frame.pack(fill="x", padx=12, pady=(12, 0))

        ctk.CTkLabel(size_frame, text="Width").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ctk.CTkLabel(size_frame, text="Height").grid(row=0, column=1, sticky="w", padx=(8, 0))

        width_var = ctk.StringVar(value=str(settings["window_width"]))
        height_var = ctk.StringVar(value=str(settings["window_height"]))
        width_entry = ctk.CTkEntry(size_frame, textvariable=width_var)
        height_entry = ctk.CTkEntry(size_frame, textvariable=height_var)
        width_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(4, 0))
        height_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(4, 0))
        size_frame.grid_columnconfigure(0, weight=1)
        size_frame.grid_columnconfigure(1, weight=1)

        def on_save() -> None:
            new_data = {
                "appearance_mode": appearance_var.get(),
                "color_theme": theme_var.get(),
                "window_width": width_var.get(),
                "window_height": height_var.get(),
            }
            try:
                clean = _sanitize_settings(new_data)
                settings.update(clean)
                save_settings(settings)
                apply_settings_to_app(app, settings)
                dialog.destroy()
            except OSError as exc:
                messagebox.showerror("Settings", f"Failed to save settings:\n{exc}")

        buttons = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons.pack(fill="x", padx=12, pady=(16, 12))

        ctk.CTkButton(buttons, text="Cancel", fg_color="gray25", hover_color="gray35", command=dialog.destroy).pack(side="right")
        ctk.CTkButton(buttons, text="Save", command=on_save).pack(side="right", padx=(0, 8))

    settings_btn = ctk.CTkButton(
        header_frame,
        text="Settings",
        width=100,
        command=open_settings
    )
    settings_btn.pack(side="right")

    # Scrollable tools area
    tools_frame = ctk.CTkScrollableFrame(root_frame, label_text="Tools")
    tools_frame.pack(fill="both", expand=True)

    def refresh_tools() -> None:
        for widget in tools_frame.winfo_children():
            widget.destroy()
        populate_tools(tools_frame, app)

    refresh_btn = ctk.CTkButton(
        header_frame,
        text="↻",
        width=36,
        command=refresh_tools
    )
    refresh_btn.pack(side="right", padx=(0, 6))

    populate_tools(tools_frame, app)

    # Exit button
    exit_btn = ctk.CTkButton(
        root_frame,
        text="Close",
        fg_color="gray25",
        hover_color="gray35",
        command=app.destroy
    )
    exit_btn.pack(fill="x", pady=(10, 0))

    app.mainloop()


if __name__ == "__main__":
    main()
