import utils

def create_habit(habit_id, name, description):
    new_dict = {
    "id": habit_id,
    "name": name,
    "description": description,
    "created_at": utils.today_iso_date(),
    "last_checked": None,
    "history": [],
    "streak": 0,
    "active": True
    }
    return new_dict

def mark_done(habit, on_date):
    if on_date in habit["history"]:
        return "already_done"
    else:
        habit["history"].append(on_date)
        habit["last_checked"] = on_date
        habit["streak"] = utils.compute_streak(habit["history"], on_date)
        return "done"
    



def recalculate_streak():
    pass

def normal_history():
    pass

