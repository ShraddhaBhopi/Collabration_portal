import customtkinter as ctk


class Navbar(ctk.CTkFrame):

    def __init__(self, parent, title="CollabCampus"):

        super().__init__(
            parent,
            height=60,
            corner_radius=0
        )

        self.pack_propagate(False)

        ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 22, "bold")
        ).pack(
            side="left",
            padx=20
        )