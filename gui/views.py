from database.queries import get_all_workers


class StartMainWindow:
    def __init__(self):
        self.workers = get_all_workers()
        self.window = get_main_window()