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

Use this template and run `genesis`. There is nothing to configure first:

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

**4. Nothing.** There is no step four. The model runs in the job — a pinned
llama.cpp build and a pinned GGUF, fetched, digest-checked and cached — so
there is no key to add and no account to hold. `[author] provider =
"anthropic"` or `"openai"` in `goedel.toml` points it at a hosted endpoint
instead if you would rather, and those do want a credential.

**5. Apply the branch protections** in [`.github/RULESETS.md`](.github/RULESETS.md).
Everything in code refuses; those are the walls GitHub itself holds up.

**6. Run `proof` by hand once.** It runs a whole night against the probe you
declared in `[proof]` — no model, no pushes — and files a synthetic run of
certificates to check the claims the epoch rules make about a *sequence* of
them. It tells you the wiring is right before you let a schedule loose on it.
Then enable the `loop-night` schedule.

`ci` and `proof` need no model at all and are green from the first push.

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
| `model` | the authors, running in the job: pinned files and a server, one per shard |
| `template-check` | the machine checked against itself |
| `selftest-all` | runs every suite from disk, for the one gate that needs it |

Every action answers `command: selftest` and `ci` runs all twenty-one. An action
that cannot prove itself is refused by `template-check`, because that is how a
check gets deleted — not by argument, by nobody noticing it went.

---

## The parts worth knowing about

### The model runs in the job, and that is why there is no key

`[author] provider = "local"` fetches a pinned llama.cpp build and a pinned
GGUF, checks both against a size and a digest, caches them, and serves them on
loopback. `draft` talks to that. Nothing in the nightly loop holds a
credential, because there is no credential.

The original of this machine was built against a hosted endpoint that retired
mid-loop — `HTTP 410 github_models_retirement_brownout` — and took the loop
with it. The property that endpoint had been chosen for was *no new
credential*; a model in the job has it more completely, and two files with
digests do not get retired, rotate keys or bill.

It is also what keeps the record meaning something. A certificate names the
night that produced it. llama.cpp tags a release per commit, so `latest` moves
several times a day — an interpreter that changed under the loop would make
every certificate name a night nobody can reproduce.

Two details are worth knowing because they cost a week to find. The server is
started **without** `--no-warmup`: that defers the weight load to the first
request, so `/health` answers in four seconds and the completion then times
out. And it is started **with** `--reasoning off`: these weights open every
answer inside a `<think>` block otherwise, and a grammar does not stop it —
measured here, a request without the switch came back with `content` empty and
the whole answer in `reasoning_content`. A perfectly shaped answer that reads
as none, which is refused for having no fence, fed back, refused again, and
filed as a balk. Three balks retire a milestone the model was never allowed to
see. `draft` asks for the same thing per request, so neither half depends on
the other being there.

### Several models, one per shard

A night fans out over N shards, and each shard is already its own runner with
its own four vCPU. Nothing says they must all run the same weights. Declare a
pool and shard N draws with `pool[N % len(pool)]`:

```toml
[[author.local.pool]]
name = "qwen38-4b"
weights = "…/Qwen3.8-4B-Q4_K_M.gguf"
weights_sha256 = "dec96e8c…"
weights_bytes = 2783446304

[[author.local.pool]]
name = "qwen38-4b-q8"
…
```

This is a **portfolio, not a conversation.** The models never see each other's
work; each draws independently and one judge decides. That is the point — a
second model is a genuinely different prior, which is not the same thing as a
second temperature sample from one, and the fan-out already exists to buy
exactly that. It costs nothing in wall clock, because the shards were running
in parallel anyway.

Every certificate records **which author drew it**, and `archive report` prices
each one under the same Beta(1,1) the clades use:

```
  the portfolio, best first
  author        adopted  trials  cmp
  qwen38-4b-q8  4        7       0.556
  qwen38-4b     3        9       0.364
```

A portfolio you cannot attribute is one you cannot learn from. With the counts
recorded, "is this model worth a runner" stops being a matter of taste.

**And the night spends its runners on that.** `archive authors` Thompson-samples
the assignment against the ledger: shard 0 takes the best posterior mean — it is
the greedy shard everywhere else here, so the best-known author never misses a
night — and the rest draw independently from Beta(1+S, 1+F). Measured over forty
synthetic nights, four shards each:

| the record | runners won |
|---|---|
| 7/9 against 1/9 | 160 – 0 |
| 5/9 against 3/9 | 135 – 25 |

The second row is the interesting one. A contested pair keeps splitting, because
the challenger's posterior is still wide; a settled one stops, because it is not.
Nothing is hard-coded about either outcome — the same sampler produces both, and
what changed is the evidence. The 7/9 author is not permanently safe either: its
challenger wins about one sampled shard in 385, so it is re-tried, just rarely.

Duplicates are the point rather than a bug. Two shards on the model with the
record and two on the challenger is the allocation the evidence justifies;
forcing one shard each would spend the same runners ignoring everything the
ledger knows. With one author, or none attributed yet, it is uniform — which is
correct, and is why there is no minimum-evidence floor here as there is on
`reconsider`. Sampling two identical priors costs nothing; *backtracking* on them
would move the night somewhere for no reason.

**A record does not expire, and that is a real limitation.** An author is scored
over every trial it has ever had, so a model that did badly against an old goal
carries that forever, and a model added tonight starts from the uniform prior
rather than from anything it has shown. Epoch-scoping the tally would be the
principled fix — `utility` already changes only at epoch boundaries, and entries
judged by different criteria are not strictly comparable — but sixteen entries an
epoch is thin evidence to sample from. It is named here rather than half-solved.

**The cache is the ceiling.** GitHub gives a repository 10 GB of Actions cache,
evicted least-recently-used, so three 2.78 GB authors fit and four do not. Over
the limit nothing breaks — a miss is a 55-second download on a runner about to
spend thirty minutes — but a pool that thrashes pays that on every shard of
every night. Mixing sizes is how to spend it: a 4B and a 1.7B cost less
together than two 4Bs and disagree more.

**What this deliberately is not** is models reviewing each other. The judge is
code, and `[project] evaluator` exists so that nothing the loop proposes can
touch what judges it. An LLM reviewer would be a judge the machine could argue
with, which is the one thing this whole arrangement is built to prevent.

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
