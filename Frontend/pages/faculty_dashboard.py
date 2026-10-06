import customtkinter as ctk
from Backend.projects import get_projects


class FacultyDashboard(ctk.CTkFrame):
    def __init__(self, parent, app, user):
        super().__init__(parent)

        self.app = app
        self.user = user

        self.configure(fg_color="#F5F7FB")

        self.create_navbar()
        self.create_dashboard()

    # ---------------------------------------------------------
    # NAVBAR
    # ---------------------------------------------------------

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
        ).pack(side="left", padx=30)

        ctk.CTkButton(
            navbar,
            text="Dashboard",
            width=100,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.refresh
        ).pack(side="right", padx=8)

        ctk.CTkButton(
            navbar,
            text="Projects",
            width=90,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_projects
        ).pack(side="right", padx=8)

        ctk.CTkButton(
            navbar,
            text="Notifications",
            width=115,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_notifications
        ).pack(side="right", padx=8)

    # ---------------------------------------------------------
    # DASHBOARD
    # ---------------------------------------------------------

    def create_dashboard(self):
        main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        main.pack(
            fill="both",
            expand=True,
            padx=60,
            pady=30
        )

        # Welcome section
        welcome = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )
        welcome.pack(fill="x", pady=(5, 20))

        ctk.CTkLabel(
            welcome,
            text=f"Welcome, {self.user.get('name', 'Faculty')} 👋",
            font=("Arial", 30, "bold"),
            text_color="#202124"
        ).pack(anchor="w")

        ctk.CTkLabel(
            welcome,
            text="Manage projects, monitor student collaboration and guide teams.",
            font=("Arial", 14),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(4, 0))

        # -----------------------------------------------------
        # Quick actions
        # -----------------------------------------------------

        ctk.CTkLabel(
            main,
            text="Quick Actions",
            font=("Arial", 20, "bold"),
            text_color="#202124"
        ).pack(anchor="w", pady=(5, 12))

        actions = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )
        actions.pack(fill="x", pady=(0, 25))

        self.create_action_card(
            actions,
            "📁",
            "Explore Projects",
            "View student projects and collaboration activity.",
            self.open_projects
        )

        self.create_action_card(
            actions,
            "🔔",
            "Notifications",
            "Check updates and project activity.",
            self.open_notifications
        )

        # -----------------------------------------------------
        # Stats
        # -----------------------------------------------------

        ctk.CTkLabel(
            main,
            text="Overview",
            font=("Arial", 20, "bold"),
            text_color="#202124"
        ).pack(anchor="w", pady=(5, 12))

        stats = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )
        stats.pack(fill="x", pady=(0, 25))

        projects = self.load_projects()

        total_projects = len(projects)

        open_projects = sum(
            1 for project in projects
            if project.get("status") == "Open"
        )

        completed_projects = sum(
            1 for project in projects
            if project.get("status") == "Completed"
        )

        self.create_stat_card(
            stats,
            "Projects",
            total_projects,
            "#E3F2FD",
            "#1976D2"
        )

        self.create_stat_card(
            stats,
            "Open Projects",
            open_projects,
            "#FEF3C7",
            "#92400E"
        )

        self.create_stat_card(
            stats,
            "Completed",
            completed_projects,
            "#D1FAE5",
            "#047857"
        )

        # -----------------------------------------------------
        # Recent projects
        # -----------------------------------------------------

        ctk.CTkLabel(
            main,
            text="Recent Projects",
            font=("Arial", 20, "bold"),
            text_color="#202124"
        ).pack(anchor="w", pady=(5, 12))

        recent_frame = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )
        recent_frame.pack(fill="x")

        if not projects:
            self.show_empty_projects(recent_frame)
        else:
            for project in projects[:5]:
                self.create_project_card(
                    recent_frame,
                    project
                )

        # -----------------------------------------------------
        # Faculty help card
        # -----------------------------------------------------

        help_card = ctk.CTkFrame(
            main,
            fg_color="#1976D2",
            corner_radius=16
        )
        help_card.pack(
            fill="x",
            pady=(30, 10)
        )

        ctk.CTkLabel(
            help_card,
            text="Faculty Collaboration",
            font=("Arial", 21, "bold"),
            text_color="white"
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            help_card,
            text=(
                "Use CollabCampus to discover student projects, "
                "follow collaboration activity and support teams."
            ),
            font=("Arial", 13),
            text_color="#E3F2FD",
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

    # ---------------------------------------------------------
    # ACTION CARD
    # ---------------------------------------------------------

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
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 30)
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 16, "bold"),
            text_color="#202124"
        ).pack(
            anchor="w",
            padx=20
        )

        ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 11),
            text_color="#6B7280",
            wraplength=250,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 12)
        )

        ctk.CTkButton(
            card,
            text="Open",
            width=90,
            height=32,
            corner_radius=8,
            command=command
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

    # ---------------------------------------------------------
    # STAT CARD
    # ---------------------------------------------------------

    def create_stat_card(
        self,
        parent,
        title,
        value,
        bg_color,
        text_color
    ):
        card = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=12
        )
        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Arial", 27, "bold"),
            text_color=text_color
        ).pack(pady=(15, 0))

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            text_color=text_color
        ).pack(pady=(0, 15))

    # ---------------------------------------------------------
    # PROJECT CARD
    # ---------------------------------------------------------

    def create_project_card(self, parent, project):
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=13,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.pack(
            fill="x",
            pady=6,
            padx=5
        )

        content = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        content.pack(
            side="left",
            fill="x",
            expand=True,
            padx=20,
            pady=16
        )

        ctk.CTkLabel(
            content,
            text=project.get("title", "Untitled Project"),
            font=("Arial", 16, "bold"),
            text_color="#202124"
        ).pack(anchor="w")

        description = project.get(
            "description",
            "No description available."
        )

        ctk.CTkLabel(
            content,
            text=description,
            font=("Arial", 11),
            text_color="#6B7280",
            wraplength=650,
            justify="left",
            anchor="w"
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        owner = project.get(
            "owner_name",
            "Unknown"
        )

        ctk.CTkLabel(
            content,
            text=f"Created by {owner}",
            font=("Arial", 10),
            text_color="#9CA3AF"
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

        status = project.get(
            "status",
            "Open"
        )

        status_colors = {
            "Open": ("#D1FAE5", "#047857"),
            "In Progress": ("#DBEAFE", "#1D4ED8"),
            "Completed": ("#E5E7EB", "#374151")
        }

        bg_color, text_color = status_colors.get(
            status,
            ("#F3F4F6", "#374151")
        )

        ctk.CTkLabel(
            card,
            text=status,
            width=105,
            height=30,
            corner_radius=9,
            fg_color=bg_color,
            text_color=text_color,
            font=("Arial", 11, "bold")
        ).pack(
            side="right",
            padx=20
        )

    # ---------------------------------------------------------
    # PROJECT LOADING
    # ---------------------------------------------------------

    def load_projects(self):
        try:
            return get_projects()
        except Exception:
            return []

    def show_empty_projects(self, parent):
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            card,
            text="No projects available",
            font=("Arial", 17, "bold"),
            text_color="#202124"
        ).pack(pady=(25, 4))

        ctk.CTkLabel(
            card,
            text="Student projects will appear here.",
            font=("Arial", 12),
            text_color="#6B7280"
        ).pack(pady=(0, 25))

    # ---------------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------------

    def refresh(self):
        self.destroy()

        FacultyDashboard(
            self.app,
            self.app,
            self.user
        ).pack(fill="both", expand=True)

    def open_projects(self):
        from Frontend.pages.project_marketplace import ProjectMarketplace

        self.destroy()

        ProjectMarketplace(
            self.app,
            self.app,
            self.user
        ).pack(fill="both", expand=True)

    def open_notifications(self):
        from Frontend.pages.notifications_page import NotificationsPage

        self.destroy()

        NotificationsPage(
            self.app,
            self.app,
            self.user
        ).pack(fill="both", expand=True)