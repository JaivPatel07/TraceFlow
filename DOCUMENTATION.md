# TraceFlow Docs

TraceFlow is a lightweight, zero-dependency Python tracing library designed to provide high-visibility debugging. It leverages `sys.settrace` to monitor function calls, variable mutations, and exceptions in real-time.

---

## API Reference (`api.py`)

### `@trace` (Decorator)
The main tool. Stick it on any function you want to watch.

- `show_lines`: Logs every line as it runs.
- `show_locals`: Dumps local variables on every line (use with `show_lines`).
- `show_args`: Logs inputs when function is called.

### `trace_state_start(show_locals=True)`
Turn on detailed line tracing mid-function. Great for isolating loops without flooding the logs for the whole app.

### `trace_state_stop()`
Go back to the default overview mode.

---

## Example

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

## Output Breakdown

```text
=== TraceFlow: calculate_factorial ===
▶ calculate_factorial(n=3)
  │ line 5: if n <= 1:
    ▶ calculate_factorial(n=2)
        ▶ calculate_factorial(n=1)
        ◀ calculate_factorial() -> 1
    ◀ calculate_factorial() -> 2
◀ calculate_factorial() -> 6
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
