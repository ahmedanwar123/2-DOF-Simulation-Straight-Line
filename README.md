# Robotics Mid-Term Project


# 2-Link Manipulator Animation

This project simulates a 2-link robotic manipulator following a predefined path using inverse kinematics. The manipulator is visualized using `matplotlib` and is controlled to follow a straight line path. The main components of this project include the manipulator (with inverse kinematics calculations), the path generator, and the plotter.

## Project Structure

- **`constants.py`**: Defines constants for link lengths, step size, and the line equation.
- **`path_generator.py`**: Contains the `PathGenerator` class, which generates reachable points along a specified line.
- **`manipulator.py`**: Contains the `Manipulator` class, which calculates the inverse kinematics for reaching target points.
- **`plotter.py`**: Contains the `Plotter` class, which visualizes the manipulator's movement along the path and plots the joint angles over time.
- **`main.py`**: Initializes and executes the main components of the project, displaying the manipulator's animation and saving the angle plots.

## Setup and Usage

1. Install required dependencies:
   ```bash
   pip install matplotlib
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

   This will display an animation of the manipulator following the target path and save the joint angle plots in the `angle_plots` folder.

## Components

**Note : All units are in mm**

### 1. Path Generator
The `PathGenerator` class generates path points along a target line, defined as `y = -x / 2 + 100`. The points are spaced by `STEP_SIZE` and limited by the manipulator's maximum reach.

### 2. Manipulator
The `Manipulator` class uses inverse kinematics to compute the joint angles (`theta1`, `theta2`) needed to reach a target `(x, y)`.

#### Inverse Kinematics Calculation
Given a target point `(x, y)`, the joint angles are computed as follows:

1. **Calculate the Distance `d`**:
   - `d` is the distance from the base to the target:
     - `d = sqrt(x^2 + y^2)`
   - Ensure `d` is within reach: `d` must satisfy `|L1 - L2| <= d <= L1 + L2`.

2. **Compute `theta2` (Elbow Angle)**:
   - Using the law of cosines:
     - `cos(theta2) = (d^2 - L1^2 - L2^2) / (2 * L1 * L2)`
   - Then:
     - `theta2 = atan2(sqrt(1 - cos(theta2)^2), cos(theta2))`

3. **Compute `theta1` (Shoulder Angle)**:
   - First, calculate the angle `alpha` to `(x, y)`:
     - `alpha = atan2(y, x)`
   - Then adjust by the angle `beta`:
     - `beta = atan2(L2 * sin(theta2), L1 + L2 * cos(theta2))`
   - Finally:
     - `theta1 = alpha - beta`

4. **Return Angles**:
   - The calculated `theta1` and `theta2` represent the joint angles needed to reach `(x, y)`.

### 3. Plotter
The `Plotter` class animates the manipulator’s movement along the target path and plots the joint angles over time. It creates and displays the animation, saving angle plots in the `angle_plots` directory.

## Example Output

Running `main.py` displays an animation of the manipulator following the line path and saves shoulder and elbow angle plots as PNG files.

## Dependencies
- Python 3
- `matplotlib` for plotting and animation
