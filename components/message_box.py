import customtkinter as ctk


def show_message(
    parent,
    message,
    message_type="info"
):

    if message_type == "error":
        title = "Error"

    elif message_type == "success":
        title = "Success"

    else:
        title = "Information"

    dialog = ctk.CTkToplevel(parent)

    dialog.title(title)
    dialog.geometry("400x200")

    dialog.transient(parent)
    dialog.grab_set()

    ctk.CTkLabel(
        dialog,
        text=message,
        wraplength=350,
        font=("Arial", 15)
    ).pack(
        padx=25,
        pady=40
    )

    ctk.CTkButton(
        dialog,
        text="OK",
        width=100,
        command=dialog.destroy
    ).pack()