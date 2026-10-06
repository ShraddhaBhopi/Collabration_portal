import customtkinter as ctk

from Backend.users import get_user, update_profile


class ProfileSetupPage(ctk.CTkFrame):

    def __init__(self, parent, app, user):
        super().__init__(parent)

        self.app = app
        self.user = user

        self.configure(fg_color="#F5F7FB")

        self.load_user()
        self.create_navbar()
        self.create_profile()

    # ---------------- LOAD USER ----------------

    def load_user(self):

        try:
            self.current_user = get_user(
                self.user["id"]
            )
        except Exception:
            self.current_user = self.user

    # ---------------- NAVBAR ----------------

    def create_navbar(self):

        navbar = ctk.CTkFrame(
            self,
            height=65,
            corner_radius=0,
            fg_color="#1976D2"
        )

        navbar.pack(fill="x")
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
            text="Dashboard",
            width=100,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.back
        ).pack(
            side="right",
            padx=8
        )

        ctk.CTkButton(
            navbar,
            text="Projects",
            width=90,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_projects
        ).pack(
            side="right",
            padx=8
        )

        ctk.CTkButton(
            navbar,
            text="Find Teams",
            width=105,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_teammates
        ).pack(
            side="right",
            padx=8
        )

    # ---------------- PROFILE ----------------

    def create_profile(self):

        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=70,
            pady=30
        )

        ctk.CTkLabel(
            main,
            text="My Profile",
            font=("Arial", 32, "bold"),
            text_color="#202124"
        ).pack(pady=(5, 3))

        ctk.CTkLabel(
            main,
            text="Build your profile so teammates can discover you.",
            font=("Arial", 15),
            text_color="#6B7280"
        ).pack(
            pady=(0, 25)
        )

        # Main profile card

        card = ctk.CTkFrame(
            main,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E5E7EB"
        )

        card.pack(
            fill="x",
            padx=50
        )

        # ---------------- PROFILE HEADER ----------------

        header = ctk.CTkFrame(
            card,
            fg_color="#EFF6FF",
            corner_radius=12
        )

        header.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # Avatar

        avatar = ctk.CTkLabel(
            header,
            text=self.current_user.get(
                "name",
                "U"
            )[0].upper(),
            width=80,
            height=80,
            corner_radius=40,
            fg_color="#1976D2",
            text_color="white",
            font=("Arial", 32, "bold")
        )

        avatar.pack(
            side="left",
            padx=20,
            pady=20
        )

        identity = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        identity.pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            identity,
            text=self.current_user.get(
                "name",
                "Student"
            ),
            font=("Arial", 24, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            identity,
            text=self.current_user.get(
                "email",
                ""
            ),
            font=("Arial", 12),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        ctk.CTkLabel(
            identity,
            text="Student",
            font=("Arial", 12, "bold"),
            text_color="#1976D2"
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        # ---------------- FORM ----------------

        ctk.CTkLabel(
            card,
            text="Profile Information",
            font=("Arial", 19, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=30,
            pady=(5, 3)
        )

        ctk.CTkLabel(
            card,
            text="Add information about yourself and your technical skills.",
            font=("Arial", 12),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=30
        )

        # Department

        ctk.CTkLabel(
            card,
            text="Department",
            font=("Arial", 14, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 5)
        )

        self.department = ctk.CTkEntry(
            card,
            height=42,
            placeholder_text="e.g. Computer Engineering"
        )

        self.department.pack(
            fill="x",
            padx=30
        )

        if self.current_user.get("department"):
            self.department.insert(
                0,
                self.current_user["department"]
            )

        # Skills

        ctk.CTkLabel(
            card,
            text="Technical Skills",
            font=("Arial", 14, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=30,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card,
            text="Separate skills using commas.",
            font=("Arial", 11),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=30
        )

        self.skills = ctk.CTkEntry(
            card,
            height=42,
            placeholder_text="Python, Java, SQL, Git, UI/UX..."
        )

        self.skills.pack(
            fill="x",
            padx=30,
            pady=(7, 0)
        )

        if self.current_user.get("skills"):
            self.skills.insert(
                0,
                self.current_user["skills"]
            )

        # Skill shortcuts

        skill_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        skill_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        for skill in [
            "Python",
            "Java",
            "SQL",
            "Git",
            "UI/UX",
            "Machine Learning"
        ]:

            ctk.CTkButton(
                skill_frame,
                text=skill,
                width=95,
                height=30,
                corner_radius=8,
                fg_color="#F8FAFC",
                hover_color="#E3F2FD",
                text_color="#374151",
                border_width=1,
                border_color="#D1D5DB",
                command=lambda s=skill: self.add_skill(s)
            ).pack(
                side="left",
                padx=4
            )

        # Bio

        ctk.CTkLabel(
            card,
            text="About Me",
            font=("Arial", 14, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=30,
            pady=(15, 5)
        )

        self.bio = ctk.CTkTextbox(
            card,
            height=140,
            font=("Arial", 13)
        )

        self.bio.pack(
            fill="x",
            padx=30
        )

        if self.current_user.get("bio"):
            self.bio.insert(
                "1.0",
                self.current_user["bio"]
            )

        # ---------------- MESSAGE ----------------

        self.message = ctk.CTkLabel(
            card,
            text="",
            font=("Arial", 12)
        )

        self.message.pack(
            pady=(15, 5)
        )

        # ---------------- BUTTONS ----------------

        buttons = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        buttons.pack(
            pady=(5, 25)
        )

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=120,
            height=40,
            fg_color="white",
            text_color="#374151",
            border_width=1,
            border_color="#D1D5DB",
            hover_color="#F3F4F6",
            command=self.back
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Save Profile",
            width=140,
            height=40,
            command=self.save
        ).pack(
            side="left",
            padx=5
        )

    # ---------------- SKILL ----------------

    def add_skill(self, skill):

        current = self.skills.get().strip()

        if not current:

            self.skills.insert(
                0,
                skill
            )

            return

        existing = [
            item.strip().lower()
            for item in current.split(",")
        ]

        if skill.lower() not in existing:

            self.skills.delete(
                0,
                "end"
            )

            self.skills.insert(
                0,
                current + ", " + skill
            )

    # ---------------- SAVE ----------------

    def save(self):

        department = self.department.get().strip()
        skills = self.skills.get().strip()
        bio = self.bio.get(
            "1.0",
            "end"
        ).strip()

        try:

            update_profile(
                self.user["id"],
                department,
                skills,
                bio
            )

            self.message.configure(
                text="Profile updated successfully.",
                text_color="#047857"
            )

        except Exception as error:

            self.message.configure(
                text=f"Unable to update profile: {error}",
                text_color="#B91C1C"
            )

    # ---------------- NAVIGATION ----------------

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

    def open_projects(self):

        from Frontend.pages.project_marketplace import ProjectMarketplace

        self.destroy()

        ProjectMarketplace(
            self.app,
            self.app,
            self.user
        ).pack(
            fill="both",
            expand=True
        )

    def open_teammates(self):

        from Frontend.pages.find_teammates import FindTeammatesPage

        self.destroy()

        FindTeammatesPage(
            self.app,
            self.app,
            self.user
        ).pack(
            fill="both",
            expand=True
        )