#!/usr/bin/env python3
"""The example project's test runner, and part of the evaluator.

It lives under `tools/` rather than under `tests/` because it is the thing
that decides what a passing claim IS, and `tests/` is writable by the machine.
A loop that can edit the counter is judged by nothing.

Its whole contract with the rest of the template is two lines of output:

    ok <name>              one per assertion that held
    N tests passed         once, at the end

which is what `harness.claims_re` and `harness.suites_re` in `goedel.toml`
match. Replace this file with your project's real runner and set those two
patterns to whatever it prints; nothing else in the machine cares.

Usage: python3 tools/testrun.py [directory]
"""

from __future__ import annotations

import importlib.util
import sys
import traceback
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else "tests")
    sys.path.insert(0, str(Path.cwd()))

    files = sorted(root.rglob("test_*.py"))
    if not files:
        # Not zero. A run that found no tests is a different fact from a run
        # where every test passed, and the second one is what `0 tests passed`
        # would read as -- silently, to a machine whose whole J2 is that this
        # number does not fall.
        print("no test files under " + str(root), file=sys.stderr)
        return 1

    passed = failed = 0
    for path in files:
        try:
            module = load(path)
        except Exception:
            failed += 1
            print(f"not ok {path} -- it did not import")
            traceback.print_exc()
            continue
        for name in sorted(dir(module)):
            if not name.startswith("test_"):
                continue
            fn = getattr(module, name)
            if not callable(fn):
                continue
            try:
                fn()
            except Exception as exc:
                failed += 1
                print(f"not ok {path.stem}.{name} -- {exc}")
                traceback.print_exc()
            else:
                passed += 1
                print(f"ok {path.stem}.{name}")

    print(f"\n{passed} tests passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
