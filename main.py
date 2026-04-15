"""
TraceFlow demo using recursion and exception handling.
"""

from traceflow import trace, trace_state_start, trace_state_stop


@trace(show_lines=True)
def generate_combinations(values):
    """Generate all subsets using backtracking."""
    result = []
    path = []

    def backtrack(start):
        result.append(path[:])

        # Enable detailed tracing only inside loop
        trace_state_start(show_locals=True)

        for i in range(start, len(values)):
            path.append(values[i])
            backtrack(i + 1)
            path.pop()

        trace_state_stop()

    backtrack(0)
    return result


@trace
def demonstrate_exception():
    """Show how exceptions are traced."""
    print("Running risky operation...")
    return 10 / 0  # intentional error


if __name__ == "__main__":
    values = [1, 2, 3]

    generate_combinations(values)

    try:
        demonstrate_exception()
    except ZeroDivisionError:
        pass