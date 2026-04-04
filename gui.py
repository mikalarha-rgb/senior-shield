"""
SeniorShield - Main GUI
Big buttons, simple icons, plain language - designed for seniors.
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from PIL import Image, ImageTk
import logging

from config import load_config, update_trusted_contact
from monitor import ProcessMonitor
from alerts import get_alert_service
from selfhelp import SelfHelpGuide

logger = logging.getLogger(__name__)


class SeniorShieldGUI:
    """Main application window with senior-friendly UI."""

    def __init__(self, root):
        self.root = root
        self.root.title("SeniorShield 🛡️")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")

        # Make window appear in center of screen
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 800) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"800x600+{x}+{y}")

        # Large, friendly fonts
        self.title_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.heading_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.button_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.body_font = tkfont.Font(family="Segoe UI", size=14)
        self.small_font = tkfont.Font(family="Segoe UI", size=12)

        # Services
        self.monitor = ProcessMonitor(callback=self._on_suspicious_event)
        self.alerts = get_alert_service()
        self.selfhelp = SelfHelpGuide()

        # Build UI
        self._build_home()

        # Start monitoring
        self.monitor.start()

        # Protocol
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_home(self):
        """Build the home/main screen."""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="SeniorShield 🛡️",
            font=self.title_font,
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(pady=20)

        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="Your Digital Safety Companion",
            font=self.heading_font,
            fg="#34495e",
            bg="#f0f4f8"
        )
        subtitle.pack(pady=(20, 30))

        # Main help buttons - BIG and friendly
        buttons_frame = tk.Frame(self.root, bg="#f0f4f8")
        buttons_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Row 1
        row1 = tk.Frame(buttons_frame, bg="#f0f4f8")
        row1.pack(fill="x", pady=10)

        self._make_big_button(
            row1, "🖨️", "Printer\nProblems",
            lambda: self._show_help("printer"), "#3498db"
        ).pack(side="left", expand=True, fill="both", padx=5)

        self._make_big_button(
            row1, "🌐", "Internet\nProblems",
            lambda: self._show_help("internet"), "#e67e22"
        ).pack(side="left", expand=True, fill="both", padx=5)

        self._make_big_button(
            row1, "📁", "Can't Find\nMy File",
            lambda: self._show_help("file"), "#9b59b6"
        ).pack(side="left", expand=True, fill="both", padx=5)

        # Row 2
        row2 = tk.Frame(buttons_frame, bg="#f0f4f8")
        row2.pack(fill="x", pady=10)

        self._make_big_button(
            row2, "🔊", "No Sound",
            lambda: self._show_help("sound"), "#1abc9c"
        ).pack(side="left", expand=True, fill="both", padx=5)

        self._make_big_button(
            row2, "📧", "Email\nProblems",
            lambda: self._show_help("email"), "#e74c3c"
        ).pack(side="left", expand=True, fill="both", padx=5)

        self._make_big_button(
            row2, "🖥️", "Screen Looks\nStrange",
            lambda: self._show_help("screen"), "#34495e"
        ).pack(side="left", expand=True, fill="both", padx=5)

        # Warning button - extra prominent
        warning_frame = tk.Frame(self.root, bg="#f0f4f8")
        warning_frame.pack(fill="x", padx=40, pady=(10, 20))

        warning_btn = tk.Button(
            warning_frame,
            text="🚨 Something Feels Wrong - Get Help",
            font=self.button_font,
            bg="#c0392b",
            fg="white",
            activebackground="#e74c3c",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._show_scam_help,
            height=2
        )
        warning_btn.pack(fill="x", pady=10)

        # Status bar
        status_frame = tk.Frame(self.root, bg="#ecf0f1", height=40)
        status_frame.pack(fill="x", side="bottom")

        remote_active, proc = self.monitor.check_active_remote_session()
        if remote_active:
            status_text = f"⚠️ Remote tool detected: {proc}"
            status_color = "#e74c3c"
        else:
            status_text = "✅ Protection Active"
            status_color = "#27ae60"

        self.status_label = tk.Label(
            status_frame,
            text=status_text,
            font=self.small_font,
            fg=status_color,
            bg="#ecf0f1"
        )
        self.status_label.pack(pady=10)

    def _make_big_button(self, parent, emoji, label, command, color):
        """Create a big, friendly button."""
        btn = tk.Button(
            parent,
            text=f"{emoji}\n{label}",
            font=self.button_font,
            bg=color,
            fg="white",
            activebackground=self._darken_color(color),
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=command,
            height=4,
            wraplength=120
        )
        return btn

    def _darken_color(self, hex_color):
        """Darken a hex color for hover effect."""
        color_map = {
            "#3498db": "#2980b9",
            "#e67e22": "#d35400",
            "#9b59b6": "#8e44ad",
            "#1abc9c": "#16a085",
            "#e74c3c": "#c0392b",
            "#34495e": "#2c3e50",
            "#2c3e50": "#1a252f",
            "#c0392b": "#a93226"
        }
        return color_map.get(hex_color, hex_color)

    def _show_help(self, issue_key):
        """Show help for a specific issue."""
        issue = self.selfhelp.get_issue(issue_key)
        if not issue:
            return

        # Build help window
        help_win = tk.Toplevel(self.root)
        help_win.title(issue["title"])
        help_win.geometry("600x500")
        help_win.configure(bg="#f0f4f8")

        # Title
        title = tk.Label(
            help_win,
            text=issue["title"],
            font=self.heading_font,
            fg="#2c3e50",
            bg="#f0f4f8"
        )
        title.pack(pady=20)

        # Steps
        steps_frame = tk.Frame(help_win, bg="#f0f4f8")
        steps_frame.pack(fill="both", expand=True, padx=30, pady=10)

        for i, step in enumerate(issue["steps"], 1):
            step_label = tk.Label(
                steps_frame,
                text=f"{i}. {step}",
                font=self.body_font,
                fg="#34495e",
                bg="#f0f4f8",
                wraplength=500,
                justify="left",
                anchor="w"
            )
            step_label.pack(anchor="w", pady=5)

        # Actions
        if issue.get("actions"):
            actions_frame = tk.Frame(help_win, bg="#f0f4f8")
            actions_frame.pack(fill="x", padx=30, pady=20)

            for action_name, action_func in issue["actions"]:
                if action_func:
                    btn = tk.Button(
                        actions_frame,
                        text=action_name,
                        font=self.button_font,
                        bg="#27ae60",
                        fg="white",
                        activebackground="#219a52",
                        activeforeground="white",
                        relief="flat",
                        cursor="hand2",
                        command=lambda f=action_func: f(),
                        height=2
                    )
                    btn.pack(fill="x", pady=5)

        # Close button
        close_btn = tk.Button(
            help_win,
            text="← Back",
            font=self.button_font,
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=help_win.destroy,
            height=2
        )
        close_btn.pack(fill="x", padx=30, pady=20)

    def _show_scam_help(self):
        """Show scam warning and pressure check."""
        # First, show the "are you being pressured?" check
        self._show_pressure_check()

    def _show_pressure_check(self):
        """Show the 'are you being pressured?' popup."""
        result = messagebox.askyesno(
            "🚨 Quick Check",
            "Is someone on the phone asking you to do something right now?\n\n(Like installing software, sending money, or giving them access to your computer)"
        )

        if result:  # Yes, they're being pressured
            self._handle_under_pressure()
        else:
            # Show scam help anyway
            self._show_help("scam")

    def _handle_under_pressure(self):
        """Handle case where user confirms they're being pressured."""
        # Send alert immediately
        event = {
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "type": "user_under_pressure",
            "description": "User confirmed they are being pressured by someone (likely a scammer)",
            "severity": "high",
            "details": {}
        }

        self.alerts.send_alert(event)

        # Show confirmation
        messagebox.showinfo(
            "✅ Alert Sent",
            "We've sent an alert to your family member.\n\nThey will contact you soon.\n\nRemember: It's okay to hang up!"
        )

    def _on_suspicious_event(self, event):
        """Handle detected suspicious activity."""
        # Send alert
        self.alerts.send_alert(event)

        # Show "are you okay?" popup
        self.root.after(0, lambda: self._show_are_you_ok(event))

    def _show_are_you_ok(self, event):
        """Show 'are you okay?' popup after suspicious event."""
        result = messagebox.askyesno(
            "🛡️ SeniorShield Check",
            f"Something happened on your computer:\n\n{event['description']}\n\nAre you okay? Is someone helping you right now?"
        )

        if not result:
            self._handle_under_pressure()

    def _on_close(self):
        """Handle window close."""
        self.monitor.stop()
        self.root.destroy()


def main():
    """Launch the application."""
    logging.basicConfig(level=logging.INFO)

    root = tk.Tk()
    app = SeniorShieldGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
