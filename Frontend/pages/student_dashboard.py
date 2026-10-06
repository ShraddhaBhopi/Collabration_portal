import customtkinter as ctk

from Backend.projects import get_projects
from Backend.notifications import get_notifications


class StudentDashboard(ctk.CTkFrame):

    def __init__(self, parent, app, user):
        super().__init__(parent)

        self.app = app
        self.user = user

        self.configure(fg_color="#F5F7FB")

        self.create_navbar()
        self.create_dashboard()

        self.load_statistics()

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

        ctk.CTkButton(
            navbar,
            text="Logout",
            width=80,
            height=35,
            fg_color="white",
            hover_color="#E3F2FD",
            text_color="#1976D2",
            command=self.logout
        ).pack(
            side="right",
            padx=(5, 25)
        )

    # ---------------- DASHBOARD ----------------

    def create_dashboard(self):

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

        # Welcome section

        welcome_frame = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        welcome_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        ctk.CTkLabel(
            welcome_frame,
            text=f"Welcome back, {self.user['name']} 👋",
            font=("Arial", 30, "bold"),
            text_color="#202124"
        ).pack(anchor="w")

        ctk.CTkLabel(
            welcome_frame,
            text="Find teammates, discover projects and build something great together.",
            font=("Arial", 15),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # ---------------- QUICK ACTIONS ----------------

        ctk.CTkLabel(
            main,
            text="Quick Actions",
            font=("Arial", 20, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        actions = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        actions.pack(
            fill="x",
            pady=(0, 25)
        )

        self.create_action_card(
            actions,
            "🔎",
            "Find Teammates",
            "Discover students with matching skills",
            self.open_teammates
        )

        self.create_action_card(
            actions,
            "📁",
            "Explore Projects",
            "Find projects looking for team members",
            self.open_projects
        )

        self.create_action_card(
            actions,
            "➕",
            "Create Project",
            "Post your own project and build a team",
            self.open_create_project
        )

        self.create_action_card(
            actions,
            "🤖",
            "AI Assistant",
            "Get help with projects and team formation",
            self.open_ai_assistant
        )

        # ---------------- STATISTICS ----------------

        ctk.CTkLabel(
            main,
            text="Your Activity",
            font=("Arial", 20, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        stats = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        stats.pack(
            fill="x",
            pady=(0, 25)
        )

        self.projects_stat = self.create_stat_card(
            stats,
            "Projects",
            "0"
        )

        self.open_stat = self.create_stat_card(
            stats,
            "Open Projects",
            "0"
        )

        self.notifications_stat = self.create_stat_card(
            stats,
            "Notifications",
            "0"
        )

        # ---------------- RECENT PROJECTS ----------------

        ctk.CTkLabel(
            main,
            text="Recent Projects",
            font=("Arial", 20, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        self.projects_frame = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        self.projects_frame.pack(
            fill="x",
            pady=(0, 25)
        )

        # ---------------- BOTTOM ----------------

        bottom = ctk.CTkFrame(
            main,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        bottom.pack(
            fill="x",
            pady=(5, 20)
        )

        ctk.CTkLabel(
            bottom,
            text="Need help?",
            font=("Arial", 18, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 3)
        )

        ctk.CTkLabel(
            bottom,
            text="Ask the CollabCampus Assistant about teams, projects, skills or tasks.",
            font=("Arial", 13),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=20
        )

        ctk.CTkButton(
            bottom,
            text="Open AI Assistant",
            width=150,
            command=self.open_ai_assistant
        ).pack(
            anchor="w",
            padx=20,
            pady=15
        )

    # ---------------- ACTION CARD ----------------

    def create_action_card(
        self,
        parent,
        icon,
        title,
        description,
        command
    ):

        card = ctk.CTkFrame(
            parent,
            width=240,
            height=145,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 25)
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 0)
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 16, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=18,
            pady=(3, 2)
        )

        ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 11),
            text_color="#6B7280",
            wraplength=200,
            justify="left"
        ).pack(
            anchor="w",
            padx=18
        )

        ctk.CTkButton(
            card,
            text="Open →",
            width=80,
            height=28,
            command=command
        ).pack(
            anchor="e",
            padx=15,
            pady=5
        )

    # ---------------- STAT CARD ----------------

    def create_stat_card(
        self,
        parent,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            height=100,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 28, "bold"),
            text_color="#1976D2"
        )

        value_label.pack(
            anchor="w",
            padx=18,
            pady=(15, 0)
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 12),
            text_color="#6B7280"
        ).pack(
            anchor="w",
            padx=18
        )

        return value_label

    # ---------------- LOAD STATISTICS ----------------

    def load_statistics(self):

        try:
            projects = get_projects()
        except Exception:
            projects = []

        try:
            notifications = get_notifications(
                self.user["id"]
            )
        except Exception:
            notifications = []

        self.projects_stat.configure(
            text=str(len(projects))
        )

        open_projects = [
            project
            for project in projects
            if project["status"] == "Open"
        ]

        self.open_stat.configure(
            text=str(len(open_projects))
        )

        unread = [
            notification
            for notification in notifications
            if not notification["is_read"]
        ]

        self.notifications_stat.configure(
            text=str(len(unread))
        )

        self.load_recent_projects(projects)

    # ---------------- RECENT PROJECTS ----------------

    def load_recent_projects(self, projects):

        for widget in self.projects_frame.winfo_children():
            widget.destroy()

        if not projects:

            empty = ctk.CTkFrame(
                self.projects_frame,
                fg_color="white",
                corner_radius=12
            )

            empty.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                empty,
                text="No projects available yet.",
                font=("Arial", 14),
                text_color="#6B7280"
            ).pack(pady=30)

            return

        for project in projects[:3]:

            self.create_project_preview(
                project
            )

    # ---------------- PROJECT PREVIEW ----------------

    def create_project_preview(self, project):

        card = ctk.CTkFrame(
            self.projects_frame,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )

        card.pack(
            fill="x",
            pady=6
        )

        left = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=18,
            pady=14
        )

        ctk.CTkLabel(
            left,
            text=project["title"],
            font=("Arial", 17, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w"
        )

        description = project["description"]

        if len(description) > 100:
            description = description[:100] + "..."

        ctk.CTkLabel(
            left,
            text=description,
            font=("Arial", 12),
            text_color="#6B7280",
            wraplength=600,
            justify="left"
        ).pack(
            anchor="w",
            pady=(4, 3)
        )

        ctk.CTkLabel(
            left,
            text=f"Led by {project['owner_name']}  •  {project['status']}",
            font=("Arial", 11),
            text_color="#6B7280"
        ).pack(
            anchor="w"
        )

        ctk.CTkButton(
            card,
            text="View",
            width=90,
            height=35,
            command=lambda p=project: self.open_workspace(p)
        ).pack(
            side="right",
            padx=18
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

    def open_create_project(self):

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

    def open_ai_assistant(self):

        from Frontend.pages.ai_assistant import AIAssistantPage

        self.destroy()

        AIAssistantPage(
            self.app,
            self.app,
            self.user
        ).pack(
            fill="both",
            expand=True
        )

    def open_workspace(self, project):

        from Frontend.pages.project_workspace import ProjectWorkspace

        self.destroy()

        ProjectWorkspace(
            self.app,
            self.app,
            self.user,
            project
        ).pack(
            fill="both",
            expand=True
        )

    # ---------------- LOGOUT ----------------

    def logout(self):

        self.destroy()

        from Frontend.pages.auth_page import AuthPage

        AuthPage(
            self.app,
            self.app
        ).pack(
            fill="both",
            expand=True
        )