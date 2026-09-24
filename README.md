# GoedelCI

A repository that builds itself, as a template.

You say what you want. It writes the specification, plans it into phases,
builds the first one, proves the result actually runs, and then improves it
every night — measuring each change against the version before it and keeping
only what did not make anything worse. With autonomous promotion on, nothing
in that sentence involves you.

<!-- goedel:brief -->
Replace this block with what you want built. A paragraph is plenty; a sentence
is fine; deleting it entirely is also fine, because a name and a kind of thing
carry most of a specification on their own. Whatever is here, `genesis` reads
it, builds it out into `loop/brief.md`, and shows you that before writing a
line of code.
<!-- /goedel:brief -->

---

## Starting one

Use this template, add one secret (`GOEDEL_INFERENCE_KEY`), and run `genesis`:

| | |
|---|---|
| **name** | what the thing is called |
| **type** | `app` · `api` · `agent` · `token` · `business` · `experiment` |
| **description** | optional — the README block above is read when it is empty |
| **autonomous** | whether nights promote their own work |

Then wait. The first pull request carries the brief it wrote, the plan it drew,
and a working phase one.

**A name and a type is a complete input.** A kind of thing carries most of its
own requirements — an API has routes and a schema, an agent has tools and an
eval set, a token utility site has a thing the token actually does — so the
missing half is filled in from what that kind of thing usually is. Everything
it decided is in `loop/brief.md`, including what it decided *not* to build,
which is where you look first if it guessed wrong.

It will not invent facts about the world. No testimonials, partners, audits,
holder counts, endorsements or performance claims appear in anything it writes,
because it has no way to know which of those are true.

---

## When the plan is finished

Nothing stops. Two things start.

**It maintains.** A finished plan is not a finished project: the first version
of everything is full of the stub put in to get a test passing, the error
caught and dropped, the input nothing validates, and the module no test names.
`survey` finds those and states each one as *what a test of it would have to
observe* — so they become ordinary milestones, judged by the ordinary judge.

**It asks you one question.** `directions` proposes two to five genuinely
different things the project could become, each as its own pull request, each
carrying a **complete replacement plan** rather than a suggestion. Merging one
replaces `loop/blueprint.txt`, and the next night starts building it. The
others close automatically with a comment saying which one won.

It proposes once and then waits — indefinitely, without degrading, because the
maintenance nights carry on the whole time. Close them all without merging and
it proposes a fresh set.

**Autonomous promotion never touches a direction pull request.** It merges only
the audit PR, by head branch, as a guard rather than a lookup. What a thing
should *become* is not a question the judge can answer: it knows whether a
change made the project worse against a fixed standard, and has no opinion
about which standard it should have been held to. A loop that picks its own
next objective is one whose record stops meaning anything, because every
verdict would be relative to a goal it chose partly because it was reachable.

That is the one decision left to you, and it is the only one.

---

## What it does in one night

```
follow      take whatever you pushed to main; record anything it overrode
reconsider  ask the record whether the current state is the best place to build
            from, and go back up the lineage if it is not
ladder      if no milestone is open, decide the next one toward your goal
draft       fan out N independent attempts at it; each one is held to your
            project's own fast check and re-asked with the compiler's refusal
judge       build and test BOTH the old tree and the new one, on one runner,
            and decide
adopt       commit the code and the certificate in one commit, or commit the
            refusal alone
```

The certificate is the point. Every night leaves one, whatever happened:

```
verdict   adopt
kind      feature
operator  cross-lineage
why       it builds, it passes, it added 2 claim(s) and lost none; no rail regressed
claims    6/8
effect    -0.201
interval  -0.205,-0.194
```

A week of these is a readable account of what your repository did while you were
not looking, and every one of them is re-checkable: the record is content-named,
so an edited certificate stops being the file the ledger says it is.

---

## Adopting it into a project that already exists

Genesis is for a repository that does not have one yet. To put the loop around
code you already have:

**1. Copy** `.github/`, `goedel.toml` and `loop/` into the repository.

**2. Edit `goedel.toml`.** It is the whole adapter between this machine and your
project, and it is commented at length. The parts that matter:

```toml
[project]
allow     = ["src/**", "tests/**"]          # what the machine may write to
evaluator = [".github/**", "goedel.toml",   # what it may never write to
             "loop/**", "tools/**"]

[harness]
check = "npm run typecheck"                  # seconds; a draft is held to this
test  = "npm test"                           # the only required line

claims_re = '^\s*(?:ok|✓|PASS)\b'            # what a passing assertion looks like
suites_re = '(\d+) (?:tests?) passed'        # what a total looks like
```

The two regular expressions are the ones worth getting right. If `claims_re`
matches nothing, every proposal is refused for a reason that has nothing to do
with the code — so `ci` fails loudly on a claim count of zero rather than
letting that go unnoticed.

**3. Write `loop/goal.txt`.** One paragraph, addressed to a competent colleague
who has not seen the project. This is the only thing the machine cannot write
for itself.

**4. Add one secret.** `GOEDEL_INFERENCE_KEY`, under Settings → Secrets →
Actions. The default provider is Anthropic; `[author] provider = "openai"` in
`goedel.toml` points it at any OpenAI-compatible endpoint instead, including a
llama.cpp server on your own machine via `GOEDEL_INFERENCE_URL`.

**5. Apply the branch protections** in [`.github/RULESETS.md`](.github/RULESETS.md).
Everything in code refuses; those are the walls GitHub itself holds up.

**6. Run `proof` by hand once.** It runs a whole night against the probe you
declared in `[proof]` — no model, no pushes — and files a synthetic run of
certificates to check the claims the epoch rules make about a *sequence* of
them. It tells you the wiring is right before you let a schedule loose on it.
Then enable the `loop-night` schedule.

Until step 4, everything still works except `draft` and the ladder: `ci` and
`proof` are green, and the machine simply has nothing to write with.

---

## What is here

| | |
|---|---|
| **Workflows** | |
| `ci.yml` | the gate: the machine proves itself, then your project builds and tests |
| `genesis.yml` | a name and a type become a brief, a plan and a phase one |
| `genesis-build.yml` | one attempt at that phase one, called by `genesis` up to three times |
| `loop-night.yml` | the night — follow, reconsider, ladder, draft, judge, adopt, tidy |
| `loop-judge.yml` | the two-arm gate, called by the night and runnable by hand |
| `proof.yml` | two drills end to end, plus a synthetic epoch; no model, no pushes |
| `directions.yml` | when the plan is done: 2-5 competing plans, one PR each |
| `decided.yml` | one was merged, so the others close |
| `boundary.yml` | the only lane that may change the evaluator itself |
| `floors.yml` | measures this runner class's own noise, as data |
| **Actions** | |
| `config` | `goedel.toml` — validated, and the digest of the evaluator judging you |
| `brief` | a name and a kind of thing, expanded into a specification |
| `blueprint` | that specification, planned into phases with observable criteria |
| `scaffold` | phase one, written whole, with `config` assembling the boundary |
| `cert` | the certificate format; the only place the field table lives |
| `ledger` | the append-only record, and the fsck that is the whole trust in it |
| `archive` | the lineage tree, clade metaproductivity, where to build from next |
| `ladder` | your goal, decomposed into milestones that each name a witness |
| `draft` | the only thing here that writes code |
| `envelope` | the proposal: admitted before it runs, derived through a temp index |
| `harness` | your build, tests and benchmark — it knows no language |
| `bench-pair` | measures two trees by alternating, so time is not compared |
| `rails` | paired comparison with a floor, an interval and an FDR |
| `budget` | how much a starved trial gets to spend next time |
| `adopt-decide` | which tree a commit is built on, as a pure function |
| `boundary-judge` | Epoch, Moves, Honest, Remembers |
| `survey` | what is left: stubs, swallowed failures, unsafe patterns |
| `directions` | complete alternative plans, for you to pick between |
| `template-check` | the machine checked against itself |
| `selftest-all` | runs every suite from disk, for the one gate that needs it |

Every action answers `command: selftest` and `ci` runs all twenty. An action
that cannot prove itself is refused by `template-check`, because that is how a
check gets deleted — not by argument, by nobody noticing it went.

---

## The parts worth knowing about

### It cannot edit its own judge

`[project] evaluator` names the machine, the config, the record, the test
runner and the benchmark. (`criterion` is the subset that *is* the judge —
everything but the record — and it is what each certificate's `utility` digest
covers.) Nothing the loop proposes may touch any of them, and
`config` refuses to load at all if an `allow` mask admits an `evaluator` path —
checked against the masks rather than the tree, so a file that does not exist
yet cannot slip through by not existing yet.

Your test runner is in that list deliberately. `tests/` is writable, because a
bug fix has to be able to add the failing test that proves it. The thing that
*counts* the tests is not: a machine judged by a number it can redefine is
judged by nothing.

### The counts may not fall

Test suites, passing assertions, and harness commands that succeeded. None of
the three may be lower in the new tree than the old one, for any kind of change,
and it is checked in the certificate format itself so that no rule can forget
it. It is the only thing standing between a machine that improves its test
numbers and a machine that deletes its tests.

### "Better" is a statistical claim, not a comparison

A rail is a measurement your benchmark prints. The two arms are measured by
**alternating** between them, one reading of each per round, because measuring
one arm and then the other puts every warm-up and every noisy neighbour on one
side of the comparison — on two trees that behave identically, that produced a
spurious 28% "improvement". Then four gates decide whether anything moved: the
declared floor, the run's own second reading, a percentile bootstrap interval on
the difference of medians, and Benjamini–Hochberg across every rail.

Improvements are corrected for multiple comparisons. Regressions are
deliberately not — a veto that gets weaker the more things you measure is a veto
that can be diluted by adding rails.

If your project has no benchmark, none of this runs and the test counts decide.

### It backtracks

The record is a tree, not a list: every certificate names the one it descends
from. Clades are scored by how well their *descendants* did, not by how well the
tip itself scored, and the night samples which clade to build from — an
ancestor of where it is now, or a cousin lineage it left behind weeks ago. A
branch of work whose last four attempts all failed stops being where tomorrow
starts.

Below six counted trials this never fires — a clade comparison over four trials
is a comparison of two priors.

### Changing your mind is one edit

Every milestone records a digest of `loop/goal.txt` as it stood when it was
written. Rewrite that file and every milestone underneath it is stale by
construction: the machine skips them and writes fresh ones. No bookkeeping.

### It can change its own judge, twice-gated

`boundary` is the one lane that may edit the evaluator. It is dispatched by
hand, and it refuses unless:

- the ledger sits exactly at an epoch boundary (the criterion holds still
  *within* an epoch, or nothing in the record is comparable);
- every action still proves itself with the change applied;
- the old and new judges **disagree** about at least one archived comparison
  (a judge change that changes no verdict is a diff with a story);
- every disagreement **sides with** that comparison's recorded ground truth;
- and the new judge still **refuses** everything the old one refused and ground
  truth calls noise.

Then it opens a pull request behind a protected environment. Two human
decisions, and it never pushes.

With no archived comparisons every one of these refuses rather than passes. A
question that cannot be asked is not a question that was answered.

---

## What it is not

It is **not** a verified Gödel machine. Schmidhuber's construction adopts a
self-modification only on a proof that it raises expected utility; nothing here
proves anything. It measures, with intervals, and it keeps the record that lets
you check the measurement later. Where the literature says *provably better*,
this says *better on this evidence, at this bar, with the bar written down*.

It is **not** autonomous of you. Its whole world is `loop/*`. Its token has no
`workflows` write, so GitHub itself rejects any push touching `.github/`, and
the audit pull request is its only route to your default branch.

It will **not** make a bad project good. It makes a project with real tests and
a clear goal incrementally better without you in the loop, and it tells you
plainly when it could not.

---

## Where it comes from

The shape is lifted from [IlumCI/GLaDOS](https://github.com/IlumCI/GLaDOS)'s
self-improvement CI and generalised until nothing about it assumed a Rust UEFI
kernel. The ideas underneath it are recent and are cited where they are
implemented; [`docs/RESEARCH.md`](docs/RESEARCH.md) says which paper is doing
what, and where each one is only partly done.

- [`docs/RESEARCH.md`](docs/RESEARCH.md) — the literature, and what is borrowed
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — the formats and the flow
- [`docs/ADOPTING.md`](docs/ADOPTING.md) — wiring it into a real project
- [`.github/RULESETS.md`](.github/RULESETS.md) — the protections to apply
