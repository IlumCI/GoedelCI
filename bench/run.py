#!/usr/bin/env python3
"""The example project's benchmark, and part of the evaluator.

Anything printing

    <name>.<rail> <value> <unit> lower|higher

becomes a rail the judge compares between the two arms. Everything else it
prints is ignored, so a benchmark may log freely.

It lives under `bench/` rather than under `src/` because it decides what a
rail READS, and a machine that can edit its own measuring apparatus is
measured by nothing.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.window import Window  # noqa: E402

N = 200_000


def main() -> int:
    start = time.perf_counter()
    w = Window(64)
    for i in range(N):
        w.push(i * 0.5)
    total = w.mean() + w.peak()
    elapsed = (time.perf_counter() - start) * 1000.0

    print(f"pushed {N} values, summary {total:.3f}")
    print(f"bench.total_ms {elapsed:.3f} ms lower")
    print(f"bench.push_ns {elapsed * 1e6 / N:.3f} ns lower")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
