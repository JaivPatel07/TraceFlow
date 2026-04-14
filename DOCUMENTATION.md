# TraceFlow Technical Documentation

TraceFlow is a lightweight, zero-dependency Python tracing library designed to provide high-visibility debugging. It leverages `sys.settrace` to monitor function calls, variable mutations, and exceptions in real-time.

---

## 1. Public API Reference (`api.py`)

These are the primary tools used by developers to instrument their code.

### `@trace` (Decorator)
The main entry point for tracing. It wraps a function to initialize the trace engine, capture execution data, and print a summary.

*   **Parameters**:
    *   `show_lines` (bool): Enables printing of every line executed within the function.
    *   `show_locals` (bool): If line tracing is on, this prints the state of local variables on each line.
    *   `show_args` (bool): Prints the values of arguments passed into the function upon entry.

### `trace_state_start(show_locals=True)`
Dynamically increases the verbosity of a running trace. Use this inside a function to "zoom in" on a specific block of code (like a complex loop) without flooding the output for the entire function.

### `trace_state_stop()`
Resets the trace verbosity to the levels defined in the `@trace` decorator. Use this to "zoom out" after a sensitive block of code has finished.

---

## 2. Internal Engine Reference (`tracer.py`)

The `TraceEngine` class manages the state and formatting of the trace session.

### Core Methods

| Method | Description |
| :--- | :--- |
| `tracer(frame, event, arg)` | The primary callback for `sys.settrace`. It dispatches events to specific handlers. |
| `configure(...)` | Updates engine flags (lines, locals, args) at runtime. |
| `reset()` | Clears the `call_depth` to ensure indentation starts fresh. |
| `_print_call(frame)` | Formats the function entry. Increments indentation. Uses `▶`. |
| `_print_line(frame)` | Formats line execution. Retrieves line numbers and local variables. Uses `│`. |
| `_print_return(frame, res)`| Formats function exit. Decrements indentation and shows return value. Uses `◀`. |
| `_print_exception(frame, arg)`| Formats unhandled exceptions. Captures type and message. Uses `✖`. |
| `_short(value)` | Uses `reprlib` to truncate long strings, lists, or dicts to keep output readable. |
| `_should_trace_frame(frame)`| Security filter. Prevents TraceFlow from tracing its own internal logic or synthetic Python frames. |

---

## 3. Comprehensive Usage Example

This example utilizes every method in the API to demonstrate a full lifecycle, including recursion, dynamic state switching, and exception handling.

```python
from traceflow.api import trace, trace_state_start, trace_state_stop

@trace(show_lines=True, show_locals=False)
def calculate_factorial(n):
    if n <= 1:
        return 1
    
    # We want to see local variables only during the multiplication step
    trace_state_start(show_locals=True)
    result = n * calculate_factorial(n - 1)
    trace_state_stop()
    
    return result

@trace
def risky_business():
    return 10 / 0

if __name__ == "__main__":
    calculate_factorial(3)
    try:
        risky_business()
    except ZeroDivisionError:
        pass
```

---

## 4. Full Output Explained

Based on the example above, here is what the console output looks like and what each part signifies.

### Function Execution Output
```text
=== TraceFlow: calculate_factorial ===
▶ calculate_factorial(n=3)
  │ line 5: if n <= 1:
  │ line 9: trace_state_start(show_locals=True)
  │ line 10: result = n * calculate_factorial(n - 1)
    ▶ calculate_factorial(n=2)
      │ line 5: if n <= 1:
      │ line 9: trace_state_start(show_locals=True)
      │ line 10: result = n * calculate_factorial(n - 1)
        ▶ calculate_factorial(n=1)
        ◀ calculate_factorial() -> 1
      │ line 10: result = n * calculate_factorial(n - 1) | n=2, result=2
      │ line 11: trace_state_stop()
      │ line 13: return result
    ◀ calculate_factorial() -> 2
  │ line 10: result = n * calculate_factorial(n - 1) | n=3, result=6
  │ line 11: trace_state_stop()
  │ line 13: return result
◀ calculate_factorial() -> 6
result: 6
time: 0.000452s
=== End TraceFlow ===
```

**Key Takeaways from Output:**
1.  **Indentation**: Notice how the `▶` and `│` symbols move to the right as the recursion gets deeper.
2.  **Arguments**: `(n=3)` is shown because `show_args` is true by default.
3.  **Local Variables**: Even though the decorator had `show_locals=False`, the variables `n=2, result=2` appeared on line 10 because `trace_state_start` was called.
4.  **Return Values**: `◀` clearly shows the unwinding of the stack.

### Exception Output
```text
=== TraceFlow: risky_business ===
▶ risky_business()
✖ risky_business() ! ZeroDivisionError: division by zero
◀ risky_business() -> None
result: None
time: 0.000120s
=== End TraceFlow ===
```
**Key Takeaways from Exception:**
1.  **The Symbol**: `✖` indicates exactly where the crash happened.
2.  **The Message**: It captures the specific error type (`ZeroDivisionError`) and the Python error message.
3.  **Graceful Exit**: The trace still prints the `time` and `result` (which is `None` because the function didn't finish).

---

## 5. Technical Symbols Summary

| Symbol | Meaning |
| :--- | :--- |
| `▶` | **Function Entry**: The start of a call. |
| `◀` | **Function Exit**: Returning a value to the caller. |
| `│ line N` | **Execution Step**: The specific line number in the source file. |
| `| var=val` | **Local State**: The current value of variables on that line. |
| `✖` | **Exception**: An error was raised during execution. |

---

## 6. Formatting & Truncation

To prevent the logs from becoming unreadable when dealing with large data, TraceFlow automatically truncates output:
- **Strings**: Max 50 characters.
- **Lists/Dicts/Tuples**: Max 6 items.
- **Nested Objects**: Represented by their type name if they don't have a clean string representation.

*Documentation Version: 1.0.0*
