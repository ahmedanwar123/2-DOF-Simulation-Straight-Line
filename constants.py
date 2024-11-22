import inspect

# Constants
L1: float = 50  # Link 1 length in mm
L2: float = 40  # Link 2 length in mm
STEP_SIZE: float = 2  # Step size in mm
MAX_REACH: int = L1 + L2  # Maximum reach in mm


def LINE_EQN(x: float) -> float:
    return -x / 2 + 10


LINE_EQN_SOURCE: str = inspect.getsource(LINE_EQN).strip().split("return")[-1].strip()

# Convert the expression to LaTeX format
LINE_EQN_LABEL: str = (
    f"${LINE_EQN_SOURCE.replace('/', ' / ').replace('+', ' + ').replace('-', ' - ')}$"
)
