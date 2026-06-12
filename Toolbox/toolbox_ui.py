# toolbox_ui.py
import subprocess
import sys
from pathlib import Path

import customtkinter as ctk


# ---------- paths ----------


BASE_DIR = Path(__file__).resolve().parent
TOOLS_DIR = BASE_DIR.parent / "tools"


# ---------- process launcher ----------

def launch_vbs(vbs_path: Path) -> None:
    """
    Launch a VBS script in a detached way so it keeps running
    even if the Python UI is closed.
    """
    # Ensure absolute path
    vbs_path = vbs_path.resolve()

    # Use wscript for normal (non-console) execution
    # DETACHED_PROCESS makes it independent from this process
    DETACHED_PROCESS = 0x00000008

    subprocess.Popen(
        ["wscript.exe", str(vbs_path)],
        creationflags=DETACHED_PROCESS,
        close_fds=True
    )


# ---------- UI ----------

def build_tools_list() -> list[Path]:
    """
    Return a sorted list of .vbs files in /tools (top-level only).
    """
    if not TOOLS_DIR.exists():
        return []

    return sorted(p for p in TOOLS_DIR.iterdir() if p.suffix.lower() == ".vbs")


def build_folders_list() -> list[Path]:
    """
    Return a sorted list of sub-folders inside /tools.
    """
    if not TOOLS_DIR.exists():
        return []

    return sorted(p for p in TOOLS_DIR.iterdir() if p.is_dir())


def open_folder_picker(folder: Path, parent: ctk.CTk) -> None:
    """
    Open a top-level popup that lists all .vbs files in a sub-folder.
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

    scripts = sorted(p for p in folder.iterdir() if p.suffix.lower() == ".vbs")

    if not scripts:
        ctk.CTkLabel(scroll, text="No .vbs files in this folder.").pack(pady=10)
    else:
        for script in scripts:
            btn = ctk.CTkButton(
                scroll,
                text=script.stem,
                command=lambda p=script: (launch_vbs(p), popup.destroy())
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
    Add all top-level .vbs buttons and sub-folder buttons to tools_frame.
    """
    tools = build_tools_list()
    folders = build_folders_list()

    if not tools and not folders:
        ctk.CTkLabel(
            tools_frame,
            text=f"No .vbs files found in: {TOOLS_DIR}",
            anchor="w",
            justify="left"
        ).pack(padx=10, pady=10, fill="x")
        return

    # Top-level .vbs files
    for tool_path in tools:
        btn = ctk.CTkButton(
            tools_frame,
            text=tool_path.stem,
            command=lambda p=tool_path: launch_vbs(p)
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
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("VBS Toolbox")
    app.geometry("400x600")

    # Root frame
    root_frame = ctk.CTkFrame(app)
    root_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Title
    title_label = ctk.CTkLabel(
        root_frame,
        text="VBS Toolbox",
        font=ctk.CTkFont(size=20, weight="bold")
    )
    title_label.pack(pady=(0, 10))

    # Scrollable tools area
    tools_frame = ctk.CTkScrollableFrame(root_frame, label_text="Tools")
    tools_frame.pack(fill="both", expand=True)

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
