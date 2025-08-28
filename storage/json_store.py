import json
from pathlib import Path


DATA_FILE = Path(__file__).parent /  "habits.json"
DATA_FILE = DATA_FILE.resolve()

def load_data():

    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
    except json.JSONDecodeError:
        print("Error: The file contains invalid JSON.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    
    return data

def save_data(data):

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        with DATA_FILE.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def init_store():
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open('w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    
    





class JsonHabitStorage:
    def __init__(self, path: str | Path): ... # TODO: remember file path
    def init(self) -> None: ... # TODO: create file if missing
    def list(self) -> List[Habit]: ... # TODO: load all habits
    def get(self, habit_id: str) -> Optional[Habit]: ...
    def create(self, habit: Habit) -> str: ... # TODO: append + persist
    def update(self, habit: Habit) -> None: ... # TODO: replace by id + persist
    def delete(self, habit_id: str) -> None: ...