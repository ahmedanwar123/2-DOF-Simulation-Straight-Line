import math
import matplotlib.pyplot as plt
import constants as c
from matplotlib.animation import FuncAnimation
from manipulator import Manipulator
from path_generator import PathGenerator
from typing import List, Tuple


class Plotter:
    def __init__(self, manipulator: Manipulator, path_generator: PathGenerator) -> None:
        self.manipulator: Manipulator = manipulator
        self.path_generator: PathGenerator = path_generator
        self.path_points: List[Tuple[float, float]] = (
            self.path_generator.generate_path()
        )

        # Setup plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-50, 150)
        self.ax.set_title("2-Link Manipulator Tracking a Straight Line")
        self.ax.set_xlabel("X (mm)")
        self.ax.set_ylabel("Y (mm)")

        # Draw the full target line for reference
        line_x: List[float] = [-90, 90]
        line_y: List[float] = [c.LINE_EQN(x) for x in line_x]
        self.ax.plot(
            line_x, line_y, "r--", label=f"Target Line (y = {c.LINE_EQN_LABEL})"
        )
        self.ax.legend()

        # Link lines and end-effector point
        (self.link1_line,) = self.ax.plot(
            [], [], "o-", lw=4, color="blue", label="Link 1"
        )
        (self.link2_line,) = self.ax.plot(
            [], [], "o-", lw=4, color="green", label="Link 2"
        )
        (self.end_effector,) = self.ax.plot([], [], "ro", label="End Effector")

    def init(self) -> Tuple:
        self.link1_line.set_data([], [])
        self.link2_line.set_data([], [])
        self.end_effector.set_data([], [])
        return self.link1_line, self.link2_line, self.end_effector

    def update(self, frame: int) -> Tuple:
        # Looping through path points
        x, y = self.path_points[frame % len(self.path_points)]

        # Compute inverse kinematics
        theta1, theta2 = self.manipulator.inverse_kinematics(x, y)
        if theta1 is None or theta2 is None:
            return (
                self.link1_line,
                self.link2_line,
                self.end_effector,
            )  # Skip if point is out of reach

        # Calculate link positions
        x1: float = self.manipulator.L1 * math.cos(theta1)
        y1: float = self.manipulator.L1 * math.sin(theta1)
        x2: float = x1 + self.manipulator.L2 * math.cos(theta1 + theta2)
        y2: float = y1 + self.manipulator.L2 * math.sin(theta1 + theta2)

        # Update link lines and end-effector position
        self.link1_line.set_data([0, x1], [0, y1])
        self.link2_line.set_data([x1, x2], [y1, y2])
        self.end_effector.set_data(x2, y2)

        return self.link1_line, self.link2_line, self.end_effector

    def create_animation(self) -> None:
        ani = FuncAnimation(  # noqa: F841
            self.fig,
            self.update,
            frames=len(self.path_points) * 2,  # Repeat the path points
            init_func=self.init,
            blit=True,
            interval=100,
            repeat=True,  # Loop the animation continuously
        )
        plt.show()
