from dataclasses import dataclass
from device import Device
from queue import Queue


@dataclass
class Configuration:
    mu1: float
    mu2: float
    t: float
    lambd: float
    queue: Queue = Queue()
    device: Device = Device()

    def initialize(self, mu1, mu2, t, lambd):
        self.mu1 = mu1
        self.mu2 = mu2
        self.t = t
        self.lambd = lambd
        self.device = Device()

        return self
