"""
Public API for TraceFlow
"""
import time
from functools import wraps
from .tracer import start, stop, reset, configure


# Prevent multiple nested trace sessions
_active_depth = 0


def trace_state_start(show_locals=True):
    configure(show_lines=True, show_locals=show_locals)


def trace_state_stop():
    configure(show_lines=False, show_locals=False)


def trace(func=None, *, show_lines=False, show_locals=False, show_args=True):
    """
    Decorator to trace function execution.
    Supports both:
        @trace
        @trace(...)
    """

    def decorator(target_func):
        @wraps(target_func)
        def wrapper(*args, **kwargs):
            global _active_depth

            # Skip if already tracing (nested call)
            if _active_depth > 0:
                return target_func(*args, **kwargs)

            reset()
            configure(
                show_lines=show_lines,
                show_locals=show_locals,
                show_args=show_args,
            )

            print(f"\n=== TraceFlow: {target_func.__name__} ===")

            start_time = time.perf_counter()
            _active_depth += 1
            start()

            result = None
            try:
                result = target_func(*args, **kwargs)
            finally:
                stop()
                _active_depth -= 1

            end_time = time.perf_counter()

            # Summary
            print(f"result: {result}")
            print(f"time: {end_time - start_time:.6f}s")
            print("=== End TraceFlow ===\n")

            return result

        return wrapper
    return decorator if func is None else decorator(func)