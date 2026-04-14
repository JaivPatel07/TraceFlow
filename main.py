"""
Example demonstration of TraceFlow using a backtracking algorithm.
"""
from traceflow.api import trace, trace_state_start, trace_state_stop

@trace(show_lines=True, show_locals=False)
def generate_combinations(values):
    """Builds all possible subsets of the given values."""
    result = []
    path = []

    def backtrack(start_index):
        result.append(path[:])
        trace_state_start(show_locals=True)
        for index in range(start_index, len(values)):
            path.append(values[index])
            backtrack(index + 1)
            path.pop()
        trace_state_stop()

    backtrack(0)
    return result

@trace
def demonstrate_exception(should_fail=True):
    """Demonstrates how TraceFlow captures exceptions."""
    print("About to do something risky...")
    if should_fail:
        return 10 / 0 # This will trigger the 'exception' event
    return "Safe!"

if __name__ == "__main__":
    numbers = [1, 2, 3]
    combinations = generate_combinations(numbers)
    try:
        demonstrate_exception()
    except ZeroDivisionError:
        pass
