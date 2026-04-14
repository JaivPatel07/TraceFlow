"""
Public API for TraceFlow.

Provides the @trace decorator and utility functions to control tracing
granularity at runtime.
"""
import time
from functools import wraps
from .tracer import configure, reset, start, stop

# Prevents redundant start/stop calls during recursive or nested traced functions.
_trace_active_depth = 0

def trace_state_start(show_locals: bool = True) -> None:
    """
    Dynamically enables line-level tracing in the current session.
    Often used to debug specific loops or logic blocks.
    """
    configure(show_line_events=True, show_locals_on_line=show_locals)

def trace_state_stop() -> None:
    """Disables line-level tracing, returning to function-level overview."""
    configure(show_line_events=False, show_locals_on_line=False)

def trace(
    func=None,
    *,
    show_lines: bool = False,
    show_locals: bool = False,
    show_args: bool = True,
):
    """
    Decorator to monitor function execution.

    Args:
        show_lines (bool): If True, prints every executed line.
        show_locals (bool): If True, prints local variables for each line.
        show_args (bool): If True, prints input arguments on function entry.
    """

    def decorator(target_func):
        @wraps(target_func)
        def wrapper(*args, **kwargs):
            global _trace_active_depth

            if _trace_active_depth > 0:
                return target_func(*args, **kwargs)

            reset()
            configure(
                show_line_events=show_lines,
                show_locals_on_line=show_locals,
                include_args=show_args,
            )

            print(f"\n=== TraceFlow: {target_func.__name__} ===")

            start_time = time.perf_counter()
            _trace_active_depth += 1
            start()

            result = None
            try:
                result = target_func(*args, **kwargs)
            finally:
                stop()
                _trace_active_depth -= 1

            end_time = time.perf_counter()

            print(f"result: {result}")
            print(f"time: {end_time - start_time:.6f}s")
            print("=== End TraceFlow ===\n")

            return result

        return wrapper

    if func is None:
        # Supports both @trace and @trace(...)
        return decorator
    return decorator(func)