"""
Core tracing engine for TraceFlow.

This module defines the TraceEngine class, which interacts with Python's 
sys.settrace mechanism to monitor function calls, line execution, 
returns, and exceptions.
"""
import inspect
import os
import reprlib
import sys
from typing import Any


class TraceEngine:
    """
    The central logic handler for capturing and formatting trace events.
    
    Attributes:
        call_depth (int): Current nesting level of function calls, used for indentation.
        show_line_events (bool): Whether to print details for every line executed.
        show_locals_on_line (bool): Whether to include local variables in line output.
        include_args (bool): Whether to print function arguments on entry.
    """

    def __init__(self):
        """Initializes the engine with default settings and a configured Repr instance."""
        self.call_depth = 0
        self.show_line_events = False
        self.show_locals_on_line = False
        self.include_args = True

        # Internal folder path so we can skip TraceFlow's own files.
        self._traceflow_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

        self._repr = reprlib.Repr()
        self._repr.maxstring = 50
        self._repr.maxother = 50
        self._repr.maxlist = 6
        self._repr.maxtuple = 6
        self._repr.maxdict = 6
        self._repr.maxset = 6

    def configure(self, show_line_events=None, show_locals_on_line=None, include_args=None):
        """
        Updates the engine configuration flags at runtime.

        Args:
            show_line_events (bool, optional): Enable/disable line-level tracing.
            show_locals_on_line (bool, optional): Enable/disable local variable inspection.
            include_args (bool, optional): Enable/disable argument printing on function calls.
        """
        if show_line_events is not None:
            self.show_line_events = bool(show_line_events)
        if show_locals_on_line is not None:
            self.show_locals_on_line = bool(show_locals_on_line)
        if include_args is not None:
            self.include_args = bool(include_args)

    def reset(self):
        """Resets the call depth counter before a new top-level trace session."""
        self.call_depth = 0

    def tracer(self, frame, event, arg):
        """
        The primary callback function passed to sys.settrace.

        This method dispatches execution events (call, line, return, exception)
        to their respective handler methods.

        Args:
            frame: The current stack frame object.
            event (str): The type of event ('call', 'line', 'return', 'exception').
            arg: Event-specific data (e.g., return value or exception tuple).

        Returns:
            method: A reference to this tracer method to continue tracing the frame.
        """
        if event == "call":
            if not self._should_trace_frame(frame):
                return None
            self._print_call(frame)
        elif event == "line":
            if self.show_line_events:
                self._print_line(frame)
        elif event == "exception":
            self._print_exception(frame, arg)
        elif event == "return":
            self._print_return(frame, arg)

        return self.tracer

    def _print_call(self, frame):
        """
        Handles the 'call' event. Prints the function name and arguments.

        Args:
            frame: The frame being entered.
        """
        indent = "  " * self.call_depth
        func_name = frame.f_code.co_name
        args_text = "()"
        if self.include_args:
            args_info = self._get_args(frame)
            if args_info:
                args_text = f"({self._format_mapping(args_info)})"

        print(f"{indent}▶ {func_name}{args_text}")

        self.call_depth += 1

    def _print_line(self, frame):
        """
        Handles the 'line' event. Prints line numbers and filtered local variables.

        Args:
            frame: The current execution frame.
        """
        indent = "  " * self.call_depth
        lineno = frame.f_lineno
        msg = f"{indent}│ line {lineno}"

        if self.show_locals_on_line:
            locals_clean = {
                k: v for k, v in frame.f_locals.items() 
                if not k.startswith("__") and not callable(v)
            }
            if locals_clean:
                msg += f" | {self._format_mapping(locals_clean)}"
        
        print(msg)

    def _print_exception(self, frame, arg):
        """
        Handles the 'exception' event.

        Args:
            frame: The frame where the exception occurred.
            arg: A tuple of (exception_type, value, traceback).
        """
        indent = "  " * max(0, self.call_depth - 1)
        exc_type, exc_value, _ = arg
        func_name = frame.f_code.co_name
        print(f"{indent}✖ {func_name}() ! {exc_type.__name__}: {exc_value}")

    def _print_return(self, frame, result):
        """
        Handles the 'return' event. Decrements call depth and prints the return value.

        Args:
            frame: The frame being exited.
            result: The value being returned.
        """
        self.call_depth = max(0, self.call_depth - 1)
        indent = "  " * self.call_depth
        func_name = frame.f_code.co_name
        print(f"{indent}◀ {func_name}() -> {self._short(result)}")

    def _get_args(self, frame):
        """
        Extracts argument names and values from a frame.

        Args:
            frame: The stack frame to inspect.

        Returns:
            dict: A mapping of argument names to their values.
        """
        args, _, _, values = inspect.getargvalues(frame)
        return {a: values[a] for a in args}

    def _format_mapping(self, mapping):
        """
        Formats a dictionary of variables into a readable string.

        Args:
            mapping (dict): The variables to format.

        Returns:
            str: A comma-separated string of key=value pairs.
        """
        return ", ".join(f"{key}={self._short(value)}" for key, value in mapping.items())

    def _short(self, value):
        """
        Truncates values for clean output using reprlib.

        Args:
            value: The object to represent.

        Returns:
            str: A string representation of the value.
        """
        try:
            return self._repr.repr(value)
        except Exception:
            return f"<{type(value).__name__}>"

    def _should_trace_frame(self, frame):
        """
        Filters frames to avoid tracing internal TraceFlow logic or synthetic frames.

        Args:
            frame: The frame to check.

        Returns:
            bool: True if the frame should be traced, False otherwise.
        """
        filename = os.path.abspath(frame.f_code.co_filename).replace("\\", "/")

        # Skip synthetic frames like <listcomp>, <lambda>, <dictcomp>.
        if frame.f_code.co_name.startswith("<"):
            return False

        return not filename.startswith(self._traceflow_dir)


# Global shared instance and bridge functions
_engine = TraceEngine()

def start() -> None:
    """Activates the global tracer using sys.settrace."""
    sys.settrace(_engine.tracer)

def stop() -> None:
    """Deactivates the global tracer by setting the trace function to None."""
    sys.settrace(None)

def reset() -> None:
    """Resets the internal state (like call depth) of the shared engine."""
    _engine.reset()

def configure(**kwargs: Any) -> None:
    """Configures the shared engine with specific tracing options."""
    _engine.configure(**kwargs)
