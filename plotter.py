import math
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from manipulator import Manipulator
import constants as c
from path_generator import PathGenerator
from typing import List, Tuple


class Plotter:
    def __init__(self, manipulator: Manipulator, path_generator: PathGenerator) -> None:
        self.manipulator: Manipulator = manipulator
        self.path_generator: PathGenerator = path_generator
        self.path_points: List[Tuple[float, float]] = (
            self.path_generator.generate_path()
        )

        # Lists to store an gles values
        self.theta1_values: List[float] = []
        self.theta2_values: List[float] = []

        # Animation plot for manipulator movement
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect("equal")
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-50, 150)
        self.ax.set_title("2-Link Manipulator Tracking a Straight Line")
        self.ax.set_xlabel("X (mm)")
        self.ax.set_ylabel("Y (mm)")

        # Plot the line y = mx + b
        line_x = [-90, 90]
        line_y = [c.LINE_EQN(x) for x in line_x]
        self.ax.plot(
            line_x, line_y, "r--", label=f"Target Line (y = {c.LINE_EQN_LABEL})"
        )
        self.ax.legend()

        # Manipulator links
        (self.link1_line,) = self.ax.plot(
            [], [], "o-", lw=4, color="blue", label="Link 1"
        )
        (self.link2_line,) = self.ax.plot(
            [], [], "o-", lw=4, color="green", label="Link 2"
        )
        (self.end_effector,) = self.ax.plot([], [], "ro", label="End Effector")

    def init(self) -> Tuple[plt.Line2D, plt.Line2D, plt.Line2D]:
        """
        Initialize the lines for the animation.
        Returns a tuple of the line objects.
        """
        self.link1_line.set_data([], [])
        self.link2_line.set_data([], [])
        self.end_effector.set_data([], [])
        return self.link1_line, self.link2_line, self.end_effector

    def update(self, frame: int) -> Tuple[plt.Line2D, plt.Line2D, plt.Line2D]:
        """
        Update the plot for each frame in the animation.
        Returns updated line objects.
        """
        x, y = self.path_points[frame]

        # Compute inverse kinematics
        theta1, theta2 = self.manipulator.inverse_kinematics(x, y)
        if theta1 is None or theta2 is None:
            return self.link1_line, self.link2_line, self.end_effector

        # Store the angles
        self.theta1_values.append(math.degrees(theta1))
        self.theta2_values.append(math.degrees(theta2))

        # Calculate link positions
        x1 = self.manipulator.L1 * math.cos(theta1)
        y1 = self.manipulator.L1 * math.sin(theta1)
        x2 = x1 + self.manipulator.L2 * math.cos(theta1 + theta2)
        y2 = y1 + self.manipulator.L2 * math.sin(theta1 + theta2)

        # Update link positions
        self.link1_line.set_data([0, x1], [0, y1])
        self.link2_line.set_data([x1, x2], [y1, y2])
        self.end_effector.set_data(x2, y2)

        return self.link1_line, self.link2_line, self.end_effector

    def create_animation(self) -> None:
        """
        Create and display the animation of the manipulator moving along the path.
        """
        ani = FuncAnimation(  # noqa: F841
            self.fig,
            self.update,
            frames=len(self.path_points),
            init_func=self.init,
            blit=True,
            interval=100,
            repeat=False,
        )
        plt.show()

    def plot_angles(self) -> None:
        """
        Plot theta1 and theta2 in separate graphs and save each plot with a sequential counter.
        """
        # Create a folder to save the images if it doesn't exist
        save_dir = "angle_plots"
        os.makedirs(save_dir, exist_ok=True)

        # Initialize the counter to the next available file number
        counter = 1

        # Check for existing files and find the next available counter
        existing_files = [
            name for name in os.listdir(save_dir) if name.endswith(".png")
        ]
        if existing_files:
            # Extract the counter from existing files (assuming filenames like "shoulder_angle_plot_1.png")
            existing_counters = [
                int(name.split("_")[-1].split(".")[0]) for name in existing_files
            ]
            # Get the next available counter (the smallest missing number)
            counter = max(existing_counters) + 1

        # Plot theta1 (shoulder angle) and save with a sequential counter
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        ax1.plot(self.theta1_values, color="blue")
        ax1.set_title("Shoulder Angle (theta1)")
        ax1.set_xlabel("Step")
        ax1.set_ylabel("Angle (degrees)")
        ax1.grid(True)
        theta1_filename = os.path.join(save_dir, f"shoulder_angle_plot_{counter}.png")
        plt.savefig(theta1_filename)
        print(f"Shoulder angle plot saved as {theta1_filename}")

        # Plot theta2 (elbow angle) and save with a sequential counter
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.plot(self.theta2_values, color="green")
        ax2.set_title("Elbow Angle (theta2)")
        ax2.set_xlabel("Step")
        ax2.set_ylabel("Angle (degrees)")
        ax2.grid(True)
        theta2_filename = os.path.join(save_dir, f"elbow_angle_plot_{counter}.png")
        plt.savefig(theta2_filename)
        print(f"Elbow angle plot saved as {theta2_filename}")

        # Show the plots
        plt.show()
