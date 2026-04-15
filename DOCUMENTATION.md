# TraceFlow Documentation (Simple)

TraceFlow is a lightweight Python tool that helps you **see what your code is doing step-by-step**.
It shows function calls, variable values, and errors in real time.

---

## 1. Main Tool (`@trace`)

Use `@trace` on any function you want to debug.

### Options:

* `show_lines=True` → shows each line being executed
* `show_locals=True` → shows variable values on each line
* `show_args=True` → shows function input values

### Example:

```python
@trace(show_lines=True, show_locals=True)
def test():
    x = 5
    return x
```

---

## 2. Control Tracing Inside Function

Sometimes you don’t want logs for the whole function, only for a specific part (like a loop).

### Functions:

* `trace_state_start(show_locals=True)` → start detailed tracing
* `trace_state_stop()` → stop detailed tracing

👉 Use this when you want to debug only a small section.

---

## 3. Manual Control (Advanced)

If you don’t want to use decorators, you can control tracing manually.

### Functions:

* `start()` → start tracing
* `stop()` → stop tracing
* `configure(...)` → change settings anytime
* `reset()` → reset indentation level

⚠️ Important: Always call `stop()` or tracing will continue running and slow your program.

---

## 4. Full Example

```python
from traceflow.api import trace, trace_state_start, trace_state_stop

@trace(show_lines=True)
def factorial(n):
    if n <= 1:
        return 1

    # Enable detailed tracing only here
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

### Example Output:

```text
▶ factorial(n=3)
  ▶ factorial(n=2)
    ▶ factorial(n=1)
    ◀ factorial() -> 1
  ◀ factorial() -> 2
◀ factorial() -> 6
```

### Meaning:

* `▶` → function started
* `◀` → function returned value
* indentation → shows nested calls
* `(n=3)` → input arguments

---

## 6. Exception Output

```text
▶ risky()
✖ risky() ! ZeroDivisionError: division by zero
◀ risky() -> None
```

### Meaning:

* `✖` → error occurred
* shows error type and message
* returns `None` because function crashed

---

## 7. Symbols

| Symbol    | Meaning        |
| --------- | -------------- |
| ▶         | Function start |
| ◀         | Function end   |
| │ line N  | Running line   |
| var=value | Variable value |
| ✖         | Error          |

---

## 8. Smart Output (Auto Shortening)

To keep logs clean and readable:

* Long strings → max 50 characters
* Large lists/dictionaries → only first few items
* Complex objects → show type name

---

## 9. Key Benefits

TraceFlow helps you:

* Understand how functions run
* Debug loops and recursion
* Track variable changes
* Find errors quickly

---

## Version

**Version: 1.0.0**
