import math
import constants as c
from typing import List, Tuple


class PathGenerator:
    def __init__(
        self, step_size: float = c.STEP_SIZE, l1: float = c.L1, l2: float = c.L2
    ) -> None:
        self.STEP_SIZE: float = step_size
        self.L1: float = l1
        self.L2: float = l2
        self.MAX_REACH: float = self.L1 + self.L2

    def generate_path(self) -> List[Tuple[float, float]]:
        """
        Generate points along the line y = mx + b that are within reach of the manipulator.
        Returns a list of (x, y) points.
        """
        path_points: List[Tuple[float, float]] = []
        x: float = -180
        while x <= 180:
            y: float = c.LINE_EQN(x)  # y-intercept in cm
            if math.sqrt(x**2 + y**2) <= self.MAX_REACH:  # Ensure it's not out of reach
                path_points.append((x, y))
            x += self.STEP_SIZE
        return path_points
