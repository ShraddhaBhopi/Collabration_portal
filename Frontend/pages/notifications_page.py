import customtkinter as ctk
from Backend.notifications import get_notifications, mark_notification_read


class NotificationsPage(ctk.CTkFrame):
    def __init__(self, parent, app, user):
        super().__init__(parent)
        self.app = app
        self.user = user

        self.configure(fg_color="#F5F7FB")

        self.create_navbar()
        self.create_page()

        self.load_notifications()

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
        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.main.pack(
            fill="both",
            expand=True,
            padx=70,
            pady=30
        )

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
            text="Notifications",
            font=("Arial", 32, "bold"),
            text_color="#202124"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Stay updated with your projects and team activity.",
            font=("Arial", 14),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(3, 0))

        self.mark_all_button = ctk.CTkButton(
            header,
            text="✓  Mark All as Read",
            width=145,
            height=38,
            corner_radius=9,
            fg_color="#1976D2",
            hover_color="#1565C0",
            command=self.mark_all_read
        )
        self.mark_all_button.pack(side="right", pady=10)

        self.status_label = ctk.CTkLabel(
            self.main,
            text="",
            font=("Arial", 12),
            text_color="#6B7280"
        )
        self.status_label.pack(anchor="w", pady=(0, 10))

        self.notifications_frame = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )
        self.notifications_frame.pack(fill="both", expand=True)

    # ---------------------------------------------------------
    # LOAD NOTIFICATIONS
    # ---------------------------------------------------------

    def load_notifications(self):
        for widget in self.notifications_frame.winfo_children():
            widget.destroy()

        try:
            notifications = get_notifications(self.user["id"])

        except Exception as error:
            self.status_label.configure(
                text=f"Unable to load notifications: {error}",
                text_color="#B91C1C"
            )
            return

        unread_count = sum(
            1 for notification in notifications
            if not notification["is_read"]
        )

        if unread_count:
            self.status_label.configure(
                text=f"{unread_count} unread notification"
                     f"{'s' if unread_count != 1 else ''}",
                text_color="#1976D2"
            )
        else:
            self.status_label.configure(
                text="You're all caught up.",
                text_color="#047857"
            )

        if not notifications:
            self.show_empty_state()
            return

        for notification in notifications:
            self.create_notification_card(notification)

    # ---------------------------------------------------------
    # NOTIFICATION CARD
    # ---------------------------------------------------------

    def create_notification_card(self, notification):
        is_unread = not notification["is_read"]

        card_color = "#EFF6FF" if is_unread else "white"
        border_color = "#BFDBFE" if is_unread else "#E5E7EB"

        card = ctk.CTkFrame(
            self.notifications_frame,
            fg_color=card_color,
            corner_radius=14,
            border_width=1,
            border_color=border_color
        )
        card.pack(
            fill="x",
            pady=7,
            padx=5
        )

        # Left notification icon
        icon = ctk.CTkLabel(
            card,
            text="🔔",
            width=45,
            height=45,
            corner_radius=23,
            fg_color="#DBEAFE" if is_unread else "#F3F4F6",
            font=("Arial", 20)
        )
        icon.pack(
            side="left",
            padx=(18, 12),
            pady=18
        )

        # Main content
        content = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        content.pack(
            side="left",
            fill="x",
            expand=True,
            pady=15
        )

        message = notification.get("message", "")

        ctk.CTkLabel(
            content,
            text=message,
            font=("Arial", 14, "bold" if is_unread else "normal"),
            text_color="#202124",
            anchor="w",
            justify="left",
            wraplength=650
        ).pack(anchor="w")

        created_at = notification.get("created_at")

        if created_at:
            created_text = str(created_at)

            ctk.CTkLabel(
                content,
                text=created_text,
                font=("Arial", 11),
                text_color="#6B7280"
            ).pack(anchor="w", pady=(5, 0))

        # Right side
        right_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        right_frame.pack(
            side="right",
            padx=18
        )

        if is_unread:
            ctk.CTkLabel(
                right_frame,
                text="NEW",
                width=50,
                height=25,
                corner_radius=8,
                fg_color="#1976D2",
                text_color="white",
                font=("Arial", 10, "bold")
            ).pack(pady=(0, 7))

            ctk.CTkButton(
                right_frame,
                text="Mark as read",
                width=105,
                height=30,
                corner_radius=7,
                fg_color="white",
                hover_color="#E3F2FD",
                text_color="#1976D2",
                border_width=1,
                border_color="#93C5FD",
                command=lambda n=notification:
                    self.mark_read(n["id"])
            ).pack()

    # ---------------------------------------------------------
    # EMPTY STATE
    # ---------------------------------------------------------

    def show_empty_state(self):
        empty_card = ctk.CTkFrame(
            self.notifications_frame,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E5E7EB"
        )
        empty_card.pack(
            fill="x",
            pady=30,
            padx=30
        )

        ctk.CTkLabel(
            empty_card,
            text="🔔",
            font=("Arial", 42)
        ).pack(pady=(35, 10))

        ctk.CTkLabel(
            empty_card,
            text="No notifications yet",
            font=("Arial", 20, "bold"),
            text_color="#202124"
        ).pack()

        ctk.CTkLabel(
            empty_card,
            text="Project updates and team activity will appear here.",
            font=("Arial", 13),
            text_color="#6B7280"
        ).pack(pady=(5, 35))

    # ---------------------------------------------------------
    # MARK READ
    # ---------------------------------------------------------

    def mark_read(self, notification_id):
        try:
            mark_notification_read(
                notification_id,
                self.user["id"]
            )
            self.load_notifications()

        except Exception as error:
            self.status_label.configure(
                text=f"Unable to update notification: {error}",
                text_color="#B91C1C"
            )

    # ---------------------------------------------------------
    # MARK ALL READ
    # ---------------------------------------------------------

    def mark_all_read(self):
        try:
            notifications = get_notifications(self.user["id"])

            for notification in notifications:
                if not notification["is_read"]:
                    mark_notification_read(
                        notification["id"],
                        self.user["id"]
                    )

            self.load_notifications()

        except Exception as error:
            self.status_label.configure(
                text=f"Unable to update notifications: {error}",
                text_color="#B91C1C"
            )

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