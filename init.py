from storage.json_store import init_store, load_data, save_data
from models.habit import create_habit, mark_done
import utils



init_store()
habits = load_data()
today_date = utils.today_iso_date()

def add_habit():

    name = input("Please enter the name of the habit: ").strip()
    if not name:
        print("You must enter a name: ")
        return
    
    description = input("Please enter a description for the task").strip()
    if not description:
        description = "No description"

    existing_ids = {h.get("id") for h in habits}
    habit_id = utils.make_id("hb")
    while habit_id in existing_ids:
        habit_id = utils.make_id("hb")

    new_habit = create_habit(habit_id, name, description)
    habits.append(new_habit)
    print(f"Wonky code actually worked, added the new habit: {name}")

def list_habits():
    if not habits:
        print("No Habits have been created yet")
        return
    for i, h in enumerate(habits, start=1):
        done_today = today_date in h.get("history", [])
        tick = "✓" if done_today else "•"
        print(f"{i}. {h.get('name','(unnamed)')} | Streak: {h.get('streak',0)} | Today: {tick}")

def mark_done_today():
    if not habits:
        print("There are no habits to choose from")
        return
    list_habits()
    selection = input("Please select a Habit to mark as completed").strip()
    if selection.lower() == "q": return()
    if not selection.isdigit():
        print("You must select a number")
        return
    n = int(selection)
    if n < 1 or n > len(habits):
        print("That number is not in the list")
        return
    index = n - 1
    h = habits[index]
    status = mark_done(h, today_date)
    if status == "already_done":
        print("Already marked today")
    else: 
        print("Marked complete for today")
    list_habits()






