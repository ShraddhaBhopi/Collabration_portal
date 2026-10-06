import customtkinter as ctk

from Frontend.pages.auth_page import AuthPage


class CollabCampusApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("CollabCampus")
        self.geometry("1100x700")
        self.minsize(900, 600)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.show_auth()

    def clear_window(self):

        for widget in self.winfo_children():
            widget.destroy()

    def show_auth(self):

        self.clear_window()

        AuthPage(
            self,
            self
        ).pack(
            fill="both",
            expand=True
        )


if __name__ == "__main__":

    app = CollabCampusApp()
    app.mainloop()