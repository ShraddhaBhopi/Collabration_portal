import customtkinter as ctk
from Backend.tasks import add_task, get_tasks


class TasksPage(ctk.CTkFrame):
    def __init__(self, parent, app, user, project):
        super().__init__(parent)

        self.app = app
        self.user = user
        self.project = project

        self.configure(fg_color="#F5F7FB")

        self.create_navbar()
        self.create_page()

        self.load_tasks()

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
            text="Workspace",
            width=100,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.back_to_workspace
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
            text="Dashboard",
            width=100,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.back
        ).pack(side="right", padx=8)

    # ---------------------------------------------------------
    # PAGE
    # ---------------------------------------------------------

    def create_page(self):
        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.main.pack(
            fill="both",
            expand=True,
            padx=65,
            pady=30
        )

        # Header
        header = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        header.pack(fill="x", pady=(5, 20))

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        title_frame.pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="Project Tasks",
            font=("Arial", 32, "bold"),
            text_color="#202124"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text=self.project.get("title", "Project"),
            font=("Arial", 14),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(4, 0))

        ctk.CTkButton(
            header,
            text="+  Add Task",
            width=125,
            height=40,
            corner_radius=9,
            fg_color="#1976D2",
            hover_color="#1565C0",
            command=self.show_add_task
        ).pack(side="right", pady=8)

        # Add task section
        self.add_task_card = ctk.CTkFrame(
            self.main,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E5E7EB"
        )

        # Hidden initially
        self.add_task_card.pack_forget()

        # Task list title
        ctk.CTkLabel(
            self.main,
            text="Task Board",
            font=("Arial", 20, "bold"),
            text_color="#202124"
        ).pack(anchor="w", pady=(10, 12))

        self.tasks_frame = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        self.tasks_frame.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # ADD TASK FORM
    # ---------------------------------------------------------

    def show_add_task(self):
        if self.add_task_card.winfo_ismapped():
            self.add_task_card.pack_forget()
            return

        self.add_task_card.pack(
            fill="x",
            pady=(0, 20),
            padx=5
        )

        for widget in self.add_task_card.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.add_task_card,
            text="Create New Task",
            font=("Arial", 19, "bold"),
            text_color="#202124"
        ).pack(anchor="w", padx=25, pady=(20, 3))

        ctk.CTkLabel(
            self.add_task_card,
            text="Add a task for your project team.",
            font=("Arial", 12),
            text_color="#6B7280"
        ).pack(anchor="w", padx=25)

        ctk.CTkLabel(
            self.add_task_card,
            text="Task Title",
            font=("Arial", 13, "bold"),
            text_color="#374151"
        ).pack(anchor="w", padx=25, pady=(18, 5))

        self.task_title = ctk.CTkEntry(
            self.add_task_card,
            height=40,
            placeholder_text="e.g. Design login page"
        )
        self.task_title.pack(fill="x", padx=25)

        ctk.CTkLabel(
            self.add_task_card,
            text="Description",
            font=("Arial", 13, "bold"),
            text_color="#374151"
        ).pack(anchor="w", padx=25, pady=(15, 5))

        self.task_description = ctk.CTkTextbox(
            self.add_task_card,
            height=100
        )
        self.task_description.pack(fill="x", padx=25)

        self.form_message = ctk.CTkLabel(
            self.add_task_card,
            text="",
            font=("Arial", 12)
        )
        self.form_message.pack(pady=(12, 3))

        buttons = ctk.CTkFrame(
            self.add_task_card,
            fg_color="transparent"
        )
        buttons.pack(pady=(5, 20))

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=100,
            height=35,
            fg_color="white",
            text_color="#374151",
            border_width=1,
            border_color="#D1D5DB",
            hover_color="#F3F4F6",
            command=self.hide_add_task
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Create Task",
            width=120,
            height=35,
            command=self.create_task
        ).pack(side="left", padx=5)

    def hide_add_task(self):
        self.add_task_card.pack_forget()

    # ---------------------------------------------------------
    # CREATE TASK
    # ---------------------------------------------------------

    def create_task(self):
        title = self.task_title.get().strip()
        description = self.task_description.get(
            "1.0",
            "end"
        ).strip()

        if not title:
            self.form_message.configure(
                text="Task title is required.",
                text_color="#B91C1C"
            )
            return

        try:
            add_task(
                self.project["id"],
                title,
                description
            )

            self.hide_add_task()
            self.load_tasks()

        except Exception as error:
            self.form_message.configure(
                text=f"Unable to create task: {error}",
                text_color="#B91C1C"
            )

    # ---------------------------------------------------------
    # LOAD TASKS
    # ---------------------------------------------------------

    def load_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        try:
            tasks = get_tasks(self.project["id"])

        except Exception as error:
            self.show_error(
                f"Unable to load tasks: {error}"
            )
            return

        if not tasks:
            self.show_empty_state()
            return

        # Counters
        pending = sum(
            1 for task in tasks
            if task["status"] == "Pending"
        )

        progress = sum(
            1 for task in tasks
            if task["status"] == "In Progress"
        )

        completed = sum(
            1 for task in tasks
            if task["status"] == "Completed"
        )

        summary = ctk.CTkFrame(
            self.tasks_frame,
            fg_color="transparent"
        )
        summary.pack(fill="x", pady=(0, 15))

        self.create_summary_card(
            summary,
            "Pending",
            pending,
            "#FEF3C7",
            "#92400E"
        )

        self.create_summary_card(
            summary,
            "In Progress",
            progress,
            "#DBEAFE",
            "#1D4ED8"
        )

        self.create_summary_card(
            summary,
            "Completed",
            completed,
            "#D1FAE5",
            "#047857"
        )

        for task in tasks:
            self.create_task_card(task)

    # ---------------------------------------------------------
    # SUMMARY CARD
    # ---------------------------------------------------------

    def create_summary_card(
        self,
        parent,
        title,
        count,
        bg_color,
        text_color
    ):
        card = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=10
        )
        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        ctk.CTkLabel(
            card,
            text=str(count),
            font=("Arial", 24, "bold"),
            text_color=text_color
        ).pack(pady=(12, 0))

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 11, "bold"),
            text_color=text_color
        ).pack(pady=(0, 12))

    # ---------------------------------------------------------
    # TASK CARD
    # ---------------------------------------------------------

    def create_task_card(self, task):
        card = ctk.CTkFrame(
            self.tasks_frame,
            fg_color="white",
            corner_radius=14,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.pack(
            fill="x",
            pady=7,
            padx=5
        )

        left = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        left.pack(
            side="left",
            fill="x",
            expand=True,
            padx=20,
            pady=18
        )

        ctk.CTkLabel(
            left,
            text=task.get("title", "Untitled Task"),
            font=("Arial", 16, "bold"),
            text_color="#202124"
        ).pack(anchor="w")

        description = task.get("description")

        if description:
            ctk.CTkLabel(
                left,
                text=description,
                font=("Arial", 12),
                text_color="#6B7280",
                justify="left",
                anchor="w",
                wraplength=650
            ).pack(anchor="w", pady=(5, 0))

        assigned_to = task.get("assigned_to")

        if assigned_to:
            ctk.CTkLabel(
                left,
                text=f"Assigned to user #{assigned_to}",
                font=("Arial", 11),
                text_color="#9CA3AF"
            ).pack(anchor="w", pady=(7, 0))

        status = task.get("status", "Pending")

        status_colors = {
            "Pending": ("#FEF3C7", "#92400E"),
            "In Progress": ("#DBEAFE", "#1D4ED8"),
            "Completed": ("#D1FAE5", "#047857")
        }

        bg_color, text_color = status_colors.get(
            status,
            ("#F3F4F6", "#374151")
        )

        status_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        status_frame.pack(
            side="right",
            padx=20
        )

        ctk.CTkLabel(
            status_frame,
            text=status,
            width=100,
            height=30,
            corner_radius=9,
            fg_color=bg_color,
            text_color=text_color,
            font=("Arial", 11, "bold")
        ).pack()

    # ---------------------------------------------------------
    # EMPTY STATE
    # ---------------------------------------------------------

    def show_empty_state(self):
        card = ctk.CTkFrame(
            self.tasks_frame,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.pack(
            fill="x",
            padx=30,
            pady=30
        )

        ctk.CTkLabel(
            card,
            text="✓",
            font=("Arial", 42),
            text_color="#1976D2"
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            card,
            text="No tasks yet",
            font=("Arial", 20, "bold"),
            text_color="#202124"
        ).pack()

        ctk.CTkLabel(
            card,
            text="Create your first task to start organizing the project.",
            font=("Arial", 13),
            text_color="#6B7280"
        ).pack(pady=(5, 35))

    # ---------------------------------------------------------
    # ERROR
    # ---------------------------------------------------------

    def show_error(self, message):
        card = ctk.CTkFrame(
            self.tasks_frame,
            fg_color="#FEF2F2",
            corner_radius=12,
            border_width=1,
            border_color="#FECACA"
        )
        card.pack(
            fill="x",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            card,
            text=message,
            font=("Arial", 12),
            text_color="#B91C1C",
            wraplength=700
        ).pack(pady=20)

    # ---------------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------------

    def back_to_workspace(self):
        from Frontend.pages.project_workspace import ProjectWorkspace

        self.destroy()

        ProjectWorkspace(
            self.app,
            self.app,
            self.user,
            self.project
        ).pack(fill="both", expand=True)

    def back(self):
        from Frontend.pages.student_dashboard import StudentDashboard

        self.destroy()

        StudentDashboard(
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