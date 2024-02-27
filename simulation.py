from random import expovariate
from clock import Clock
from configuration import Configuration
from demand import Demand
from statistics import Statistics
import math


class Simulation:
    @classmethod
    def run(cls, mu1: float, mu2: float, lambd: float, t: float) -> None:
        times = Clock()
        system = Configuration(mu1, mu2, t, lambd)
        statistics = Statistics()

        cls.loop(times, system, statistics)

    @classmethod
    def loop(cls,
             times: Clock,
             system: Configuration,
             statistics: Statistics) -> None:
        times.update_arrival_time(system.lambd)
        prev: float = 0
        while statistics.leaving_count < 1000:
            times.current = get_time_of_nearest_event(times)
            statistics.update_requirements_count(system.queue.qsize() + 1 if system.device.serves else 0,
                                                 times.current - prev)
            prev = times.current
            if times.current == times.arrival:
                cls.add(times, system)
                continue
            if times.current == times.service_start:
                cls.service(times, system)
                continue
            if times.current == times.leaving:
                cls.remove(times, system, statistics)
                continue
        print()
        print(f"Математическое ожидание длительности пребывания требований в системе обслуживания "
              f"{statistics.average_time / statistics.leaving_count}")
        print(f"Математическое ожидание длительности ожидания требований в очереди системы обслуживания "
              f"{statistics.average_time_awaiting / statistics.leaving_count}")
        n = 0
        for k, _ in enumerate(statistics.requirements_count):
            n += k * (statistics.requirements_count[k] / times.current)
        print(f"Математическое ожидание числа требований в системе обслуживания "
              f"{n}")

    @classmethod
    def add(cls, times: Clock,
            system: Configuration) -> None:
        demand = Demand(times.arrival)
        print("[ARRIVAL]",  "time =", times.current, "id =", demand.id, sep=' ')
        if system.queue.empty() and not system.device.serves:
            times.service_start = times.current
        system.queue.put(demand)
        times.update_arrival_time(system.lambd)

    @classmethod
    def service(cls, times: Clock,
                system: Configuration) -> None:
        mu = system.mu1 if (math.floor(times.current) // math.floor(system.t)) % 2 == 0 else system.mu2
        times.leaving = times.current + expovariate(mu)
        system.device.to_occupy(system.queue.get())
        print("[PROCESSING]", "time =", times.current, "id =", system.device.demand.id, sep=' ')
        system.device.demand.service_start_time = times.current
        times.service_start = float('inf')

    @classmethod
    def remove(cls, times: Clock,
               system: Configuration,
               statistics: Statistics) -> None:
        demand = system.device.get_demand()
        print("[DELETE]", "time =", times.current, "id =", demand.id, sep=' ')
        system.device.to_free()
        demand.set_leaving_time(times.current)
        statistics.update(demand)

        if not system.queue.empty():
            times.service_start = times.current
        times.leaving = float('inf')


def get_time_of_nearest_event(times: Clock) -> float:
    return min(times.arrival, times.service_start, times.leaving)
