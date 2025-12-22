"""
StationManager - COUPLED to TrainStation and Train
"""
from tts.staff import Staff


class StationManager(Staff):
    """StationManager with coupling to TrainStation and Train"""

    def __init__(self, name: str, person_id: str, email: str, phone: str,
                 employee_id: str, salary: float):
        super().__init__(name, person_id, email, phone, employee_id, salary, "Station Management")
        self.managed_station = None
        self.scheduled_trains = []

    def set_managed_station(self, station) -> None:
        self.managed_station = station

    def add_train_schedule(self, train) -> None:
        self.scheduled_trains.append(train)
        print(f"Train {train.get_train_number()} added to schedule")

    def remove_train_schedule(self, train) -> None:
        if train in self.scheduled_trains:
            self.scheduled_trains.remove(train)
            print("Train removed from schedule")

    def get_scheduled_trains(self):
        return self.scheduled_trains

    def perform_duties(self) -> None:
        print("Managing train schedules and station operations")

    def display_info(self):
        print(f"Station Manager: {self.name}")
        print(f"Employee ID: {self.employee_id}")
        print(f"Scheduled Trains: {len(self.scheduled_trains)}")
