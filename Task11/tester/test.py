import os
import time
import inspect
import importlib
import traceback
from multiprocessing import Pool

TESTS = []
FIXTURES = {}
SKIPPED = {}

def test(func):
    TESTS.append(func)
    return func

def fixture(func):
    FIXTURES[func.__name__] = func
    return func

def skip(reason=""):
    def wrapper(func):
        SKIPPED[func.__name__] = reason
        return func
    return wrapper

def parametrize(name, values):
    def wrapper(func):
        func._params = (name, values)
        return func
    return wrapper


def assert_equal(actual, expected):
    if actual != expected:
        raise AssertionError(
            f"Expected {expected}, got {actual}"
        )

def get_fixtures(func):
    args = {}
    params = inspect.signature(func).parameters
    for p in params:
        if p in FIXTURES:
            args[p] = FIXTURES[p]()
    return args

def run_test(func):
    start = time.time()
    if func.__name__ in SKIPPED:
        return ("SKIP", func.__name__, 0, SKIPPED[func.__name__])
    try:
        args = get_fixtures(func)
        if hasattr(func, "_params"):
            name, values = func._params
            for v in values:
                func(**args, **{name: v})
        else:
            func(**args)
        return ("PASS", func.__name__, time.time() - start, "")
    except Exception:
        return ("FAIL",
                func.__name__,
                time.time() - start,
                traceback.format_exc())

def discover():
    modules = 0
    for file in os.listdir("tests"):
        if file.startswith("test_") and file.endswith(".py"):
            importlib.import_module(f"tests.{file[:-3]}")
            modules += 1
    return modules

def run_all():
    with Pool(4) as pool:
        return pool.map(run_test, TESTS)

def report(results):
    passed = failed = skipped = 0
    total_time = 0
    for status, name, duration, info in results:
        total_time += duration
        if status == "PASS":
            passed += 1
            print(f"PASS {name}")
        elif status == "FAIL":
            failed += 1
            print(f"FAIL {name}")
            print(info)
        else:
            skipped += 1
            print(f"SKIP {name} ({info})")
    print("\n=== Summary ===")
    print(
        f"{len(results)} tests | "
        f"{passed} passed | "
        f"{failed} failed | "
        f"{skipped} skipped"
    )
    print(f"Total time: {total_time:.02f}s")

def main():
    print("=== Test Discovery ===")
    modules = discover()
    print(f"Found {len(TESTS)} tests across {modules} modules")
    results = run_all()
    print("\n=== Execution ===")
    report(results)

if __name__ == "__main__":
    main()