import customtkinter as ctk
from Backend.auth import login_user, register_user


class AuthPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app
        self.configure(fg_color="#F5F7FB")

        self.create_page()

    # ---------------------------------------------------------
    # MAIN PAGE
    # ---------------------------------------------------------

    def create_page(self):
        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        container.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # LEFT BRANDING PANEL
        # -----------------------------------------------------

        left_panel = ctk.CTkFrame(
            container,
            width=420,
            corner_radius=0,
            fg_color="#1976D2"
        )
        left_panel.pack(
            side="left",
            fill="y"
        )
        left_panel.pack_propagate(False)

        ctk.CTkLabel(
            left_panel,
            text="👥",
            font=("Arial", 55)
        ).pack(pady=(120, 10))

        ctk.CTkLabel(
            left_panel,
            text="CollabCampus",
            font=("Arial", 34, "bold"),
            text_color="white"
        ).pack()

        ctk.CTkLabel(
            left_panel,
            text="College Collaboration\n& Team Formation",
            font=("Arial", 17),
            text_color="#E3F2FD",
            justify="center"
        ).pack(pady=(10, 30))

        features = [
            "✓  Find teammates",
            "✓  Discover projects",
            "✓  Manage team tasks",
            "✓  Collaborate with students"
        ]

        for feature in features:
            ctk.CTkLabel(
                left_panel,
                text=feature,
                font=("Arial", 13),
                text_color="white"
            ).pack(
                anchor="w",
                padx=80,
                pady=7
            )

        # -----------------------------------------------------
        # RIGHT LOGIN PANEL
        # -----------------------------------------------------

        right_panel = ctk.CTkFrame(
            container,
            fg_color="#F5F7FB"
        )
        right_panel.pack(
            side="left",
            fill="both",
            expand=True
        )

        card = ctk.CTkFrame(
            right_panel,
            width=430,
            fg_color="white",
            corner_radius=18,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        ctk.CTkLabel(
            card,
            text="Welcome back 👋",
            font=("Arial", 27, "bold"),
            text_color="#202124"
        ).pack(
            pady=(35, 5)
        )

        ctk.CTkLabel(
            card,
            text="Login to continue to CollabCampus",
            font=("Arial", 13),
            text_color="#6B7280"
        ).pack(
            pady=(0, 25)
        )

        # Email
        ctk.CTkLabel(
            card,
            text="Email",
            font=("Arial", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=35,
            pady=(0, 5)
        )

        self.email_entry = ctk.CTkEntry(
            card,
            width=360,
            height=42,
            placeholder_text="Enter your email"
        )
        self.email_entry.pack(
            padx=35
        )

        # Password
        ctk.CTkLabel(
            card,
            text="Password",
            font=("Arial", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=35,
            pady=(18, 5)
        )

        self.password_entry = ctk.CTkEntry(
            card,
            width=360,
            height=42,
            placeholder_text="Enter your password",
            show="*"
        )
        self.password_entry.pack(
            padx=35
        )

        # Role
        ctk.CTkLabel(
            card,
            text="Role",
            font=("Arial", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=35,
            pady=(18, 5)
        )

        self.role_menu = ctk.CTkOptionMenu(
            card,
            width=360,
            height=42,
            values=["student", "faculty"],
            fg_color="#1976D2",
            button_color="#1565C0",
            button_hover_color="#0D47A1"
        )
        self.role_menu.pack(
            padx=35
        )

        # Message
        self.message = ctk.CTkLabel(
            card,
            text="",
            font=("Arial", 12),
            wraplength=350
        )
        self.message.pack(
            pady=(15, 5)
        )

        # Buttons
        ctk.CTkButton(
            card,
            text="Login",
            width=360,
            height=42,
            corner_radius=9,
            font=("Arial", 14, "bold"),
            command=self.login
        ).pack(
            padx=35,
            pady=(5, 8)
        )

        ctk.CTkButton(
            card,
            text="Create New Account",
            width=360,
            height=40,
            corner_radius=9,
            fg_color="white",
            text_color="#1976D2",
            border_width=1,
            border_color="#1976D2",
            hover_color="#EFF6FF",
            command=self.register
        ).pack(
            padx=35,
            pady=(0, 30)
        )

    # ---------------------------------------------------------
    # LOGIN
    # ---------------------------------------------------------

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            self.message.configure(
                text="Please enter your email and password.",
                text_color="#B91C1C"
            )
            return

        try:
            user = login_user(
                email,
                password
            )

        except Exception as error:
            self.message.configure(
                text=f"Database error: {error}",
                text_color="#B91C1C"
            )
            return

        if user is None:
            self.message.configure(
                text="Invalid email or password.",
                text_color="#B91C1C"
            )
            return

        self.open_dashboard(user)

    # ---------------------------------------------------------
    # OPEN DASHBOARD
    # ---------------------------------------------------------

    def open_dashboard(self, user):
        self.destroy()

        if user["role"] == "student":
            from Frontend.pages.student_dashboard import StudentDashboard

            StudentDashboard(
                self.app,
                self.app,
                user
            ).pack(
                fill="both",
                expand=True
            )

        else:
            from Frontend.pages.faculty_dashboard import FacultyDashboard

            FacultyDashboard(
                self.app,
                self.app,
                user
            ).pack(
                fill="both",
                expand=True
            )

    # ---------------------------------------------------------
    # REGISTER
    # ---------------------------------------------------------

    def register(self):
        name = self.email_entry.get().strip()

        # Registration dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Create Account")
        dialog.geometry("450x560")
        dialog.resizable(False, False)

        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Create Account",
            font=("Arial", 26, "bold"),
            text_color="#202124"
        ).pack(
            pady=(30, 5)
        )

        ctk.CTkLabel(
            dialog,
            text="Join CollabCampus",
            font=("Arial", 13),
            text_color="#6B7280"
        ).pack(
            pady=(0, 20)
        )

        ctk.CTkLabel(
            dialog,
            text="Full Name",
            font=("Arial", 13, "bold")
        ).pack(
            anchor="w",
            padx=40,
            pady=(5, 5)
        )

        name_entry = ctk.CTkEntry(
            dialog,
            width=360,
            height=40,
            placeholder_text="Enter your name"
        )
        name_entry.pack(padx=40)

        ctk.CTkLabel(
            dialog,
            text="Email",
            font=("Arial", 13, "bold")
        ).pack(
            anchor="w",
            padx=40,
            pady=(15, 5)
        )

        email_entry = ctk.CTkEntry(
            dialog,
            width=360,
            height=40,
            placeholder_text="Enter your email"
        )
        email_entry.pack(padx=40)

        ctk.CTkLabel(
            dialog,
            text="Password",
            font=("Arial", 13, "bold")
        ).pack(
            anchor="w",
            padx=40,
            pady=(15, 5)
        )

        password_entry = ctk.CTkEntry(
            dialog,
            width=360,
            height=40,
            placeholder_text="Create a password",
            show="*"
        )
        password_entry.pack(padx=40)

        ctk.CTkLabel(
            dialog,
            text="Role",
            font=("Arial", 13, "bold")
        ).pack(
            anchor="w",
            padx=40,
            pady=(15, 5)
        )

        role_menu = ctk.CTkOptionMenu(
            dialog,
            width=360,
            height=40,
            values=["student", "faculty"]
        )
        role_menu.pack(padx=40)

        result_label = ctk.CTkLabel(
            dialog,
            text="",
            font=("Arial", 11)
        )
        result_label.pack(pady=12)

        def create_account():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get()
            role = role_menu.get()

            if not name or not email or not password:
                result_label.configure(
                    text="All fields are required.",
                    text_color="#B91C1C"
                )
                return

            try:
                success, message = register_user(
                    name,
                    email,
                    password,
                    role
                )

            except Exception as error:
                result_label.configure(
                    text=f"Database error: {error}",
                    text_color="#B91C1C"
                )
                return

            result_label.configure(
                text=message,
                text_color="#047857" if success else "#B91C1C"
            )

            if success:
                name_entry.delete(0, "end")
                email_entry.delete(0, "end")
                password_entry.delete(0, "end")

        ctk.CTkButton(
            dialog,
            text="Create Account",
            width=360,
            height=42,
            corner_radius=9,
            command=create_account
        ).pack(
            padx=40
        )

        ctk.CTkButton(
            dialog,
            text="Cancel",
            width=360,
            height=38,
            fg_color="white",
            text_color="#374151",
            border_width=1,
            border_color="#D1D5DB",
            hover_color="#F3F4F6",
            command=dialog.destroy
        ).pack(
            padx=40,
            pady=8
        )