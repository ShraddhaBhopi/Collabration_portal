import customtkinter as ctk


class AIAssistantPage(ctk.CTkFrame):
    def __init__(self, parent, app, user):
        super().__init__(parent)

        self.app = app
        self.user = user

        self.configure(fg_color="#F5F7FB")

        self.create_navbar()
        self.create_page()

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
            command=self.back
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
            text="Find Teams",
            width=105,
            height=35,
            fg_color="transparent",
            hover_color="#1565C0",
            text_color="white",
            command=self.open_teammates
        ).pack(side="right", padx=8)

    # ---------------------------------------------------------
    # PAGE
    # ---------------------------------------------------------

    def create_page(self):
        main = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main.pack(
            fill="both",
            expand=True,
            padx=70,
            pady=30
        )

        # Header
        ctk.CTkLabel(
            main,
            text="AI Assistant",
            font=("Arial", 32, "bold"),
            text_color="#202124"
        ).pack(anchor="w")

        ctk.CTkLabel(
            main,
            text="Get quick guidance for your projects, teams and technical work.",
            font=("Arial", 14),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(3, 20))

        # Main card
        card = ctk.CTkFrame(
            main,
            fg_color="white",
            corner_radius=16,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.pack(
            fill="both",
            expand=True
        )

        # Assistant header
        assistant_header = ctk.CTkFrame(
            card,
            fg_color="#EFF6FF",
            corner_radius=12
        )
        assistant_header.pack(
            fill="x",
            padx=18,
            pady=18
        )

        avatar = ctk.CTkLabel(
            assistant_header,
            text="AI",
            width=55,
            height=55,
            corner_radius=28,
            fg_color="#1976D2",
            text_color="white",
            font=("Arial", 17, "bold")
        )
        avatar.pack(
            side="left",
            padx=(15, 12),
            pady=12
        )

        info = ctk.CTkFrame(
            assistant_header,
            fg_color="transparent"
        )
        info.pack(
            side="left",
            pady=10
        )

        ctk.CTkLabel(
            info,
            text="CollabCampus Assistant",
            font=("Arial", 17, "bold"),
            text_color="#202124"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text="Ask me about teams, projects, tasks or technology.",
            font=("Arial", 11),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(3, 0))

        # Suggestions
        ctk.CTkLabel(
            card,
            text="Try asking",
            font=("Arial", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=25,
            pady=(5, 7)
        )

        suggestions = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        suggestions.pack(
            fill="x",
            padx=20
        )

        questions = [
            "How can I find teammates?",
            "How do I create a project?",
            "What skills should my team have?",
            "How can I organize project tasks?"
        ]

        for question in questions:
            ctk.CTkButton(
                suggestions,
                text=question,
                height=32,
                corner_radius=8,
                fg_color="#F8FAFC",
                hover_color="#E3F2FD",
                text_color="#374151",
                border_width=1,
                border_color="#D1D5DB",
                command=lambda q=question: self.use_question(q)
            ).pack(
                side="left",
                padx=4,
                pady=3
            )

        # Question label
        ctk.CTkLabel(
            card,
            text="Your question",
            font=("Arial", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 5)
        )

        self.question = ctk.CTkEntry(
            card,
            height=42,
            placeholder_text="Ask something about CollabCampus..."
        )
        self.question.pack(
            fill="x",
            padx=25
        )

        # Ask button
        ctk.CTkButton(
            card,
            text="Ask Assistant",
            width=140,
            height=38,
            corner_radius=9,
            fg_color="#1976D2",
            hover_color="#1565C0",
            command=self.generate_response
        ).pack(
            anchor="e",
            padx=25,
            pady=10
        )

        # Response
        ctk.CTkLabel(
            card,
            text="Assistant Response",
            font=("Arial", 13, "bold"),
            text_color="#374151"
        ).pack(
            anchor="w",
            padx=25,
            pady=(3, 5)
        )

        self.response = ctk.CTkTextbox(
            card,
            height=170,
            font=("Arial", 13),
            corner_radius=10,
            fg_color="#F8FAFC",
            border_width=1,
            border_color="#E5E7EB"
        )
        self.response.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        self.response.insert(
            "1.0",
            "Hello! 👋\n\n"
            "I can help you understand how to use CollabCampus "
            "and organize your project work."
        )

    # ---------------------------------------------------------
    # SUGGESTED QUESTION
    # ---------------------------------------------------------

    def use_question(self, question):
        self.question.delete(0, "end")
        self.question.insert(0, question)
        self.generate_response()

    # ---------------------------------------------------------
    # RESPONSE
    # ---------------------------------------------------------

    def generate_response(self):
        question = self.question.get().strip().lower()

        if not question:
            self.set_response(
                "Please enter a question first."
            )
            return

        if "team" in question or "teammate" in question:
            answer = (
                "You can find teammates using the Find Teams page. "
                "Search for students based on their technical skills "
                "and profile information, then connect with suitable "
                "team members."
            )

        elif "project" in question and (
            "create" in question
            or "post" in question
            or "start" in question
        ):
            answer = (
                "To create a project, open the Project Marketplace "
                "and select '+ Post Project'. Enter the project title, "
                "description and required skills, then publish it."
            )

        elif "skill" in question:
            answer = (
                "A good project team should have complementary skills. "
                "For example, a software project could include members "
                "with programming, database, UI/UX and testing skills."
            )

        elif "task" in question:
            answer = (
                "Use the Tasks section inside a project workspace. "
                "You can create tasks, describe them and organize "
                "the project's work into smaller responsibilities."
            )

        elif "python" in question:
            answer = (
                "Python can be useful for backend development, "
                "automation, data analysis and AI/ML projects."
            )

        elif "database" in question or "mysql" in question:
            answer = (
                "MySQL is used by CollabCampus to store users, "
                "projects, team members, tasks and notifications."
            )

        else:
            answer = (
                "I can help with teams, projects, skills, tasks, "
                "Python and databases. Try asking one of those topics."
            )

        self.set_response(answer)

    def set_response(self, text):
        self.response.delete("1.0", "end")
        self.response.insert("1.0", text)

    # ---------------------------------------------------------
    # NAVIGATION
    # ---------------------------------------------------------

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

    def open_teammates(self):
        from Frontend.pages.find_teammates import FindTeammatesPage

        self.destroy()

        FindTeammatesPage(
            self.app,
            self.app,
            self.user
        ).pack(fill="both", expand=True)