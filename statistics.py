from dataclasses import dataclass
from demand import Demand
import numpy as np


@dataclass
class Statistics:
    average_time: float = 0
    average_time_awaiting: float = 0
    leaving_count: int = 0
    requirements_count = np.zeros(1000)

    def update(self, demand: Demand) -> None:
        self.average_time += demand.leaving_time - demand.arrival_time
        self.average_time_awaiting += demand.service_start_time - demand.arrival_time
        self.leaving_count += 1

    def update_requirements_count(self, count: int, time: float) -> None:
        self.requirements_count[count] += time
