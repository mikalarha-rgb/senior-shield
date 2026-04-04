"""
SeniorShield - Self-Help Guide
Simple guided help for common tech problems seniors face.
"""

import subprocess
import logging
from pathlib import Path
import webbrowser

logger = logging.getLogger(__name__)


class SelfHelpGuide:
    """Provides simple, plain-language help for common tech problems."""

    def __init__(self):
        self._common_issues = {
            "printer": {
                "title": "🖨️ Printer Problems",
                "steps": [
                    "Is the printer turned on?",
                    "Is it connected to the computer (USB or Wi-Fi)?",
                    "Is there paper in the tray?",
                    "Try turning the printer off and back on.",
                    "If nothing works, we can search for a solution."
                ],
                "actions": [
                    ("Open Printer Settings", self._open_printer_settings),
                    ("Search Online Help", lambda: self._search_help("printer not working"))
                ]
            },
            "internet": {
                "title": "🌐 Internet / Wi-Fi Problems",
                "steps": [
                    "Is your Wi-Fi turned on?",
                    "Are you close enough to your router?",
                    "Try turning Wi-Fi off and back on.",
                    "Restart your computer.",
                    "If still not working, try turning off your router for 30 seconds."
                ],
                "actions": [
                    ("Open Wi-Fi Settings", self._open_wifi_settings),
                    ("Search Online Help", lambda: self._search_help("wifi not connecting"))
                ]
            },
            "file": {
                "title": "📁 Missing Files",
                "steps": [
                    "Check your Desktop.",
                    "Check your Documents folder.",
                    "Did you save it with a specific name?",
                    "Try using Windows Search (the magnifying glass).",
                    "Files are sometimes in the Downloads folder."
                ],
                "actions": [
                    ("Search for File", self._search_files),
                    ("Open Documents", self._open_documents),
                    ("Open Downloads", self._open_downloads)
                ]
            },
            "email": {
                "title": "📧 Email Problems",
                "steps": [
                    "Check your internet connection first.",
                    "Try refreshing your inbox.",
                    "Check your Spam/Junk folder.",
                    "Make sure you typed the email address correctly.",
                    "Try logging out and back in."
                ],
                "actions": [
                    ("Open Email", lambda: webbrowser.open("https://mail.google.com")),
                    ("Search Online", lambda: self._search_help("email not loading"))
                ]
            },
            "screen": {
                "title": "🖥️ Screen Looks Strange",
                "steps": [
                    "Did anything change recently?",
                    "Try pressing F11 (may toggle fullscreen).",
                    "Try restarting your computer.",
                    "Check if the display cable is loose.",
                    "Is it a pop-up? Don't click anything unusual!"
                ],
                "actions": [
                    ("Restart Computer", self._restart_computer),
                    ("Search Online", lambda: self._search_help("screen looks wrong windows"))
                ]
            },
            "sound": {
                "title": "🔊 No Sound",
                "steps": [
                    "Is the volume turned up? (Bottom right corner)",
                    "Are headphones plugged in?",
                    "Try restarting your computer.",
                    "Check if sound is muted.",
                    "Make sure the right speaker is selected."
                ],
                "actions": [
                    ("Open Sound Settings", self._open_sound_settings),
                    ("Search Online", lambda: self._search_help("no sound windows computer"))
                ]
            },
            "scam": {
                "title": "🚨 Someone Called About My Computer",
                "steps": [
                    "⚠️ Microsoft, Apple, and others NEVER call you first.",
                    "⚠️ Never give anyone remote access to your computer.",
                    "⚠️ Never send money or gift cards.",
                    "If someone is pressuring you, hang up.",
                    "It's okay to say NO."
                ],
                "actions": [
                    ("⚠️ Get Help Now - Are you being scammed?", None)
                ],
                "is_scam": True
            },
            "popup": {
                "title": "⚠️ Strange Pop-ups",
                "steps": [
                    "⚠️ Do NOT click on anything suspicious.",
                    "⚠️ Do NOT call any phone numbers shown.",
                    "⚠️ Do NOT download anything.",
                    "Try closing the browser completely (Ctrl+Shift+X).",
                    "If it keeps coming back, restart your computer."
                ],
                "actions": [
                    ("Close Everything & Restart", self._restart_computer),
                    ("Search for Help", lambda: self._search_help("remove virus popup from browser"))
                ],
                "is_suspicious": True
            }
        }

    def get_issue(self, key):
        """Get help for a specific issue."""
        return self._common_issues.get(key)

    def get_all_issues(self):
        """Get all available help topics."""
        return list(self._common_issues.keys())

    def get_issue_title(self, key):
        """Get just the title for an issue."""
        issue = self._common_issues.get(key)
        return issue["title"] if issue else None

    # --- Actions ---

    def _open_printer_settings(self):
        """Open Windows printer settings."""
        try:
            subprocess.run(["control", "printers"], shell=True)
        except Exception as e:
            logger.error(f"Failed to open printer settings: {e}")

    def _open_wifi_settings(self):
        """Open Windows Wi-Fi settings."""
        try:
            subprocess.run(["ms-settings:network"], shell=True)
        except Exception as e:
            logger.error(f"Failed to open Wi-Fi settings: {e}")

    def _open_documents(self):
        """Open Documents folder."""
        try:
            subprocess.run(["explorer", str(Path.home() / "Documents")])
        except Exception as e:
            logger.error(f"Failed to open documents: {e}")

    def _open_downloads(self):
        """Open Downloads folder."""
        try:
            subprocess.run(["explorer", str(Path.home() / "Downloads")])
        except Exception as e:
            logger.error(f"Failed to open downloads: {e}")

    def _search_files(self):
        """Open Windows search."""
        try:
            subprocess.run(["explorer", "shell:searchHomeFolder"])
        except Exception as e:
            logger.error(f"Failed to open search: {e}")

    def _open_sound_settings(self):
        """Open Windows sound settings."""
        try:
            subprocess.run(["ms-settings:sound"], shell=True)
        except Exception as e:
            logger.error(f"Failed to open sound settings: {e}")

    def _restart_computer(self):
        """Restart the computer."""
        try:
            subprocess.run(["shutdown", "/r", "/t", "60", "/c", "SeniorShield is restarting your computer."], shell=True)
        except Exception as e:
            logger.error(f"Failed to initiate restart: {e}")

    def _search_help(self, query):
        """Open browser with search query."""
        try:
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
