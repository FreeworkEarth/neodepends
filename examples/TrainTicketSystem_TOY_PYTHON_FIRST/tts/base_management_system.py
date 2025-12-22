"""
Base Management System - Abstract base class
All management systems extend this to provide logging and statistics
This is the exact Python equivalent of Java's BaseManagementSystem
"""


class BaseManagementSystem:
    """Base class for management systems"""

    def log_action(self, action: str):
        """
        Log an action for auditing purposes

        Args:
            action: The action to log
        """
        print(f"[LOG] {action}")

    def display_system_stats(self):
        """
        Display system statistics
        Must be implemented by subclasses
        """
        raise NotImplementedError("Subclass must implement display_system_stats()")
