# Wiring it into a real project

Half an hour, most of it spent on two regular expressions.

---

## 1. Copy four things

```
.github/          the machine
goedel.toml       the adapter
loop/goal.txt     your goal
tools/testrun.py  only if you want the example's runner; usually you do not
```

Delete `src/`, `tests/`, `bench/` and `tools/testrun.py` — they are the example
project, and they exist so that `ci` is green before you have configured
anything.

## 2. Draw the two boundaries

```toml
[project]
allow     = ["src/**", "tests/**"]
evaluator = [".github/**", "goedel.toml", "loop/**", "scripts/**"]
```

`allow` is what the machine may write to. `evaluator` is what it may never write
to, and it must cover, at minimum:

- `.github/**` — the machine itself
- `goedel.toml` — the file naming these masks
- `loop/**` — the record it reasons from
- **whatever runs and counts your tests** — the runner, the CI config it reads,
  the fixtures that decide what passing means

That last one is the one people get wrong. Your *tests* should be writable — a
bug fix has to be able to add the failing test that proves it — but the thing
that **counts** the tests must not be. A machine judged by a number it can
redefine is judged by nothing.

If the two masks overlap, `config` refuses to load and says which mask did it.
That is checked against the masks themselves, so a file you have not written yet
cannot slip through by not existing yet.

## 3. Describe your harness

```toml
[harness]
check = "…"     # seconds. a draft is re-asked with its output on failure
build = "…"     # optional
clean = "…"     # optional, and read the warning below
test  = "…"     # required
bench = "…"     # optional
artifact = "…"  # optional; its size becomes cost.artifact_bytes
```

**`clean` is the one that will bite you if you skip it.** Both arms of a
comparison are built in one workspace with a `git checkout` between them.
A cache keyed on modification time and file size — CPython's `__pycache__`,
a TypeScript `.tsbuildinfo`, incremental compiler state — cannot tell two
same-length edits written in the same second apart, so the candidate arm runs
the *baseline's* artifact and both arms report the same result. That was live
here and it was found by two probe files differing by one character.

The machine runs everything with `PYTHONDONTWRITEBYTECODE=1`, which stops new
Python caches being written. `clean` removes whatever the checkout brought with
it, and is the only place your project can say what its own version of this
hazard looks like:

| project | `clean` |
|---|---|
| Python | `find . -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null; true` |
| TypeScript | `rm -f tsconfig.tsbuildinfo` |
| Rust | *(not needed — cargo fingerprints on content)* |
| Go | *(not needed — the build cache is content-addressed)* |

`check` is the single highest-leverage line in the file. It runs up to six times
inside one draw and its refusals are what the next attempt is shown, so it is
the only feedback loop the drafter has. Make it fast and make it right about
whether code is broken.

`setup` is what has to happen before `check` can run at all — `npm ci`, `pip
install -e .`, whatever installs your dependencies. The drafting job is a fresh
checkout, so without it every attempt fails on a missing dependency, six times,
and the run reports that as the model being unable to write the milestone.

| project | `check` | `test` |
|---|---|---|
| Python | `ruff check src && python -m mypy src` | `pytest -q` |
| Node/TS | `npx tsc --noEmit` | `npm test` |
| Rust | `cargo check --all-targets` | `cargo test` |
| Go | `go vet ./...` | `go test ./...` |

## 4. Get the two regular expressions right

```toml
claims_re = '^\s*(?:ok|PASS|✓)\b'
suites_re = '(\d+) (?:tests?|examples?) (?:passed|ok)'
```

`claims_re` matches **one line per passing assertion**. `suites_re` captures a
**total**, and the last match wins — runners print a per-file tally as they go
and a grand total at the end, and the grand total is the one that describes the
run.

Check them by hand before trusting them:

```sh
npm test 2>&1 | grep -cE '^\s*(ok|PASS|✓)\b'
```

If that prints `0`, the loop has no J2 and every proposal will be refused for a
reason that has nothing to do with the code. `ci` fails loudly on a claim count
of zero rather than letting it go unnoticed — but it is much less confusing to
find out here.

Known-good starting points:

| runner | `claims_re` | `suites_re` |
|---|---|---|
| pytest `-v` | `PASSED` | `(\d+) passed` |
| jest | `^\s*✓` | `Tests:\s+(\d+) passed` |
| vitest | `^\s*✓` | `Tests\s+(\d+) passed` |
| `cargo test` | `^test .* ok$` | `(\d+) passed` |
| `go test -v` | `^--- PASS` | `^ok\s` *(no count — see below)* |
| TAP | `^ok \d` | `^1\.\.(\d+)` |

If your runner prints no total, leave `suites_re` matching nothing. `suites` will
be `0` in both arms, which never falls and therefore never vetoes — the claim
count carries the invariant on its own.

## 4b. Declare the drill's probe

`proof` runs a whole night against a candidate written by hand — no model, no
pushes — and it is the only test that covers the *seams* between the actions
rather than each action alone. Every bug that has actually shipped here lived
in a seam, so it is worth keeping after you adopt the template.

```toml
[proof]
kind = "feature"
target = "src/_goedel_probe.py"

[proof.pass]
"src/_goedel_probe.py" = """…code that works…"""
"tests/test_goedel_probe.py" = """…a test of it…"""

[proof.fail]
"src/_goedel_probe.py" = """…the same code, wrong…"""
"tests/test_goedel_probe.py" = """…the same test…"""
```

The two variants must write the same files and differ only in what the code
*does*; `config` refuses a pair that does not. The `fail` one should be
syntactically valid — a probe that will not parse only proves that
`harness.check` works, which is a different claim.

The refused drill is the one that matters. It is what checks that a refusal
builds on the live tree rather than filing the code it has just refused.

Delete the section and `proof` skips with a notice instead of failing.

## 5. Write the goal

One paragraph in `loop/goal.txt`, addressed to a competent colleague who has not
seen the project: what it is for, what "done" would look like, what you would
refuse. Vagueness here comes back as vague milestones, and a vague milestone is
one whose witness cannot be written — which the ladder refuses, so a vague goal
reads as a machine that proposes nothing.

Rewriting this file abandons every milestone underneath it, cleanly. Changing
your mind is one edit.

## 6. Add one secret and one variable

| | where | what |
|---|---|---|
| `GOEDEL_INFERENCE_KEY` | repository secret | your API key |
| `GOEDEL_INFERENCE_URL` | repository variable | only for a non-default endpoint |

`[author] provider = "anthropic"` is the default. `"openai"` covers any
OpenAI-compatible endpoint — vLLM, llama.cpp, a gateway — set through
`GOEDEL_INFERENCE_URL`.

Pick the model in `goedel.toml`. A nightly loop that writes a file at a time
does not need the largest model available, and `shards` buys more than model
size does: four independent draws at a raised temperature beat one careful one,
because only one of them has to survive the judge.

## 7. Apply the protections

[`.github/RULESETS.md`](../.github/RULESETS.md). Everything in code refuses;
those are the walls GitHub itself holds up. The one that surprises people is
**Settings → Actions → General → Allow GitHub Actions to create and approve pull
requests**, which is off by default and makes the audit PR step fail after
everything else in the night has already succeeded — a red square on a night
that worked, which is the shape that gets ignored.

## 8. Rehearse before you schedule

Run `proof` by hand. It runs a whole night against a hand-written candidate — no
model, no pushes — and fails loudly if the wiring is wrong. Then run
`loop-night` by hand with `dry_run: true`, which drafts and judges and writes
nothing.

Only then enable the schedule.

---

## Choosing kinds

Start with two and add more when the first two are boring.

```toml
[kinds.feature]
verb = "create"          # its target must NOT exist
j1 = "claims"            # the passing count must rise
targets = ["src/**"]     # what a milestone may be ABOUT

[kinds.repair]
verb = "edit"            # its target MUST exist
j1 = "witness"           # fail-then-pass
targets = ["src/**"]
```

`targets` narrows where a milestone may be *aimed*; it does not narrow what a
patch may *touch*, because a repair has to write a test. Leaving it out lets a
milestone be aimed anywhere in `allow`, which is how a `claims` kind gets gamed
by aiming at a test file.

Add a `rail` kind only once you have a benchmark you believe and floors measured
by the `floors` workflow on the runner class that will judge it. A performance
kind against an unmeasured floor adopts the weather.

---

## What to expect

**The first week does very little.** The archive needs six counted trials before
it will backtrack, the anchor stock is empty so `boundary` refuses outright, and
the ladder is writing its first milestones. This is the design working.

**Most nights refuse.** A refusal is a night that spent a runner and produced a
sentence about why the thing did not work. That is the normal outcome and the
ledger is mostly made of them.

**Read `ladder progress`, not the ledger.** It is at the top of the audit PR
body. The ledger says what was judged; the ladder says whether the loop is
getting anywhere, and that is the question you actually have.

**A milestone the drafter cannot write retires itself** after `judge.balks`
refusals and balks. Without that, a milestone it is stuck on is offered again
every night forever.

---

## When something is wrong

| symptom | cause |
|---|---|
| every draw fails on a missing module or binary | `[harness] setup` is empty and the check needs dependencies |
| `ci` fails with "nothing counted a single claim" | `claims_re` matches nothing |
| every night refuses with "adds no claim" | the drafter is not writing tests — put an example in `[kinds.*] prompt` |
| every night is `unstable` | your benchmark is noisier than its floor; run `floors` |
| both arms report identical results | a stale artifact survived the checkout — set `[harness] clean` |
| nothing is ever proposed | `loop/goal.txt` is too vague to decompose, or every milestone is retired |
| `config` refuses to load | an `allow` mask admits an `evaluator` path; the error names it |
| the audit PR step fails alone | the Actions setting in step 7 |
| `boundary` always refuses | no anchors are archived yet, or none is labelled |

The run log is verbose on purpose. Every refusal says which gate refused and
what it wanted instead.
