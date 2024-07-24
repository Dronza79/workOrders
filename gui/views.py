from database.queries import get_all_workers, get_all_tasks
from .windows import get_main_window


class StartMainWindow:
    def __init__(self):
        self.workers = get_all_workers()
        self.tasks = get_all_tasks()
        self.window = get_main_window()
