"""
Example demonstration of TraceFlow using a backtracking algorithm.
"""
from traceflow.api import trace

@trace(show_lines=False)
def generate_combinations(values):
    """Builds all possible subsets of the given values."""
    result = []
    path = []

    def backtrack(start_index):
        result.append(path[:])

        for index in range(start_index, len(values)):
            path.append(values[index])
            backtrack(index + 1)
            path.pop()

    backtrack(0)
    return result

if __name__ == "__main__":
    numbers = [1, 2, 3]
    combinations = generate_combinations(numbers)
    print("combinations:", combinations)
