import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        buttons=None
    ):

        super().__init__(
            parent,
            width=200,
            corner_radius=0
        )

        self.pack_propagate(False)

        ctk.CTkLabel(
            self,
            text="Menu",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(25, 20)
        )

        if buttons:

            for button_text, command in buttons:

                ctk.CTkButton(
                    self,
                    text=button_text,
                    command=command,
                    width=160
                ).pack(
                    pady=6
                )