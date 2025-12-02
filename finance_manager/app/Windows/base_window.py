from customtkinter import CTkToplevel, CTkFrame


class BaseWindow(CTkToplevel):
    """Базовый класс для всех модальных окон"""

    def __init__(self, parent, title: str, width: int = 400, height: int = 500):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        self.grab_set()  # Делает окно модальным

        self.center_window(width, height)

        self.main_frame = CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def center_window(self, width: int, height: int):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
