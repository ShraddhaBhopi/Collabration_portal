import customtkinter as ctk

from Backend.users import find_teammates


class FindTeammatesPage(ctk.CTkFrame):

    def __init__(self, parent, app, user):
        super().__init__(parent)

        self.app = app
        self.user = user

        self.configure(fg_color="#F5F7FB")

        self.create_navbar()
        self.create_main_content()

        self.load_users()

    # ---------------- NAVBAR ----------------

    def create_navbar(self):

        navbar = ctk.CTkFrame(
            self,
            height=65,
            corner_radius=0,
            fg_color="#1976D2"
        )

        navbar.pack(
            fill="x"
        )

        navbar.pack_propagate(False)

        ctk.CTkLabel(
            navbar,
            text="👥  CollabCampus",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(
            side="left",
            padx=30
        )

        ctk.CTkButton(
            navbar,
            text="Find Teams",
            width=110,
            height=35,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            text_color="white",
            command=self.refresh
        ).pack(
            side="right",
            padx=8
        )

        ctk.CTkButton(
            navbar,
            text="My Profile",
            width=110,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_profile
        ).pack(
            side="right",
            padx=8
        )

        ctk.CTkButton(
            navbar,
            text="+  Post Project",
            width=130,
            height=35,
            fg_color="white",
            hover_color="#E3F2FD",
            text_color="#1976D2",
            command=self.create_project
        ).pack(
            side="right",
            padx=(8, 25)
        )

    # ---------------- MAIN CONTENT ----------------

    def create_main_content(self):

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=25
        )

        ctk.CTkLabel(
            self.content,
            text="Find Your Ideal Project Team",
            font=("Arial", 32, "bold"),
            text_color="#202124"
        ).pack(
            pady=(10, 5)
        )

        ctk.CTkLabel(
            self.content,
            text="Discover students with the skills you need for your next project",
            font=("Arial", 15),
            text_color="#6B7280"
        ).pack(
            pady=(0, 25)
        )

        # ---------------- SEARCH ----------------

        search_frame = ctk.CTkFrame(
            self.content,
            fg_color="white",
            corner_radius=12
        )

        search_frame.pack(
            fill="x",
            padx=30,
            pady=5
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=45,
            placeholder_text="🔍  Search skills (e.g. Python, Java, SQL, UI/UX...)",
            font=("Arial", 15),
            border_width=0
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 5),
            pady=8
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=120,
            height=40,
            corner_radius=8,
            command=self.search_users
        ).pack(
            side="right",
            padx=8
        )

        # ---------------- FILTERS ----------------

        ctk.CTkLabel(
            self.content,
            text="SKILLS & TECHNOLOGIES",
            font=("Arial", 12, "bold"),
            text_color="#6B7280"
        ).pack(
            pady=(25, 8)
        )

        filters = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        filters.pack()

        skills = [
            "Python",
            "Java",
            "C++",
            "SQL / MySQL",
            "React",
            "UI/UX",
            "Flutter",
            "Project Management"
        ]

        for skill in skills:

            ctk.CTkButton(
                filters,
                text=skill,
                width=105,
                height=32,
                corner_radius=8,
                fg_color="white",
                hover_color="#E3F2FD",
                text_color="#374151",
                border_width=1,
                border_color="#D1D5DB",
                command=lambda s=skill: self.select_skill(s)
            ).pack(
                side="left",
                padx=4,
                pady=4
            )

        # ---------------- RESULTS ----------------

        self.results = ctk.CTkScrollableFrame(
            self.content,
            fg_color="transparent"
        )

        self.results.pack(
            fill="both",
            expand=True,
            pady=(25, 5)
        )

    # ---------------- LOAD USERS ----------------

    def load_users(self, skill=""):

        for widget in self.results.winfo_children():
            widget.destroy()

        try:
            users = find_teammates(
                self.user["id"],
                skill
            )
        except Exception as error:

            self.show_message(
                f"Database unavailable.\n\n{error}"
            )

            return

        if not users:

            ctk.CTkLabel(
                self.results,
                text="No students found.",
                font=("Arial", 18),
                text_color="#6B7280"
            ).pack(
                pady=50
            )

            return

        # 3-column layout

        row = None

        for index, user in enumerate(users):

            if index % 3 == 0:

                row = ctk.CTkFrame(
                    self.results,
                    fg_color="transparent"
                )

                row.pack(
                    fill="x",
                    pady=8
                )

            self.create_user_card(
                row,
                user
            )

    # ---------------- USER CARD ----------------

    def create_user_card(self, parent, user):

        card = ctk.CTkFrame(
            parent,
            width=300,
            height=230,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )

        card.pack_propagate(False)

        # Name

        ctk.CTkLabel(
            card,
            text=user["name"],
            font=("Arial", 19, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 3)
        )

        # Department

        department = (
            user["department"]
            if user["department"]
            else "Computer Engineering"
        )

        ctk.CTkLabel(
            card,
            text=department,
            font=("Arial", 12),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=18
        )

        # Skills

        skills = user["skills"] or "Skills not added"

        ctk.CTkLabel(
            card,
            text=skills,
            font=("Arial", 13),
            text_color="#374151",
            wraplength=250,
            justify="left"
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 5)
        )

        # Bio

        if user["bio"]:

            ctk.CTkLabel(
                card,
                text=user["bio"],
                font=("Arial", 11),
                text_color="#6B7280",
                wraplength=250,
                justify="left"
            ).pack(
                anchor="w",
                padx=18
            )

        # Button

        ctk.CTkButton(
            card,
            text="View Profile",
            height=32,
            corner_radius=7,
            command=lambda u=user: self.view_profile(u)
        ).pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=15
        )

    # ---------------- SEARCH ----------------

    def search_users(self):

        skill = self.search_entry.get().strip()

        self.load_users(skill)

    # ---------------- FILTER ----------------

    def select_skill(self, skill):

        self.search_entry.delete(
            0,
            "end"
        )

        self.search_entry.insert(
            0,
            skill
        )

        self.load_users(skill)

    # ---------------- PROFILE ----------------

    def view_profile(self, user):

        self.show_message(
            f"Name: {user['name']}\n\n"
            f"Department: {user['department'] or 'Not specified'}\n\n"
            f"Skills: {user['skills'] or 'Not specified'}\n\n"
            f"Email: {user['email']}"
        )

    # ---------------- NAVIGATION ----------------

    def open_profile(self):

        from Frontend.pages.profile_setup import ProfileSetupPage

        self.destroy()

        ProfileSetupPage(
            self.app,
            self.app,
            self.user
        ).pack(
            fill="both",
            expand=True
        )

    def create_project(self):

        from Frontend.pages.project_creation import ProjectCreationPage

        self.destroy()

        ProjectCreationPage(
            self.app,
            self.app,
            self.user
        ).pack(
            fill="both",
            expand=True
        )

    def refresh(self):

        self.load_users()

    def back(self):

        from Frontend.pages.student_dashboard import StudentDashboard

        self.destroy()

        StudentDashboard(
            self.app,
            self.app,
            self.user
        ).pack(
            fill="both",
            expand=True
        )

    def show_message(self, message):

        dialog = ctk.CTkToplevel(self)

        dialog.title("CollabCampus")
        dialog.geometry("450x300")

        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=380,
            justify="left",
            font=("Arial", 14)
        ).pack(
            padx=30,
            pady=40
        )

        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            command=dialog.destroy
        ).pack()