import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x150")
        self.title("Money Manager")


