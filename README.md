# TraceFlow

TraceFlow is a lightweight Python tracing tool that helps you understand code flow while functions run.

It can show:
- which function is called
- input argument values
- return values
- optional line-by-line execution
- optional local state per line
- exceptions
- total execution time

## What Is Included

Project files:

```text
TraceFlow/
	main.py
	traceflow/
		api.py
		engine.py
		tracer.py
```

### File Responsibilities

- `traceflow/api.py`:
	- Public API for users.
	- Provides `trace` decorator.
	- Provides state-detail flags: `trace_state_start` and `trace_state_stop`.
- `traceflow/engine.py`:
	- Small bridge around `sys.settrace`.
	- Starts/stops tracing and forwards settings to tracer engine.
- `traceflow/tracer.py`:
	- Core trace logic (`TraceEngine`).
	- Handles call, line, return, and exception events.
	- Formats output to keep it readable.
- `main.py`:
	- Example usage (backtracking combinations demo).

## Requirements

- Python 3.8+
- No external dependencies

## Quick Start

Run from project root:

```bash
python main.py
```

## Public API

Import API:

```python
from traceflow.api import trace, trace_state_start, trace_state_stop
```

### 1. `trace`

Decorator to trace a function.

Usage:

```python
@trace
def fn(...):
		...
```

or with options:

```python
@trace(show_lines=True, show_locals=True, show_args=True)
def fn(...):
		...
```

Parameters:

- `show_lines` (default: `False`):
	- `True` prints each executed line.
- `show_locals` (default: `False`):
	- `True` prints local variables on each line event.
	- Works when line tracing is enabled.
- `show_args` (default: `True`):
	- `True` prints function arguments.
- Backward-compatible aliases:
	- `lines` maps to `show_lines`
	- `locals_on_line` maps to `show_locals`

### 2. `trace_state_start(show_locals=True)`

Enables detailed line tracing in the current running trace session.

Use this when you want extra detail only for one code block, usually around loops.

### 3. `trace_state_stop()`

Turns off detailed line tracing and goes back to compact output.

## Recommended Usage Pattern

Default mode should stay compact. Enable detail only around code you are debugging.

```python
from traceflow.api import trace, trace_state_start, trace_state_stop

@trace
def process(items):
		summary = []

		trace_state_start(show_locals=True)
		for item in items:
				summary.append(item * 2)
		trace_state_stop()

		return summary
```

This gives clean function-level trace, plus deep detail only inside the loop block.

## Output Format

TraceFlow uses symbols to make output easy to scan:

- `▶` function call
- `◀` function return
- `│ line N` line execution (when enabled)
- `✖` exception event

Wrapper summary:

- `result: ...`
- `time: ...`

Example:

```text
=== TraceFlow: add ===
▶ add(a=2, b=3)
◀ add() -> 5
result: 5
time: 0.000102s
=== End TraceFlow ===
```

## Current Example in `main.py`

The demo generates all combinations of `[1, 2, 3]` using backtracking and shows:

- recursive function tracing
- loop-state tracing only inside selected block

Expected combinations:

```text
[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
```

## Internal Behavior Details

### Re-entrancy / Nested Calls

- `trace` uses an internal depth counter.
- Only the top-level traced call starts and stops `sys.settrace`.
- Nested traced calls do not create duplicate top-level wrappers.

### Frame Filtering

Trace engine skips:

- internal TraceFlow module frames
- synthetic frames such as `<listcomp>`, `<dictcomp>`, and `<lambda>`

This keeps output focused on user code.

### Value Formatting

To avoid noisy output:

- large values are shortened
- lists/dicts are truncated
- objects are shown in compact readable form where possible

## Troubleshooting

### Output is too noisy

Use default compact mode:

```python
@trace
```

Enable detailed state only in a small block:

```python
trace_state_start(show_locals=True)
# debug target block
trace_state_stop()
```

### I only want line numbers, not full locals

```python
trace_state_start(show_locals=False)
```

### I do not want argument values

```python
@trace(show_args=False)
```

### Tracing does not start

- Ensure function is decorated with `@trace`.
- Ensure script is run from project root.

## License

MIT License. See `LICENSE`.
