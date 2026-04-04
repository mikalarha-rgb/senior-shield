"""
SeniorShield - Process Monitor
Watches for suspicious remote access tools and risky behavior patterns.
"""

import time
import psutil
import logging
from datetime import datetime
from threading import Thread, Event
from config import load_config

logger = logging.getLogger(__name__)


class ProcessMonitor:
    """Monitors running processes for suspicious activity."""

    def __init__(self, callback=None):
        self.callback = callback  # Called when suspicious activity detected
        self.running = False
        self._thread = None
        self._stop_event = Event()
        self._config = None
        self._known_processes = set()
        self._suspicious_events = []

    def _load_config(self):
        self._config = load_config()

    def start(self):
        """Start monitoring in background thread."""
        if self.running:
            return

        self._load_config()
        self.running = True
        self._stop_event.clear()
        self._thread = Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        logger.info("Process monitor started")

    def stop(self):
        """Stop monitoring."""
        self.running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)
        logger.info("Process monitor stopped")

    def _monitor_loop(self):
        """Main monitoring loop."""
        # Initial scan - record what's already running
        self._known_processes = self._get_running_processes()

        while not self._stop_event.is_set():
            try:
                current_processes = self._get_running_processes()
                new_processes = current_processes - self._known_processes

                # Check for suspicious new processes
                remote_tools = [t.lower() for t in self._config["monitoring"]["remote_access_tools"]]

                for proc in new_processes:
                    proc_name = proc.lower()
                    for tool in remote_tools:
                        if tool in proc_name or proc_name in tool.replace(".exe", ""):
                            self._handle_suspicious_event(
                                event_type="remote_access_launch",
                                description=f"Remote access tool detected: {proc}",
                                severity="high",
                                details={"process": proc}
                            )

                # Update known processes
                self._known_processes = current_processes

            except Exception as e:
                logger.error(f"Monitor error: {e}")

            # Check every 2 seconds
            self._stop_event.wait(2)

    def _get_running_processes(self):
        """Get set of currently running process names."""
        processes = set()
        for proc in psutil.process_iter(['name']):
            try:
                processes.add(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes

    def _handle_suspicious_event(self, event_type, description, severity, details=None):
        """Handle a detected suspicious event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "description": description,
            "severity": severity,
            "details": details or {}
        }

        logger.warning(f"Suspicious event: {event}")
        self._suspicious_events.append(event)

        if self.callback:
            self.callback(event)

    def get_recent_events(self, limit=10):
        """Get recent suspicious events."""
        return self._suspicious_events[-limit:]

    def check_active_remote_session(self):
        """Check if any remote access tool is currently running."""
        current = self._get_running_processes()
        remote_tools = [t.lower() for t in self._config["monitoring"]["remote_access_tools"]]

        for proc in current:
            proc_lower = proc.lower()
            for tool in remote_tools:
                if tool in proc_lower:
                    return True, proc
        return False, None
