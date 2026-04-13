import time
import inspect
from functools import wraps

# Global variable to track recursion depth
call_depth = 0


def funFlow(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global call_depth

        indent = "  " * call_depth
        func_name = func.__name__

        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        print(f"{indent}Function: {func_name}")
        print(f"{indent}Arguments: {dict(bound.arguments)}")

        start_time = time.perf_counter()
        call_depth += 1

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            call_depth -= 1
            print(f"{indent}Error: {e}")
            raise

        call_depth -= 1
        end_time = time.perf_counter()

        print(f"{indent}Result: {result}")
        print(f"{indent}Execution Time: {end_time - start_time:.6f}s\n")

        return result

    return wrapper


# ---------------- TEST CODE ---------------- #

if __name__ == "__main__":

    @funFlow
    def add(a, b):
        return a + b

    @funFlow
    def factorial(n):
        if n < 0:
            raise ValueError("Negative not allowed")
        if n == 0 or n == 1:
            return 1
        return n * factorial(n - 1)

    print("---- ADD ----")
    add(3, 5)

    print("\n---- FACTORIAL ----")
    result = factorial(5)
    print(f"\nFinal Result: {result}")