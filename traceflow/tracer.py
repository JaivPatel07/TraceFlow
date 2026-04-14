"""
Core engine logic. Handles the sys.settrace hooks and output formatting.
"""
import inspect
import os
import reprlib
import sys
from typing import Any


class TraceEngine:
    def __init__(self):
        self.depth = 0
        self.lines = False
        self.locals = False
        self.args = True

        # Grab the package dir so we don't trace ourselves
        self._pkg_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

        # Sensible defaults for truncating large data
        self._repr = reprlib.Repr()
        self._repr.maxstring = 60
        self._repr.maxlist = self._repr.maxtuple = self._repr.maxdict = 6

    def configure(self, show_line_events=None, show_locals_on_line=None, include_args=None):
        if show_line_events is not None:
            self.lines = bool(show_line_events)
        if show_locals_on_line is not None:
            self.locals = bool(show_locals_on_line)
        if include_args is not None:
            self.args = bool(include_args)

    def reset(self):
        self.depth = 0

    def tracer(self, frame, event, arg):
        if event == "call":
            if not self._is_user_code(frame):
                return None
            self._print_call(frame)
        elif event == "line":
            if self.lines:
                self._print_line(frame)
        elif event == "exception":
            self._print_exception(frame, arg)
        elif event == "return":
            self._print_return(frame, arg)
        return self.tracer

    def _print_call(self, frame):
        indent = "  " * self.depth
        args_text = "()"

        if self.args:
            # inspect.getargvalues is a bit legacy but works fine here
            names, _, _, _ = inspect.getargvalues(frame)
            if names:
                items = [f"{n}={self._fmt(frame.f_locals[n])}" for n in names]
                args_text = f"({', '.join(items)})"

        print(f"{indent}▶ {frame.f_code.co_name}{args_text}")
        self.depth += 1

    def _print_line(self, frame):
        indent = "  " * self.depth
        msg = f"{indent}│ line {frame.f_lineno}"

        if self.locals:
            # filter out noisy internals and functions
            items = [f"{k}={self._fmt(v)}" for k, v in frame.f_locals.items() 
                     if not (k.startswith("__") or callable(v))]
            if items:
                msg += f" | {', '.join(items)}"
        print(msg)

    def _print_exception(self, frame, arg):
        indent = "  " * max(0, self.depth - 1)
        etype, evalue, _ = arg
        print(f"{indent}✖ {frame.f_code.co_name}() [line {frame.f_lineno}] ! {etype.__name__}: {evalue}")

    def _print_return(self, frame, result):
        self.depth = max(0, self.depth - 1)
        print(f"{'  ' * self.depth}◀ {frame.f_code.co_name}() -> {self._fmt(result)}")

    def _fmt(self, val):
        try:
            return self._repr.repr(val)
        except Exception:
            return f"<{type(val).__name__}>"

    def _is_user_code(self, frame):
        path = os.path.abspath(frame.f_code.co_filename).replace("\\", "/")
        # Ignore synthetic stuff like <listcomp>
        if frame.f_code.co_name.startswith("<"):
            return False
        return not path.startswith(self._pkg_dir)


_engine = TraceEngine()

def start(): sys.settrace(_engine.tracer)
def stop(): sys.settrace(None)
def reset(): _engine.reset()
def configure(**kw): _engine.configure(**kw)
