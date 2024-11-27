"""
2-Link Manipulator Animation

This project simulates a 2-link robotic manipulator following a predefined path
using inverse kinematics to calculate the required joint angles at each step.
The manipulator consists of two links (L1 and L2), and the path is defined by
the equation y =  mx + b, where x ranges from -90 to 90.

The system is divided into three main components:
1. "Manipulator": This class handles the inverse kinematics calculations,
   determining t    he required joint angles (theta1 and theta2) to move the manipulator
   to the desired position (x, y).

2. "PathGenerator": This class generates the path that the manipulator must follow,
   calculating (x, y) points along the line y = mx + b that lie within the
   reach of the manipulator.

3. "Plotter": This class creates and manages the visual representation of the manipulator's movement.
   It uses "matplotlib" to plot the target path and animate the manipulator's motion
   along that path, updating the position of the manipulator's links and end-effector at each frame.

"""

# Import necessary modules
from manipulator import Manipulator
from path_generator import PathGenerator
from plotter import Plotter


def main() -> None:
    manipulator: Manipulator = Manipulator()
    path_generator: PathGenerator = PathGenerator()
    plotter: Plotter = Plotter(manipulator, path_generator)
    plotter.create_animation()
    plotter.plot_angles()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"Exiting program with error: {e}")
        exit(0)
