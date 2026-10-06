import customtkinter as ctk

from Backend.projects import get_project_members
from Backend.tasks import get_tasks
from Frontend.pages.tasks_page import TasksPage


class ProjectWorkspace(ctk.CTkFrame):

    def __init__(self, parent, app, user, project):
        super().__init__(parent)

        self.app = app
        self.user = user
        self.project = project

        self.configure(fg_color="#F5F7FB")

        self.create_navbar()
        self.create_workspace()

        self.load_members()
        self.load_tasks()

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
            text="Projects",
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
            text="My Profile",
            width=105,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_profile
        ).pack(
            side="right",
            padx=8
        )

    # ---------------- WORKSPACE ----------------

    def create_workspace(self):

        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        main.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=25
        )

        # Header

        header = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            pady=(0, 20)
        )

        ctk.CTkLabel(
            header,
            text=self.project["title"],
            font=("Arial", 30, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            header,
            text="Project Workspace",
            font=("Arial", 14),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # Status

        status_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        status_frame.pack(
            anchor="w",
            pady=10
        )

        ctk.CTkLabel(
            status_frame,
            text=f"●  {self.project['status']}",
            fg_color="#D1FAE5",
            text_color="#047857",
            corner_radius=8,
            font=("Arial", 12, "bold")
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ctk.CTkLabel(
            status_frame,
            text=f"Led by {self.project['owner_name']}",
            font=("Arial", 12),
            text_color="#6B7280"
        ).pack(
            side="left"
        )

        # Description

        description_card = ctk.CTkFrame(
            main,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        description_card.pack(
            fill="x",
            pady=(0, 20)
        )

        ctk.CTkLabel(
            description_card,
            text="About this project",
            font=("Arial", 18, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            description_card,
            text=self.project["description"],
            font=("Arial", 13),
            text_color="#4B5563",
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

        # Two-column area

        columns = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        columns.pack(
            fill="both",
            expand=True
        )

        # Members

        members_card = ctk.CTkFrame(
            columns,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        members_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 8)
        )

        ctk.CTkLabel(
            members_card,
            text="Team Members",
            font=("Arial", 19, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        ctk.CTkLabel(
            members_card,
            text="People working on this project",
            font=("Arial", 12),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=20
        )

        self.members_frame = ctk.CTkScrollableFrame(
            members_card,
            height=320,
            fg_color="transparent"
        )

        self.members_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Tasks

        tasks_card = ctk.CTkFrame(
            columns,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        tasks_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(8, 0)
        )

        task_header = ctk.CTkFrame(
            tasks_card,
            fg_color="transparent"
        )

        task_header.pack(
            fill="x",
            padx=20,
            pady=(18, 3)
        )

        ctk.CTkLabel(
            task_header,
            text="Tasks",
            font=("Arial", 19, "bold"),
            text_color="#202124"
        ).pack(side="left")

        ctk.CTkButton(
            task_header,
            text="+ Add Task",
            width=100,
            height=30,
            command=self.open_tasks
        ).pack(side="right")

        ctk.CTkLabel(
            tasks_card,
            text="Track project progress",
            font=("Arial", 12),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=20
        )

        self.tasks_frame = ctk.CTkScrollableFrame(
            tasks_card,
            height=320,
            fg_color="transparent"
        )

        self.tasks_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # ---------------- MEMBERS ----------------

    def load_members(self):

        for widget in self.members_frame.winfo_children():
            widget.destroy()

        try:
            members = get_project_members(
                self.project["id"]
            )
        except Exception as error:

            ctk.CTkLabel(
                self.members_frame,
                text=f"Unable to load members.\n{error}",
                text_color="#6B7280"
            ).pack(pady=30)

            return

        if not members:

            ctk.CTkLabel(
                self.members_frame,
                text="No team members yet.",
                text_color="#6B7280"
            ).pack(pady=30)

            return

        for member in members:

            card = ctk.CTkFrame(
                self.members_frame,
                fg_color="#F8FAFC",
                corner_radius=10
            )

            card.pack(
                fill="x",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=f"👤  {member['name']}",
                font=("Arial", 15, "bold"),
                text_color="#202124"
            ).pack(
                anchor="w",
                padx=14,
                pady=(10, 2)
            )

            ctk.CTkLabel(
                card,
                text=member["email"],
                font=("Arial", 11),
                text_color="#6B7280"
            ).pack(
                anchor="w",
                padx=14
            )

            skills = member["skills"] or "No skills listed"

            ctk.CTkLabel(
                card,
                text=f"Skills: {skills}",
                font=("Arial", 11),
                text_color="#4B5563",
                wraplength=350,
                justify="left"
            ).pack(
                anchor="w",
                padx=14,
                pady=(3, 10)
            )

    # ---------------- TASKS ----------------

    def load_tasks(self):

        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        try:
            tasks = get_tasks(
                self.project["id"]
            )
        except Exception as error:

            ctk.CTkLabel(
                self.tasks_frame,
                text=f"Unable to load tasks.\n{error}",
                text_color="#6B7280"
            ).pack(pady=30)

            return

        if not tasks:

            ctk.CTkLabel(
                self.tasks_frame,
                text="No tasks created yet.",
                text_color="#6B7280"
            ).pack(pady=30)

            return

        for task in tasks[:8]:

            card = ctk.CTkFrame(
                self.tasks_frame,
                fg_color="#F8FAFC",
                corner_radius=10
            )

            card.pack(
                fill="x",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=task["title"],
                font=("Arial", 14, "bold"),
                text_color="#202124"
            ).pack(
                anchor="w",
                padx=14,
                pady=(10, 3)
            )

            description = task["description"] or ""

            if len(description) > 90:
                description = description[:90] + "..."

            if description:
                ctk.CTkLabel(
                    card,
                    text=description,
                    font=("Arial", 11),
                    text_color="#6B7280",
                    wraplength=350,
                    justify="left"
                ).pack(
                    anchor="w",
                    padx=14
                )

            status = task["status"]

            status_color = {
                "Pending": "#FEF3C7",
                "In Progress": "#DBEAFE",
                "Completed": "#D1FAE5"
            }.get(status, "#E5E7EB")

            text_color = {
                "Pending": "#B45309",
                "In Progress": "#1D4ED8",
                "Completed": "#047857"
            }.get(status, "#4B5563")

            ctk.CTkLabel(
                card,
                text=f"  {status}  ",
                fg_color=status_color,
                text_color=text_color,
                corner_radius=7,
                font=("Arial", 10, "bold")
            ).pack(
                anchor="w",
                padx=14,
                pady=(6, 10)
            )

    # ---------------- TASK MANAGEMENT ----------------

    def open_tasks(self):

        self.destroy()

        TasksPage(
            self.app,
            self.app,
            self.user,
            self.project
        ).pack(
            fill="both",
            expand=True
        )

    # ---------------- NAVIGATION ----------------

    def back(self):

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