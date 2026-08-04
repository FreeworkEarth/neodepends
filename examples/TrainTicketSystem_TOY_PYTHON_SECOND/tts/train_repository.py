"""
NEW CLASS: Repository pattern
Manages Train entities separately
"""
from typing import Dict, List, Optional
from tts.train import Train

# Failure-mode fixture R4 (conditional import): both branches create a real
# runtime dependency, but static analysis may capture only one or neither.
# NeoDepends should capture the import to tts.route regardless of which
# branch executes.
try:
    from tts.route import Route as _Route
except ImportError:
    _Route = None  # type: ignore[assignment,misc]


class TrainRepository:
    """Repository for Train entities"""

    def __init__(self):
        self.trains: Dict[str, Train] = {}

    def add_train(self, train: Train):
        """Add a train to the repository"""
        self.trains[train.train_id] = train

    def get_train(self, train_id: str) -> Optional[Train]:
        """Get train by ID"""
        return self.trains.get(train_id)

    def get_all_trains(self) -> List[Train]:
        """Get all trains"""
        return list(self.trains.values())

    def get_trains_by_route(self, route_id: str) -> List[Train]:
        """Get trains for a specific route"""
        result = []
        for train in self.trains.values():
            if train.route_id == route_id:
                result.append(train)
        return result
