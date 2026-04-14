"""
User-facing API. Provides the decorator and manual toggles.
"""
import time
from functools import wraps
from .tracer import configure, reset, start, stop

# Keep track of nested @trace calls so we don't start/stop multiple times
_active_depth = 0

def trace_state_start(show_locals=True):
    configure(show_line_events=True, show_locals_on_line=show_locals)

def trace_state_stop():
    configure(show_line_events=False, show_locals_on_line=False)

def trace(func=None, *, show_lines=False, show_locals=False, show_args=True):
    def decorator(target_func):
        @wraps(target_func)
        def wrapper(*args, **kwargs):
            global _active_depth
            if _active_depth > 0:
                return target_func(*args, **kwargs)

            reset()
            configure(
                show_line_events=show_lines,
                show_locals_on_line=show_locals,
                include_args=show_args,
            )

            print(f"\n=== TraceFlow: {target_func.__name__} ===")

            t0 = time.perf_counter()
            _active_depth += 1
            start()

            result = None
            try:
                result = target_func(*args, **kwargs)
            finally:
                stop()
                _active_depth -= 1

            t1 = time.perf_counter()
            print(f"result: {result}")
            print(f"time: {t1 - t0:.6f}s")
            print("=== End TraceFlow ===\n")

            return result

        return wrapper

    if func is None:
        # Supports both @trace and @trace(...)
        return decorator
    return decorator(func)