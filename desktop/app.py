import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from storage.json_store import init_store, load_data, save_data
from models.habit import create_habit, mark_done
import utils

init_store()
habits = load_data()
today = utils.today_iso_date()

def add_habit_button_clicked():
    name = simpledialog.askstring("Add a Habit", "Please enter a name for your habit")
    if name is None:
        return
    name = name.strip()
    if not name:
        messagebox.showerror("Add Habit", "The name cannot be empty, please add a name")
        return
    description = simpledialog.askstring("Habit Description", "Please enter a description for your habit")

    if description is None:
        return
    description = description.strip()
    if not description:
        description = "No description"
    
    existing_ids = {h.get("id") for h in habits}
    habit_id = utils.make_id("hb")
    while habit_id in existing_ids:
        habit_id = utils.make_id("hb")
    create_habit_dict = create_habit(habit_id, name, description)
    
    habits.append(create_habit_dict)
    tick = "✓" if today in create_habit_dict.get("history", []) else "•"
    active_text = "Yes" if create_habit_dict.get("active", True) else "No"

    tatree.insert(
    "", "end",
    iid=create_habit_dict["id"],
    values=(create_habit_dict["name"], create_habit_dict.get("streak", 0), tick, active_text))

    refresh_total_habit()
    save_data(habits)

root = tk.Tk()
root.title("HabitTracker")
root.geometry("800x800")
root.minsize(800, 800)

menubar = tk.Menu(root)
root.config(menu=menubar)
file_menu = tk.Menu(menubar)

toolbar = tk.Frame(root)
toolbar.pack(side=tk.LEFT, fill=tk.X)
add_habit_button = tk.Button(toolbar,
                             text="Add Habit",
                             command=add_habit_button_clicked,
                             activebackground="blue",
                             activeforeground="white",
                             cursor="hand2")

add_habit_button.pack(padx=20, pady=20)




    

tablearea = tk.Frame(root)
tablearea.pack(fill=tk.BOTH, expand=True)
columns = ("name", "streak", "today", "active")
tatree = ttk.Treeview(tablearea, columns=columns, show="headings")
tatree.heading("name", text="Name")
tatree.heading("streak", text="Streak")
tatree.heading("today", text="Today")
tatree.heading("active", text="Active")
tatree.column("name",   width=450, anchor=tk.W,     stretch=True)
tatree.column("streak", width=90,  anchor=tk.CENTER, stretch=False)
tatree.column("today",  width=90,  anchor=tk.CENTER, stretch=False)
tatree.column("active", width=110, anchor=tk.CENTER, stretch=False)
scrollbar = tk.Scrollbar(tablearea, orient="vertical", command=tatree.yview)
tatree.configure(yscrollcommand=scrollbar.set)
for h in habits:
    tick = "✓" if today in h.get("history", []) else "•"
    active_text = "Yes" if h.get("active", True) else "No"
    tatree.insert("", "end", iid=h["id"], values=(h["name"], h.get("streak", 0), tick, active_text))
# later when inserting:
# tatree.insert("", "end", iid=habit["id"], values=(habit["name"], habit["streak"], tick, active_text))

tatree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

statusbar = tk.Frame(root)
statusbar.pack( side=tk.BOTTOM, fill=tk.X)
total_var = tk.StringVar()
tk.Label(statusbar, textvariable=total_var, anchor="w").pack(side=tk.LEFT, padx=8, pady=4)

def refresh_total_habit():
    total_var.set(f"Total Habits: {len(habits)}")

refresh_total_habit()

        


file_menu.add_command(
    label="Exit",
    command=root.destroy,
)

menubar.add_cascade(
    label="File",
    menu=file_menu,
    underline=0
)

root.mainloop()