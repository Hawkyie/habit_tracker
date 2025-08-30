import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkinter.font as tkfont

from storage.json_store import init_store, load_data, save_data
from models.habit import create_habit, mark_done
import utils

init_store()
habits = load_data()
today = utils.today_iso_date()

def add_btn_clicked():
    name = simpledialog.askstring("Add a Habit", "Please enter a name for your habit", parent=root)
    if name is None:
        return
    name = name.strip()
    if not name:
        messagebox.showerror("Add Habit", "This is not my wonky code wonking, you didn't enter a name. Do it.", parent=root)
        return
    
    description = simpledialog.askstring("Habit Description", "Please enter a description for your habit", parent=root)
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

    item_id = create_habit_dict["id"]
    tatree.selection_set(item_id)
    tatree.focus(item_id)
    tatree.see(item_id)
    set_description(create_habit_dict.get("description",""))

    refresh_total_habit()
    save_data(habits)

def done_btn_clicked():
    selected_items = tatree.selection()
    if not selected_items:
        messagebox.showinfo("Nothing selected", "You didn't select anything", parent=root)
        return
    
    for iid in selected_items:
        habit = next((h for h in habits if h.get("id") == iid), None)
        if habit is None:
            continue

        status =  mark_done(habit, today)
        if status == "done":
            tatree.set(iid, "today", "✓")
            tatree.set(iid, "streak", habit.get("streak", 0))
    
    save_data(habits)

def edit_btn_clicked():
    selected_items = tatree.selection()
    if len(selected_items) !=1:
        messagebox.showinfo("Too many", "Greedy", parent=root)
        return
    iid = selected_items[0]
    habit = next((h for h in habits if h.get("id") == iid), None)
    if habit is None:
        return
    
    name = simpledialog.askstring("Edit Habit", "Please specify the Habit name", initialvalue=habit.get("name", ""), parent=root)
    if name is None:
        return
    name = name.strip()
    if not name:
        messagebox.showerror("Edit Habit", "This is not my wonky code wonking, you didn't enter a name. Do it.", parent=root)
        return
    habit["name"] = name
    tatree.set(iid, "name", name)
    
    description = simpledialog.askstring("Habit Description", "Please enter a description for your habit", initialvalue=habit.get("description", ""), parent=root)
    if description is None:
        return
    habit["description"] = description.strip() or "No description"
    
    set_description(habit["description"])
    save_data(habits)

def tgl_btn_clicked():
    selected_items = tatree.selection()
    if len(selected_items) !=1:
        messagebox.showinfo("Select one", "Please select exactly one habit.", parent=root)
        return
    iid = selected_items[0]
    habit = next((h for h in habits if h.get("id") == iid), None)
    if habit is None:
        return
    habit["active"] = not habit.get("active", True)
    tatree.set(iid, "active", "Yes" if habit["active"] else "No")

    save_data(habits)

def del_btn_clicked():
    selected_items = tatree.selection()
    if len(selected_items) !=1:
        messagebox.showinfo("We are showing you this", "You did something wrong, this is a feature not a bug", parent=root)
        return
    iid = selected_items[0]
    habit = next((h for h in habits if h.get("id") == iid), None)
    if habit is None:
        return
    else:
        ok = messagebox.askyesno("To delete or not to delete", "Are you sure you want to delete this habit?", parent=root)
        if not ok: return
        habits.remove(habit)

    tatree.delete(iid)
    refresh_total_habit()
    on_selection_change()
    save_data(habits)

def save_btn_clicked():
    try:
        save_data(habits)
    except Exception as e:
        messagebox.showerror("The wonky code is wonking :/", str(e), parent=root)
        return
    else:
        save_var.set("Saved just now")
        root.after(10000, lambda: save_var.set(""))

def set_description(text: str):
    description_text.configure(state="normal")
    description_text.delete("1.0", "end")
    description_text.insert("1.0", text or "")
    description_text.configure(state="disabled")

root = tk.Tk()
tkfont.nametofont("TkDefaultFont").configure(family="Segoe UI", size=10)
tkfont.nametofont("TkTextFont").configure(family="Segoe UI", size=10)
tkfont.nametofont("TkHeadingFont").configure(family="Segoe UI", size=10, weight="bold")
tkfont.nametofont("TkMenuFont").configure(family="Segoe UI", size=10)
tkfont.nametofont("TkFixedFont").configure(family="Consolas", size=10)

root.title("HabitTracker")
root.geometry("800x800")
root.minsize(800, 800)

menubar = tk.Menu(root)
root.config(menu=menubar)
file_menu = tk.Menu(menubar)

toolbar = ttk.Frame(root)
toolbar.pack(side=tk.TOP, fill=tk.X)
btn_row = ttk.Frame(toolbar)
btn_row.pack()
add_btn = ttk.Button(btn_row,
                    text="Add Habit",
                    command=add_btn_clicked,
                    cursor="hand2")
add_btn.pack(side=tk.LEFT, padx=16, pady=6)

done_btn = ttk.Button(btn_row,
                     text="Mark done today",
                    state=tk.DISABLED,
                    command=done_btn_clicked,
                    cursor="hand2")
done_btn.pack(side=tk.LEFT, padx=16, pady=6)

edit_btn = ttk.Button(btn_row,
                     text="Edit",
                     state=tk.DISABLED,
                     command=edit_btn_clicked,
                     cursor="hand2")
edit_btn.pack(side=tk.LEFT, padx=16, pady=6)

tgl_btn = ttk.Button(btn_row,
                    text="Archive/Unarchive",
                    state=tk.DISABLED,
                    command=tgl_btn_clicked,
                    cursor="hand2")
tgl_btn.pack(side=tk.LEFT, padx=16, pady=6)

del_btn = ttk.Button(btn_row,
                    text="Delete",
                    state=tk.DISABLED,
                    command=del_btn_clicked,
                    cursor="hand2")
del_btn.pack(side=tk.LEFT, padx=16, pady=6)

save_btn = ttk.Button(btn_row,
                     text="Save",
                     command=save_btn_clicked,
                     cursor="hand2")
save_btn.pack(side=tk.LEFT, padx=16, pady=6)

def on_selection_change(event=None):
    selected_items = tatree.selection()

    if selected_items and len(selected_items) > 1:
        done_btn.config(state=tk.NORMAL)
        edit_btn.config(state=tk.DISABLED)
        tgl_btn.config(state=tk.DISABLED)
        del_btn.config(state=tk.DISABLED)

    elif selected_items and len(selected_items) == 1:
        done_btn.config(state=tk.NORMAL)
        edit_btn.config(state=tk.NORMAL)
        tgl_btn.config(state=tk.NORMAL)
        del_btn.config(state=tk.NORMAL)
    else:
        done_btn.config(state=tk.DISABLED)
        edit_btn.config(state=tk.DISABLED)
        tgl_btn.config(state=tk.DISABLED)
        del_btn.config(state=tk.DISABLED)

    if selected_items and len(selected_items) == 1:
        iid = selected_items[0]
        habit = next((h for h in habits if h.get("id") == iid), None)
        set_description(habit.get("description", "") if habit else "")
    elif selected_items:
        set_description("Multiple items selected.")
    else:
        set_description("Select a habit to see details.")

tablearea = ttk.Frame(root)
tablearea.pack(fill=tk.BOTH, expand=True)
columns = ("name", "streak", "today", "active")
tatree = ttk.Treeview(tablearea, columns=columns, show="headings")
tatree.heading("name", text="Name")
tatree.heading("streak", text="Streak")
tatree.heading("today", text="Today")
tatree.heading("active", text="Active")
tatree.column("name",   width=200, anchor=tk.W, stretch=True)
tatree.column("streak", width=90,  anchor=tk.CENTER, stretch=False)
tatree.column("today",  width=90,  anchor=tk.CENTER, stretch=False)
tatree.column("active", width=110, anchor=tk.CENTER, stretch=False)
scrollbar = ttk.Scrollbar(tablearea, orient="vertical", command=tatree.yview)
tatree.configure(yscrollcommand=scrollbar.set)
for h in habits:
    tick = "✓" if today in h.get("history", []) else "•"
    active_text = "Yes" if h.get("active", True) else "No"
    tatree.insert("", "end", iid=h["id"], values=(h["name"], h.get("streak", 0), tick, active_text))

details = ttk.LabelFrame(root, text="Details")
details.pack(fill=tk.X, padx=8, pady=6)

description_text = tk.Text(details, height=5, wrap="word", borderwidth=0)
details_font = tkfont.Font(family="Segoe UI", size=10)
description_text.configure(state="disabled", font=details_font)
description_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8, pady=6)
description_scroll = ttk.Scrollbar(details, orient="vertical", command=description_text.yview)
description_text.configure(yscrollcommand=description_scroll.set)
description_scroll.pack(side=tk.RIGHT, fill=tk.Y)
tatree.bind("<<TreeviewSelect>>", on_selection_change)
on_selection_change()

tatree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

statusbar = ttk.Frame(root)
statusbar.pack( side=tk.BOTTOM, fill=tk.X)
save_var = tk.StringVar()
ttk.Label(statusbar, textvariable=save_var, anchor="w").pack(side=tk.RIGHT, padx=8, pady=4)
total_var = tk.StringVar()
ttk.Label(statusbar, textvariable=total_var, anchor="w").pack(side=tk.LEFT, padx=8, pady=4)

def refresh_total_habit():
    total_var.set(f"Total Habits: {len(habits)}")

refresh_total_habit()

menubar.add_cascade(
    label="File",
    menu=file_menu,
    underline=0
)

file_menu.add_command(
    label="Exit",
    command=root.destroy,
)


root.mainloop()