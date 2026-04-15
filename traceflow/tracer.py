"""
Core tracing engine using sys.settrace.
Handles function calls, lines, returns, and exceptions.
"""

import inspect
import os
import reprlib
import sys


class TraceEngine:
    def __init__(self):
        self.depth = 0
        self.show_lines = False
        self.show_locals = False
        self.show_args = True

        # Avoid tracing internal library code
        self._pkg_dir = os.path.dirname(os.path.abspath(__file__))

        # Shorten large outputs
        self._repr = reprlib.Repr()
        self._repr.maxstring = 60
        self._repr.maxlist = self._repr.maxtuple = self._repr.maxdict = 6

    def configure(self, show_lines=None, show_locals=None, show_args=None):
        if show_lines is not None:
            self.show_lines = show_lines
        if show_locals is not None:
            self.show_locals = show_locals
        if show_args is not None:
            self.show_args = show_args

    def reset(self):
        self.depth = 0

    def tracer(self, frame, event, arg):
        if event == "call":
            if not self._is_user_code(frame):
                return None
            self._print_call(frame)

        elif event == "line" and self.show_lines:
            self._print_line(frame)

        elif event == "return":
            self._print_return(frame, arg)

        elif event == "exception":
            self._print_exception(frame, arg)

        return self.tracer

    def _print_call(self, frame):
        indent = "  " * self.depth

        args_text = "()"
        if self.show_args:
            names, _, _, _ = inspect.getargvalues(frame)
            if names:
                args_text = "(" + ", ".join(
                    f"{n}={self._fmt(frame.f_locals[n])}" for n in names
                ) + ")"

        print(f"{indent}▶ {frame.f_code.co_name}{args_text}")
        self.depth += 1

    def _print_line(self, frame):
        indent = "  " * self.depth
        msg = f"{indent}│ line {frame.f_lineno}"

        if self.show_locals:
            items = [
                f"{k}={self._fmt(v)}"
                for k, v in frame.f_locals.items()
                if not k.startswith("__") and not callable(v)
            ]
            if items:
                msg += " | " + ", ".join(items)

        print(msg)

    def _print_return(self, frame, result):
        self.depth = max(0, self.depth - 1)
        indent = "  " * self.depth
        print(f"{indent}◀ {frame.f_code.co_name}() -> {self._fmt(result)}")

    def _print_exception(self, frame, arg):
        indent = "  " * max(0, self.depth - 1)
        etype, evalue, _ = arg
        print(f"{indent}✖ {frame.f_code.co_name}() ! {etype.__name__}: {evalue}")

    def _fmt(self, value):
        try:
            return self._repr.repr(value)
        except Exception:
            return f"<{type(value).__name__}>"

    def _is_user_code(self, frame):
        filename = os.path.abspath(frame.f_code.co_filename)

        # Skip internal + synthetic frames
        if frame.f_code.co_name.startswith("<"):
            return False

        return not filename.startswith(self._pkg_dir)


_engine = TraceEngine()


def start():
    sys.settrace(_engine.tracer)


def stop():
    sys.settrace(None)


def reset():
    _engine.reset()


def configure(**kwargs):
    _engine.configure(**kwargs)