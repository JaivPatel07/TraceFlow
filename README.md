# TraceFlow

TraceFlow is a lightweight Python tracing tool that helps you understand how your code runs.

It provides clear visibility into:

* Function calls
* Input arguments
* Return values
* Optional line-by-line execution
* Optional variable values (locals)
* Exceptions
* Execution time

---

## Demo

![TraceFlow Demo](demo.gif)

---

## Installation

No installation required.

* Python 3.8+
* No external dependencies

Clone or download the repository and run directly.

---

## Quick Start

```python
from traceflow.api import trace

@trace
def add(a, b):
    return a + b

add(2, 3)
```

Output:

```
▶ add(a=2, b=3)
◀ add() -> 5
```

---

## Core Usage

### Basic

```python
@trace
def func():
    ...
```

### With Options

```python
@trace(show_lines=True, show_locals=True)
def func():
    ...
```

### Options

| Option      | Default | Description                   |
| ----------- | ------- | ----------------------------- |
| show_lines  | False   | Show each executed line       |
| show_locals | False   | Show variable values per line |
| show_args   | True    | Show function arguments       |

---

## Focused Debugging

Enable detailed tracing only where needed to avoid noisy output.

```python
from traceflow.api import trace, trace_state_start, trace_state_stop

@trace
def process(items):
    result = []

    trace_state_start(show_locals=True)
    for i in items:
        result.append(i * 2)
    trace_state_stop()

    return result
```

---

## Output Format

| Symbol   | Meaning         |
| -------- | --------------- |
| ▶        | Function call   |
| ◀        | Function return |
| │ line N | Line execution  |
| ✖        | Exception       |

Example:

```
▶ factorial(n=3)
  ▶ factorial(n=2)
    ▶ factorial(n=1)
    ◀ factorial() -> 1
  ◀ factorial() -> 2
◀ factorial() -> 6
```

---

## Exception Example

```
▶ risky()
✖ risky() ! ZeroDivisionError: division by zero
◀ risky() -> None
```

---

## Project Structure

```
TraceFlow/
│
├── main.py
└── traceflow/
    ├── api.py
    └── tracer.py
```

---

## How It Works

* Uses Python’s built-in `sys.settrace`
* Tracks function calls, line execution, returns, and exceptions
* Formats output to remain readable and concise

---

## Smart Output

To keep logs readable:

* Long strings are shortened
* Large lists and dictionaries are truncated
* Complex objects are simplified

---

## Tips

* Use `@trace` for a clean overview
* Enable detailed tracing only where necessary
* Avoid full line tracing across large code blocks

---

## License

MIT License
