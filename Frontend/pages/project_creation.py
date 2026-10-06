import customtkinter as ctk

from Backend.projects import create_project


class ProjectCreationPage(ctk.CTkFrame):

    def __init__(self, parent, app, user):
        super().__init__(parent)

        self.app = app
        self.user = user

        self.configure(fg_color="#F5F7FB")

        self.create_navbar()
        self.create_form()

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
            text="Find Teams",
            width=105,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_teammates
        ).pack(
            side="right",
            padx=5
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
            padx=5
        )

        ctk.CTkButton(
            navbar,
            text="My Profile",
            width=100,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_profile
        ).pack(
            side="right",
            padx=5
        )

    # ---------------- FORM ----------------

    def create_form(self):

        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=80,
            pady=30
        )

        ctk.CTkLabel(
            main,
            text="Post a New Project",
            font=("Arial", 32, "bold"),
            text_color="#202124"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            main,
            text="Share your idea and find students who can help build it.",
            font=("Arial", 15),
            text_color="#6B7280"
        ).pack(pady=(0, 25))

        # Main form card

        form = ctk.CTkFrame(
            main,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E5E7EB"
        )

        form.pack(
            fill="x",
            padx=50,
            pady=10
        )

        # Project title

        ctk.CTkLabel(
            form,
            text="Project Title",
            font=("Arial", 15, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            form,
            text="Give your project a clear and meaningful name.",
            font=("Arial", 11),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=30
        )

        self.title_entry = ctk.CTkEntry(
            form,
            height=42,
            placeholder_text="e.g. AI Student Career Advisor",
            font=("Arial", 14)
        )

        self.title_entry.pack(
            fill="x",
            padx=30,
            pady=(8, 20)
        )

        # Description

        ctk.CTkLabel(
            form,
            text="Project Description",
            font=("Arial", 15, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=30,
            pady=(5, 5)
        )

        ctk.CTkLabel(
            form,
            text="Explain the problem, idea and what your team wants to build.",
            font=("Arial", 11),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=30
        )

        self.description = ctk.CTkTextbox(
            form,
            height=170,
            font=("Arial", 13)
        )

        self.description.pack(
            fill="x",
            padx=30,
            pady=(8, 20)
        )

        # Skills

        ctk.CTkLabel(
            form,
            text="Skills Needed",
            font=("Arial", 15, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=30,
            pady=(5, 5)
        )

        ctk.CTkLabel(
            form,
            text="Mention the skills you are looking for in teammates.",
            font=("Arial", 11),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=30
        )

        self.skills_entry = ctk.CTkEntry(
            form,
            height=42,
            placeholder_text="Python, Java, UI/UX, SQL, Documentation..."
        )

        self.skills_entry.pack(
            fill="x",
            padx=30,
            pady=(8, 20)
        )

        # Suggested skills

        ctk.CTkLabel(
            form,
            text="Quick Select",
            font=("Arial", 12, "bold"),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 5)
        )

        skills_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        skills_frame.pack(
            fill="x",
            padx=25
        )

        for skill in [
            "Python",
            "Java",
            "SQL",
            "React",
            "UI/UX",
            "Testing",
            "Documentation",
            "Presentation"
        ]:

            ctk.CTkButton(
                skills_frame,
                text=skill,
                width=90,
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
                padx=4,
                pady=4
            )

        # Project status information

        info = ctk.CTkFrame(
            form,
            fg_color="#EFF6FF",
            corner_radius=10
        )

        info.pack(
            fill="x",
            padx=30,
            pady=25
        )

        ctk.CTkLabel(
            info,
            text="💡  Tip",
            font=("Arial", 14, "bold"),
            text_color="#1D4ED8"
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 3)
        )

        ctk.CTkLabel(
            info,
            text="Projects with a clear description and required skills are easier for students to discover.",
            font=("Arial", 11),
            text_color="#374151",
            wraplength=700,
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        # Message

        self.message = ctk.CTkLabel(
            form,
            text="",
            font=("Arial", 12)
        )

        self.message.pack(
            pady=(0, 8)
        )

        # Buttons

        button_frame = ctk.CTkFrame(
            form,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=(0, 25)
        )

        ctk.CTkButton(
            button_frame,
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
            button_frame,
            text="🚀  Publish Project",
            width=160,
            height=40,
            command=self.create
        ).pack(
            side="left",
            padx=5
        )

    # ---------------- ADD SKILL ----------------

    def add_skill(self, skill):

        current = self.skills_entry.get().strip()

        if not current:
            self.skills_entry.insert(
                0,
                skill
            )
            return

        existing = [
            item.strip().lower()
            for item in current.split(",")
        ]

        if skill.lower() not in existing:
            self.skills_entry.delete(
                0,
                "end"
            )

            self.skills_entry.insert(
                0,
                current + ", " + skill
            )

    # ---------------- CREATE PROJECT ----------------

    def create(self):

        title = self.title_entry.get().strip()

        description = self.description.get(
            "1.0",
            "end"
        ).strip()

        skills = self.skills_entry.get().strip()

        if not title:
            self.message.configure(
                text="Please enter a project title.",
                text_color="#B91C1C"
            )
            return

        if not description:
            self.message.configure(
                text="Please describe your project.",
                text_color="#B91C1C"
            )
            return

        try:

            project_id = create_project(
                title,
                description,
                self.user["id"]
            )

            self.message.configure(
                text=f"Project published successfully! Project ID: {project_id}",
                text_color="#047857"
            )

            self.title_entry.delete(
                0,
                "end"
            )

            self.description.delete(
                "1.0",
                "end"
            )

            self.skills_entry.delete(
                0,
                "end"
            )

        except Exception as error:

            self.message.configure(
                text=f"Unable to create project: {error}",
                text_color="#B91C1C"
            )

    # ---------------- NAVIGATION ----------------

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