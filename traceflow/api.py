import time
from functools import wraps
from .tracer import start, stop, reset, configure


class Colors:
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"


_active_depth = 0


def trace_state_start(show_locals=True):
    configure(show_lines=True, show_locals=show_locals)


def trace_state_stop():
    configure(show_lines=False, show_locals=False)


def _color(text, color, use_colors):
    if not use_colors:
        return text
    return f"{color}{text}{Colors.RESET}"


def trace(
    func=None,
    *,
    show_lines=False,
    show_locals=False,
    show_args=True,
    use_colors=True,
):
    def decorator(target_func):
        @wraps(target_func)
        def wrapper(*args, **kwargs):
            global _active_depth

            if _active_depth > 0:
                return target_func(*args, **kwargs)

            reset()
            configure(
                show_lines=show_lines,
                show_locals=show_locals,
                show_args=show_args,
                use_colors=use_colors,
            )

            print(_color(f"\n=== TraceFlow: {target_func.__name__} ===", Colors.CYAN, use_colors))

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

            print(_color("result:", Colors.GREEN, use_colors), result)
            print(_color("time:", Colors.YELLOW, use_colors), f"{end_time - start_time:.6f}s")
            print(_color("=== End TraceFlow ===\n", Colors.CYAN, use_colors))

            return result

        return wrapper

    return decorator if func is None else decorator(func)