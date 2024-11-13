import math
import constants as c
from typing import Optional, Tuple


class Manipulator:
    def __init__(self, l1: float = c.L1, l2: float = c.L2) -> None:
        self.L1: float = l1  # Length of link 1
        self.L2: float = l2  # Length of link 2
        self.MAX_REACH: float = self.L1 + self.L2

    def inverse_kinematics(
        self, x: float, y: float
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Calculate the inverse kinematics for a 2-link manipulator.
        Returns the joint angles (theta1, theta2) or None if out of reach.
        """
        d: float = math.sqrt(x**2 + y**2)
        if d > self.MAX_REACH or d < abs(self.L1 - self.L2):
            return None, None  # Out of reach

        cos_theta2: float = (d**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        sin_theta2: float = math.sqrt(1 - cos_theta2**2)
        theta2: float = math.atan2(sin_theta2, cos_theta2)

        theta1: float = math.atan2(y, x) - math.atan2(
            self.L2 * sin_theta2, self.L1 + self.L2 * cos_theta2
        )
        return theta1, theta2
