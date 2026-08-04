"""
StationManager - IMPROVED: Reduced to just employee data
Management logic moved to ManagementService
"""
import importlib

from tts.staff import Staff


class StationManager(Staff):
    """StationManager with minimal coupling"""

    def __init__(self, name: str, person_id: str, email: str, phone: str,
                 employee_id: str, salary: float, managed_station_id: str):
        super().__init__(name, person_id, email, phone, employee_id, salary)
        self.managed_station_id = managed_station_id  # CHANGED: ID not object!

    def display_info(self):
        print(f"Station Manager: {self.name} (ID: {self.employee_id})")
        print(f"Managed Station: {self.managed_station_id}")
        print(f"Salary: ${self.salary}")

    def get_station_repo(self):
        """Dynamically load the station repository module.

        Failure-mode fixture R3 (importlib.import_module with constant string):
        this creates a real runtime dependency on tts.train_station_repository,
        but static analysis cannot see it — the target is a string literal.
        NeoDepends should ideally detect this and add an Import edge, but
        currently it is invisible.
        """
        mod = importlib.import_module("tts.train_station_repository")
        return mod.TrainStationRepository()
