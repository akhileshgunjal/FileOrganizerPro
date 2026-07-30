import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime

from organizer import organize_folder
from logger import write_log
from undo import undo_last_operation
from report import generate_report
from search import search_files
from settings import get_default_settings

# ==========================================
# APP SETTINGS
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

selected_folder = ""
current_stats = {}
current_total = 0

enabled_categories = get_default_settings()


# ==========================================
# ACTIVITY LOG
# ==========================================

def add_log(message):

    current_time = datetime.now().strftime("%H:%M:%S")

    log_box.configure(state="normal")

    log_box.insert(
        "end",
        f"[{current_time}] {message}\n"
    )

    log_box.see("end")

    log_box.configure(state="disabled")


# ==========================================
# BROWSE FOLDER
# ==========================================

def browse_folder():

    global selected_folder

    folder = filedialog.askdirectory()

    if folder:

        selected_folder = folder

        folder_label.configure(
            text=folder
        )

        status_label.configure(
            text="Ready"
        )

        add_log(
            f"Selected folder: {folder}"
        )


# ==========================================
# ORGANIZE FILES
# ==========================================

def organize():

    global current_stats
    global current_total

    if not selected_folder:

        messagebox.showwarning(
            "Warning",
            "Please select a folder first."
        )

        return

    try:

        status_label.configure(
            text="Organizing..."
        )

        progress.set(0.2)

        app.update()

        total, stats, moved_files = organize_folder(
            selected_folder,
            enabled_categories
        )  
    

        current_stats = stats
        current_total = total

        progress.set(1.0)

        total_value.configure(
            text=str(total)
        )

        images_value.configure(
            text=str(stats.get("Images", 0))
        )

        documents_value.configure(
            text=str(stats.get("Documents", 0))
        )

        pdfs_value.configure(
            text=str(stats.get("PDFs", 0))
        )

        videos_value.configure(
            text=str(stats.get("Videos", 0))
        )

        audio_value.configure(
            text=str(stats.get("Audio", 0))
        )

        archives_value.configure(
            text=str(stats.get("Archives", 0))
        )

        programs_value.configure(
            text=str(stats.get("Programs", 0))
        )

        others_value.configure(
            text=str(stats.get("Others", 0))
        )

        add_log(
            "Organization started"
        )

        write_log(
            "Organization started"
        )

        for file, category in moved_files:

            message = (
                f"Moved {file} → {category}"
            )

            add_log(message)
            write_log(message)

        completion_message = (
            f"Completed — {total} files organized"
        )

        add_log(completion_message)
        write_log(completion_message)

        status_label.configure(
            text="Completed ✅"
        )

        messagebox.showinfo(
            "Success",
            f"{total} files organized successfully!"
        )

    except Exception as error:

        error_message = (
            f"ERROR: {error}"
        )

        add_log(error_message)
        write_log(error_message)

        status_label.configure(
            text="Error ❌"
        )

        messagebox.showerror(
            "Error",
            str(error)
        )


# ==========================================
# UNDO
# ==========================================

def undo():

    try:

        restored = undo_last_operation()

        if restored == 0:

            messagebox.showinfo(
                "Undo",
                "There is no organization to undo."
            )

            return

        message = (
            f"Undo completed — "
            f"{restored} files restored"
        )

        add_log(message)
        write_log(message)

        status_label.configure(
            text="Undo Completed ↩️"
        )

        progress.set(0)

        messagebox.showinfo(
            "Undo Successful",
            f"{restored} files restored successfully!"
        )

    except Exception as error:

        error_message = (
            f"Undo ERROR: {error}"
        )

        add_log(error_message)
        write_log(error_message)

        status_label.configure(
            text="Undo Error ❌"
        )

        messagebox.showerror(
            "Undo Error",
            str(error)
        )


# ==========================================
# GENERATE REPORT
# ==========================================

def create_report():

    if not selected_folder:

        messagebox.showwarning(
            "Warning",
            "Please organize a folder first."
        )

        return

    if current_total == 0:

        messagebox.showwarning(
            "Warning",
            "Please organize files before generating a report."
        )

        return

    try:

        report_file = generate_report(
            selected_folder,
            current_stats,
            current_total
        )

        message = (
            f"Report generated: {report_file}"
        )

        add_log(message)
        write_log(message)

        messagebox.showinfo(
            "Report Generated",
            "Report successfully created!"
        )

    except Exception as error:

        error_message = (
            f"Report ERROR: {error}"
        )

        add_log(error_message)
        write_log(error_message)

        messagebox.showerror(
            "Report Error",
            str(error)
        )


# ==========================================
# SEARCH
# ==========================================

def perform_search():

    if not selected_folder:

        messagebox.showwarning(
            "Warning",
            "Please select a folder first."
        )

        return

    query = search_entry.get().strip()

    if not query:

        messagebox.showwarning(
            "Warning",
            "Please enter a file name or extension."
        )

        return

    try:

        results = search_files(
            selected_folder,
            query
        )

        search_results.configure(
            state="normal"
        )

        search_results.delete(
            "1.0",
            "end"
        )

        if not results:

            search_results.insert(
                "end",
                f"No files found for: {query}\n"
            )

            add_log(
                f"Search: no results for '{query}'"
            )

        else:

            search_results.insert(
                "end",
                f"Found {len(results)} file(s) for '{query}':\n\n"
            )

            for result in results:

                search_results.insert(
                    "end",
                    f"📄 {result.name}\n"
                    f"📂 {result}\n\n"
                )

            add_log(
                f"Search: found {len(results)} file(s) for '{query}'"
            )

        search_results.configure(
            state="disabled"
        )

    except Exception as error:

        add_log(
            f"Search ERROR: {error}"
        )

        messagebox.showerror(
            "Search Error",
            str(error)
        )


# ==========================================
# OPEN SEARCHED FILE
# ==========================================

def open_selected_file(event):

    try:

        index = search_results.index(
            f"@{event.x},{event.y}"
        )

        line_start = search_results.index(
            f"{index} linestart"
        )

        line_end = search_results.index(
            f"{index} lineend"
        )

        line_text = search_results.get(
            line_start,
            line_end
        ).strip()

        if line_text.startswith("📄 "):

            file_name = line_text[2:].strip()

            results = search_files(
                selected_folder,
                file_name
            )

            for result in results:

                if result.name == file_name:

                    import os

                    os.startfile(
                        result.resolve()
                    )

                    break

    except Exception as error:

        add_log(
            f"Open file ERROR: {error}"
        )

# ==========================================
# TOGGLE DARK / LIGHT MODE
# ==========================================

def toggle_theme():

    if theme_switch.get() == 1:

        ctk.set_appearance_mode("dark")

        add_log("Dark mode enabled")

    else:

        ctk.set_appearance_mode("light")

        add_log("Light mode enabled")

# ==========================================
# SETTINGS WINDOW
# ==========================================

def open_settings():

    global enabled_categories

    settings_window = ctk.CTkToplevel(app)

    settings_window.title(
        "Settings - File Organizer Pro"
    )

    settings_window.geometry(
        "420x560"
    )

    settings_window.resizable(
        False,
        False
    )

    # -----------------------------
    # Title
    # -----------------------------

    title = ctk.CTkLabel(
        settings_window,
        text="⚙️ Settings",
        font=("Segoe UI", 24, "bold")
    )

    title.pack(
        pady=(25, 5)
    )

    subtitle = ctk.CTkLabel(
        settings_window,
        text="Choose categories to organize",
        font=("Segoe UI", 11),
        text_color="gray"
    )

    subtitle.pack(
        pady=(0, 20)
    )

    # -----------------------------
    # Categories
    # -----------------------------

    settings_frame = ctk.CTkFrame(
        settings_window
    )

    settings_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=5
    )

    categories = [
        "Images",
        "Documents",
        "PDFs",
        "Videos",
        "Audio",
        "Archives",
        "Programs",
        "Others"
    ]

    checkboxes = {}

    for category in categories:

        variable = ctk.BooleanVar(
            value=enabled_categories.get(
                category,
                True
            )
        )

        checkbox = ctk.CTkCheckBox(
            settings_frame,
            text=category,
            variable=variable,
            font=("Segoe UI", 13)
        )

        checkbox.pack(
            anchor="w",
            padx=25,
            pady=7
        )

        checkboxes[category] = variable

    # -----------------------------
    # Save
    # -----------------------------

    def save_settings():

        global enabled_categories

        for category in categories:

            enabled_categories[category] = (
                checkboxes[category].get()
            )

        add_log(
            "Settings updated successfully"
        )

        messagebox.showinfo(
            "Settings",
            "Settings saved successfully!"
        )

        settings_window.destroy()

    save_button = ctk.CTkButton(
        settings_window,
        text="💾 SAVE SETTINGS",
        command=save_settings,
        width=220,
        height=45,
        font=("Segoe UI", 13, "bold")
    )

    save_button.pack(
        pady=20
    )

# ==========================================
# MENU BAR FUNCTIONS
# ==========================================

def menu_open_folder():
    browse_folder()


def menu_generate_report():
    create_report()


def menu_undo():
    undo()


def menu_exit():
    app.destroy()


def show_about():

    about_window = ctk.CTkToplevel(app)

    about_window.title(
        "About File Organizer Pro"
    )

    about_window.geometry(
        "450x400"
    )

    about_window.resizable(
        False,
        False
    )

    about_window.transient(app)
    about_window.grab_set()

    # Title
    ctk.CTkLabel(
        about_window,
        text="📁 File Organizer Pro",
        font=("Segoe UI", 25, "bold")
    ).pack(
        pady=(35, 10)
    )

    ctk.CTkLabel(
        about_window,
        text="Version 1.0",
        font=("Segoe UI", 12),
        text_color="gray"
    ).pack(
        pady=3
    )

    ctk.CTkLabel(
        about_window,
        text=(
            "An intelligent desktop application\n"
            "for automatically organizing files."
        ),
        font=("Segoe UI", 13),
        justify="center"
    ).pack(
        pady=20
    )

    ctk.CTkLabel(
        about_window,
        text=(
            "Developed using Python + CustomTkinter\n\n"
            "Features:\n"
            "• Automatic file organization\n"
            "• Search\n"
            "• Statistics\n"
            "• Undo\n"
            "• Reports\n"
            "• Activity logs\n"
            "• Custom settings\n"
            "• Dark / Light mode"
        ),
        font=("Segoe UI", 11),
        justify="left"
    ).pack(
        pady=5
    )

    ctk.CTkButton(
        about_window,
        text="Close",
        command=about_window.destroy,
        width=140,
        height=38
    ).pack(
        pady=20
    )

# ==========================================
# MAIN WINDOW
# ==========================================

app = ctk.CTk()

# ==========================================
# MENU BAR
# ==========================================

menu_bar = ctk.CTkFrame(
    app,
    height=35,
    corner_radius=0
)

menu_bar.pack(
    fill="x",
    side="top"
)


file_menu = ctk.CTkOptionMenu(
    menu_bar,
    values=[
        "File",
        "Open Folder",
        "Generate Report",
        "Undo",
        "Exit"
    ],
    command=lambda choice: {
        "Open Folder": menu_open_folder,
        "Generate Report": menu_generate_report,
        "Undo": menu_undo,
        "Exit": menu_exit
    }.get(choice, lambda: None)(),
    width=110,
    height=30
)

file_menu.set("File")

file_menu.pack(
    side="left",
    padx=5,
    pady=2
)


tools_menu = ctk.CTkOptionMenu(
    menu_bar,
    values=[
        "Tools",
        "Settings",
        "Dark Mode",
        "Light Mode"
    ],
    command=lambda choice: {
        "Settings": open_settings,
        "Dark Mode": lambda: ctk.set_appearance_mode("dark"),
        "Light Mode": lambda: ctk.set_appearance_mode("light")
    }.get(choice, lambda: None)(),
    width=110,
    height=30
)

tools_menu.set("Tools")

tools_menu.pack(
    side="left",
    padx=5,
    pady=2
)


help_menu = ctk.CTkOptionMenu(
    menu_bar,
    values=[
        "Help",
        "About"
    ],
    command=lambda choice: {
        "About": show_about
    }.get(choice, lambda: None)(),
    width=110,
    height=30
)

help_menu.set("Help")

help_menu.pack(
    side="left",
    padx=5,
    pady=2
)

app.title(
    "File Organizer Pro"
)

app.geometry(
    "1100x700"
)

app.minsize(
    900,
    650
)

app.resizable(
    True,
    True
)


# ==========================================
# TITLE
# ==========================================

title = ctk.CTkLabel(
    app,
    text="📁 File Organizer Pro",
    font=("Segoe UI", 28, "bold")
)

title.pack(
    pady=(15, 0)
)


subtitle = ctk.CTkLabel(
    app,
    text="Intelligent Desktop File Management System",
    font=("Segoe UI", 12),
    text_color="gray"
)

subtitle.pack(
    pady=(0, 10)
)

# ==========================================
# THEME SWITCH
# ==========================================

theme_switch = ctk.CTkSwitch(
    app,
    text="🌙 Dark Mode",
    command=toggle_theme,
    font=("Segoe UI", 11, "bold")
)

theme_switch.pack(
    anchor="ne",
    padx=35,
    pady=(0, 5)
)

theme_switch.select()


# ==========================================
# FOLDER SECTION
# ==========================================

folder_frame = ctk.CTkFrame(
    app
)

folder_frame.pack(
    fill="x",
    padx=30,
    pady=5
)


folder_label = ctk.CTkLabel(
    folder_frame,
    text="No folder selected",
    anchor="w",
    font=("Segoe UI", 12)
)

folder_label.pack(
    side="left",
    padx=15,
    pady=10
)


browse_button = ctk.CTkButton(
    folder_frame,
    text="📂 BROWSE",
    command=browse_folder,
    width=160,
    height=38,
    font=("Segoe UI", 12, "bold")
)

browse_button.pack(
    side="right",
    padx=15,
    pady=8
)


# ==========================================
# TOTAL FILES
# ==========================================

total_frame = ctk.CTkFrame(
    app
)

total_frame.pack(
    fill="x",
    padx=30,
    pady=5
)


ctk.CTkLabel(
    total_frame,
    text="TOTAL FILES ORGANIZED",
    font=("Segoe UI", 11)
).pack(
    pady=(5, 0)
)


total_value = ctk.CTkLabel(
    total_frame,
    text="0",
    font=("Segoe UI", 24, "bold")
)

total_value.pack(
    pady=(0, 5)
)


# ==========================================
# STATISTICS
# ==========================================

ctk.CTkLabel(
    app,
    text="📊 File Statistics",
    font=("Segoe UI", 17, "bold")
).pack(
    anchor="w",
    padx=35,
    pady=(5, 2)
)


stats_frame = ctk.CTkFrame(
    app
)

stats_frame.pack(
    fill="x",
    padx=30,
    pady=2
)


def create_card(parent, title):

    card = ctk.CTkFrame(
        parent,
        height=65
    )

    card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=3,
        pady=5
    )

    ctk.CTkLabel(
        card,
        text=title,
        font=("Segoe UI", 10)
    ).pack(
        pady=(5, 0)
    )

    value = ctk.CTkLabel(
        card,
        text="0",
        font=("Segoe UI", 17, "bold")
    )

    value.pack(
        pady=(0, 4)
    )

    return value


images_value = create_card(
    stats_frame,
    "🖼 Images"
)

documents_value = create_card(
    stats_frame,
    "📄 Documents"
)

pdfs_value = create_card(
    stats_frame,
    "📕 PDFs"
)

videos_value = create_card(
    stats_frame,
    "🎬 Videos"
)

audio_value = create_card(
    stats_frame,
    "🎵 Audio"
)

archives_value = create_card(
    stats_frame,
    "📦 Archives"
)

programs_value = create_card(
    stats_frame,
    "💻 Programs"
)

others_value = create_card(
    stats_frame,
    "📁 Others"
)


# ==========================================
# PROGRESS
# ==========================================

progress = ctk.CTkProgressBar(
    app,
    height=10
)

progress.pack(
    fill="x",
    padx=40,
    pady=6
)

progress.set(0)


# ==========================================
# STATUS
# ==========================================

status_frame = ctk.CTkFrame(
    app
)

status_frame.pack(
    fill="x",
    padx=30,
    pady=2
)


ctk.CTkLabel(
    status_frame,
    text="Status:",
    font=("Segoe UI", 11, "bold")
).pack(
    side="left",
    padx=12,
    pady=5
)


status_label = ctk.CTkLabel(
    status_frame,
    text="Waiting...",
    font=("Segoe UI", 11)
)

status_label.pack(
    side="left"
)


# ==========================================
# SEARCH
# ==========================================

search_title = ctk.CTkLabel(
    app,
    text="🔎 Search Files",
    font=("Segoe UI", 17, "bold")
)

search_title.pack(
    anchor="w",
    padx=35,
    pady=(5, 2)
)


search_frame = ctk.CTkFrame(
    app
)

search_frame.pack(
    fill="x",
    padx=30,
    pady=2
)


search_entry = ctk.CTkEntry(
    search_frame,
    placeholder_text="Enter file name or extension...",
    height=38,
    font=("Segoe UI", 12)
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=8,
    pady=7
)


search_button = ctk.CTkButton(
    search_frame,
    text="🔎 SEARCH",
    command=perform_search,
    width=150,
    height=38,
    font=("Segoe UI", 12, "bold")
)

search_button.pack(
    side="right",
    padx=8,
    pady=7
)


# ==========================================
# SEARCH RESULTS
# ==========================================

search_results = ctk.CTkTextbox(
    app,
    height=55,
    font=("Segoe UI", 11)
)

search_results.pack(
    fill="x",
    padx=30,
    pady=(2, 3)
)

search_results.configure(
    state="disabled"
)

search_results.bind(
    "<Double-Button-1>",
    open_selected_file
)


# ==========================================
# MAIN BUTTONS
# ==========================================

button_frame = ctk.CTkFrame(
    app
)

button_frame.pack(
    fill="x",
    padx=30,
    pady=4
)


organize_button = ctk.CTkButton(
    button_frame,
    text="📂 ORGANIZE",
    command=organize,
    width=180,
    height=42,
    font=("Segoe UI", 12, "bold")
)

organize_button.pack(
    side="left",
    expand=True,
    padx=6,
    pady=7
)


undo_button = ctk.CTkButton(
    button_frame,
    text="↩️ UNDO",
    command=undo,
    width=150,
    height=42,
    font=("Segoe UI", 12, "bold"),
    fg_color="orange",
    hover_color="darkorange"
)

undo_button.pack(
    side="left",
    expand=True,
    padx=6,
    pady=7
)


report_button = ctk.CTkButton(
    button_frame,
    text="📄 REPORT",
    command=create_report,
    width=170,
    height=42,
    font=("Segoe UI", 12, "bold")
)

report_button.pack(
    side="left",
    expand=True,
    padx=6,
    pady=7
)


exit_button = ctk.CTkButton(
    button_frame,
    text="✖ EXIT",
    command=app.destroy,
    width=130,
    height=42,
    font=("Segoe UI", 12, "bold"),
    fg_color="red",
    hover_color="darkred"
)

exit_button.pack(
    side="left",
    expand=True,
    padx=6,
    pady=7
)

# ==========================================
# SETTINGS BUTTON
# ==========================================

settings_button = ctk.CTkButton(
    app,
    text="⚙️ SETTINGS",
    command=open_settings,
    width=150,
    height=35,
    font=("Segoe UI", 11, "bold")
)

settings_button.pack(
    pady=(0, 3)
)

# ==========================================
# ACTIVITY LOG
# ==========================================

log_title = ctk.CTkLabel(
    app,
    text="📋 Activity Log",
    font=("Segoe UI", 15, "bold")
)

log_title.pack(
    anchor="w",
    padx=35,
    pady=(2, 0)
)


log_box = ctk.CTkTextbox(
    app,
    height=55,
    font=("Consolas", 10)
)

log_box.pack(
    fill="x",
    padx=30,
    pady=(2, 3)
)

log_box.configure(
    state="disabled"
)


# ==========================================
# FOOTER
# ==========================================

footer = ctk.CTkLabel(
    app,
    text="File Organizer Pro • Python + CustomTkinter",
    text_color="gray",
    font=("Segoe UI", 9)
)

footer.pack(
    pady=2
)


# ==========================================
# START APP
# ==========================================

app.mainloop()