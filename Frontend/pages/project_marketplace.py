import customtkinter as ctk

from Backend.projects import get_projects, join_project
from Frontend.pages.project_workspace import ProjectWorkspace


class ProjectMarketplace(ctk.CTkFrame):

    def __init__(self, parent, app, user):
        super().__init__(parent)

        self.app = app
        self.user = user

        self.configure(fg_color="#F5F7FB")

        self.create_navbar()
        self.create_content()

        self.load_projects()

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
            width=110,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_teammates
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

    # ---------------- CONTENT ----------------

    def create_content(self):

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
            text="Project Marketplace",
            font=("Arial", 32, "bold"),
            text_color="#202124"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self.content,
            text="Discover projects and find your next team",
            font=("Arial", 15),
            text_color="#6B7280"
        ).pack(pady=(0, 20))

        # Search area

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
            placeholder_text="🔍  Search projects...",
            border_width=0,
            font=("Arial", 15)
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=8
        )

        ctk.CTkButton(
            search_frame,
            text="Search",
            width=120,
            height=40,
            command=self.search_projects
        ).pack(
            side="right",
            padx=8
        )

        # Filter buttons

        filter_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        filter_frame.pack(pady=15)

        for status in ["All Projects", "Open", "In Progress", "Completed"]:

            ctk.CTkButton(
                filter_frame,
                text=status,
                width=110,
                height=32,
                corner_radius=8,
                fg_color="white",
                hover_color="#E3F2FD",
                text_color="#374151",
                border_width=1,
                border_color="#D1D5DB",
                command=lambda s=status: self.filter_projects(s)
            ).pack(
                side="left",
                padx=4
            )

        # Project results

        self.projects_frame = ctk.CTkScrollableFrame(
            self.content,
            fg_color="transparent"
        )

        self.projects_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

    # ---------------- LOAD PROJECTS ----------------

    def load_projects(self, projects=None):

        for widget in self.projects_frame.winfo_children():
            widget.destroy()

        if projects is None:

            try:
                projects = get_projects()

            except Exception as error:

                ctk.CTkLabel(
                    self.projects_frame,
                    text=f"Database unavailable.\n\n{error}",
                    font=("Arial", 15),
                    text_color="#6B7280",
                    wraplength=700
                ).pack(pady=60)

                return

        if not projects:

            ctk.CTkLabel(
                self.projects_frame,
                text="No projects available yet.",
                font=("Arial", 18),
                text_color="#6B7280"
            ).pack(pady=60)

            return

        row = None

        for index, project in enumerate(projects):

            if index % 3 == 0:

                row = ctk.CTkFrame(
                    self.projects_frame,
                    fg_color="transparent"
                )

                row.pack(
                    fill="x",
                    pady=8
                )

            self.create_project_card(
                row,
                project
            )

    # ---------------- PROJECT CARD ----------------

    def create_project_card(self, parent, project):

        card = ctk.CTkFrame(
            parent,
            width=310,
            height=310,
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

        # Status badge

        status = project["status"]

        status_color = {
            "Open": "#D1FAE5",
            "In Progress": "#FEF3C7",
            "Completed": "#E5E7EB"
        }.get(status, "#E5E7EB")

        status_text_color = {
            "Open": "#047857",
            "In Progress": "#B45309",
            "Completed": "#4B5563"
        }.get(status, "#4B5563")

        ctk.CTkLabel(
            card,
            text=status,
            fg_color=status_color,
            text_color=status_text_color,
            corner_radius=8,
            font=("Arial", 11, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 8)
        )

        # Title

        ctk.CTkLabel(
            card,
            text=project["title"],
            font=("Arial", 18, "bold"),
            text_color="#202124",
            wraplength=270,
            justify="left"
        ).pack(
            anchor="w",
            padx=18,
            pady=3
        )

        # Description

        description = project["description"]

        ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 12),
            text_color="#6B7280",
            wraplength=270,
            justify="left"
        ).pack(
            anchor="w",
            padx=18,
            pady=(8, 5)
        )

        # Owner

        ctk.CTkLabel(
            card,
            text=f"Led by  {project['owner_name']}",
            font=("Arial", 12),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=18,
            pady=5
        )

        # Buttons

        button_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        button_frame.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15
        )

        ctk.CTkButton(
            button_frame,
            text="Join Team",
            height=35,
            corner_radius=7,
            command=lambda pid=project["id"]:
                self.join_team(pid)
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        ctk.CTkButton(
            button_frame,
            text="Workspace",
            height=35,
            corner_radius=7,
            fg_color="white",
            text_color="#1976D2",
            border_width=1,
            border_color="#1976D2",
            hover_color="#E3F2FD",
            command=lambda p=project:
                self.open_workspace(p)
        ).pack(
            side="right",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

    # ---------------- SEARCH ----------------

    def search_projects(self):

        query = self.search_entry.get().strip().lower()

        try:
            projects = get_projects()

        except Exception as error:

            self.load_projects()
            return

        if query:

            projects = [
                project
                for project in projects
                if query in project["title"].lower()
                or query in project["description"].lower()
                or query in project["owner_name"].lower()
            ]

        self.load_projects(projects)

    # ---------------- FILTER ----------------

    def filter_projects(self, status):

        try:
            projects = get_projects()

        except Exception:
            self.load_projects()
            return

        if status != "All Projects":

            projects = [
                project
                for project in projects
                if project["status"] == status
            ]

        self.load_projects(projects)

    # ---------------- JOIN ----------------

    def join_team(self, project_id):

        try:

            success = join_project(
                project_id,
                self.user["id"]
            )

            if success:

                self.show_message(
                    "You have successfully joined the project.",
                    "Success"
                )

            else:

                self.show_message(
                    "You could not join this project.\n"
                    "You may already be a member.",
                    "Information"
                )

        except Exception as error:

            self.show_message(
                str(error),
                "Error"
            )

    # ---------------- WORKSPACE ----------------

    def open_workspace(self, project):

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

    # ---------------- MESSAGE ----------------

    def show_message(self, message, title):

        dialog = ctk.CTkToplevel(self)

        dialog.title(title)
        dialog.geometry("430x220")

        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=350,
            justify="center",
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