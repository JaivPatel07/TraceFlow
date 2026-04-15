# TraceFlow Documentation

TraceFlow is a lightweight Python tool that helps you **see how your code runs step-by-step**.
It shows function calls, variable values, and errors in real time.

---

## 1. Main Tool (`@trace`)

Use `@trace` on any function you want to debug.

### Options

* `show_lines=True` → show each executed line
* `show_locals=True` → show variable values on each line
* `show_args=True` → show function input values

### Example

```python
@trace(show_lines=True, show_locals=True)
def test():
    x = 5
    return x
```

---

## 2. Control Tracing Inside a Function

Sometimes you only need detailed logs for a specific part (like a loop).

### Functions

* `trace_state_start(show_locals=True)` → start detailed tracing
* `trace_state_stop()` → stop detailed tracing

Use this to keep output clean and focus only on important sections.

---

## 3. Manual Control (Advanced)

You can also control tracing without decorators.

### Functions

* `start()` → start tracing
* `stop()` → stop tracing
* `configure(...)` → update settings anytime
* `reset()` → reset indentation level

Important: Always call `stop()` to avoid performance issues.

---

## 4. Example

```python
from traceflow.api import trace, trace_state_start, trace_state_stop

@trace(show_lines=True)
def factorial(n):
    if n <= 1:
        return 1

    trace_state_start(show_locals=True)
    result = n * factorial(n - 1)
    trace_state_stop()

    return result


@trace
def risky():
    return 10 / 0


if __name__ == "__main__":
    factorial(3)

    try:
        risky()
    except ZeroDivisionError:
        pass
```

---

## 5. Understanding Output

### Example

```
▶ factorial(n=3)
  ▶ factorial(n=2)
    ▶ factorial(n=1)
    ◀ factorial() -> 1
  ◀ factorial() -> 2
◀ factorial() -> 6
```

### Meaning

* `▶` → function call
* `◀` → function return
* indentation → shows nested calls
* `(n=3)` → input arguments

---

## 6. Exception Output

```
▶ risky()
✖ risky() ! ZeroDivisionError: division by zero
◀ risky() -> None
```

### Meaning

* `✖` → error occurred
* shows error type and message
* returns `None` because execution stopped

---

## 7. Symbols

| Symbol    | Meaning         |
| --------- | --------------- |
| ▶         | Function call   |
| ◀         | Function return |
| │ line N  | Executed line   |
| var=value | Variable value  |
| ✖         | Exception       |

---

## 8. Smart Output

To keep logs readable:

* Long strings are shortened
* Large lists/dictionaries show only a few items
* Complex objects are simplified

---

## 9. Key Benefits

TraceFlow helps you:

* Understand code flow
* Debug loops and recursion
* Track variable changes
* Detect errors quickly

---

## Version

**Version: 1.0.0**
