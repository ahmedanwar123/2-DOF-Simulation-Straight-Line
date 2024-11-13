import inspect

# Constants for the manipulator
L1: float = 50  # Length of link 1 in mm
L2: float = 40  # Length of link 2 in mm
STEP_SIZE: float = 2  # Step size along the line in mm
MAX_REACH: int = L1 + L2  # Maximum reach of the manipulator in mm


def LINE_EQN(x: float) -> float:
    return -x / 2 + 10


# Retrieve the function's source code as a string
LINE_EQN_SOURCE: str = inspect.getsource(LINE_EQN).strip().split("return")[-1].strip()

# Convert the expression to LaTeX format
LINE_EQN_LABEL: str = (
    f"${LINE_EQN_SOURCE.replace('/', ' / ').replace('+', ' + ').replace('-', ' - ')}$"
)
