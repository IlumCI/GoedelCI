# How it fits together

Three file formats and one flow. Everything else is detail.

---

## The formats

### The envelope — a proposal

Written by `draft`, admitted by `envelope`, named by its own digest (its
**point**), and committed to `loop/ledger/tried/` *before* anything runs it.

```
[envelope] v2
kind repair
verb edit
target src/cache.py
lane model
axis src/cache.py
rung 3
corpus 00000000
parent-tree 8c31760b…          the tree the drafter was looking at
operator cross-lineage          which comparative evidence wrote it
lineage a4f2…                   the certificate this descends from
seed 2                          which shard, or `-` for the greedy one
witness a test that evicts past the bound
title An LRU bound on the resolver cache
[witness]
<a unified diff that must FAIL on the parent tree>
[patch]
<a unified diff that must make it pass>
[end]
```

**Two diffs, not one, and that is the three-tree shape.** A bug fix with one
diff is a diff with a story attached. Separated, the judge can build *parent*,
*parent + witness* and *parent + witness + fix*, and record that the witness
failed on the second and passed on the third. That recording is what makes a
certificate a certificate.

Admission runs before a runner is spent and checks the diff rather than the
declaration: every path the patch touches must be inside `allow`, outside
`evaluator`, and inside the kind's own `targets`; no binary patches; within the
kind's line and file budget; and the declared target must actually appear in the
diff. A patch that says `src/a.py` in its header and edits a workflow in a hunk
is exactly the mistake the masks exist to stop, and checking the header would
not see it.

### The rail file — a measurement

Whatever your benchmark prints, gathered over `repeats` runs:

```
[rail] v2
bench.total_ms 13.838,12.867,12.874 ms lower
cost.warnings 0 n lower
[rail] end
```

Samples rather than a value, because a single pair of readings cannot tell a
change in the code from the day the runner is having.

### The certificate — a decision

One line per field, content-named, written once and never edited:

```
version 2
seq 14
utc 2026-09-24T02:17:41Z
point 561ad711…
kind feature
lane model
operator cross-lineage
lineage a4f2…
epoch 0
utility 391563f2…            the digest of the judge that decided this
…
claims 6/8
moved better
effect -0.201
interval -0.205,-0.194
q 0.004
why it builds, it passes, it added 2 claim(s) and lost none
verdict adopt
```

Every field is required and every field is checked. A field missing is not a
gap; it is a file this machine declines to call a certificate, because the
missing one is always the one that mattered. `-` means *nobody counted this* and
is a different fact from `0`, which means somebody counted and got none.

`cert` also refuses combinations no single field can catch: an adoption whose
candidate tree equals its parent changed nothing; an adoption on a `worse` or
`unstable` reading adopted noise; an adoption whose interval straddles zero
adopted noise more precisely; an adoption that reduces a count deleted a test.

---

## The record

```
loop/
  goal.txt                       one paragraph. yours.
  ladder/rungs.txt               milestones, appended
  ledger/entries/<name>.cert     one per night, named by its own digest
  ledger/tried/<point>.env       the envelope, committed before the trial
  anchors/<point>/               before.txt, after.txt, claims, ground
  evidence/floors/<stamp>.tsv    what this runner class's noise actually is
  boundary/                      proposed changes to the evaluator
```

`ledger fsck` runs before the night reads the record and again after it writes
it, and checks what the *directory* claims about itself:

- every file is named by the first 16 hex of its own digest — an edited
  certificate stops being the file the ledger says it is;
- the sequence numbers are exactly `1..N`, no gaps and no repeats;
- timestamps do not go backwards;
- every `lineage` names an earlier entry that was **adopted** — a tree that was
  never adopted is not a state anything could have been built from;
- entries within one epoch carry one `utility` digest, epochs advance by
  exactly one, and only at a multiple of `epoch_len`. The digest covers the
  `criterion` masks — the judge — and deliberately not the record, which
  changes every night and would otherwise make every entry in an epoch
  disagree about which judge decided it;
- every tried marker hashes to the point it is named for.

Per-field validity is delegated to `cert check-dir`, so the field table exists
in exactly one place.

**Rung state is derived, never stored.** Whether a milestone is open, met or
retired is read off the ledger: met when an adopted certificate carries its
point, retired after enough refusals carry it. A counter in the ladder file
would be a second account of the same history and would eventually disagree with
the first. Balks are the one exception, because a draw that came back with
nothing files no certificate to count.

---

## A night

```
                 ┌──────────┐
   your main ───▶│  follow  │  merge main; a conflict means you overrode an
                 └────┬─────┘  adoption, and that is recorded, not hidden
                      ▼
                 ┌──────────┐  fsck · archive report · budget
                 │   plan   │  reconsider → maybe commit a backtrack
                 └────┬─────┘  ladder propose → maybe commit a milestone
                      ▼
        ┌────────┬────┴───┬────────┐
     shard 0  shard 1  shard 2  shard 3     ← draft, in parallel
      greedy   seeded   seeded   seeded        each held to `harness.check`
        └────────┴────┬───┴────────┘           and re-asked with its refusal
                      ▼
                 ┌──────────┐  lowest shard that drew wins
                 │  stage   │  mark tried · push loop/cand/<point>
                 └────┬─────┘
                      ▼
                 ┌──────────┐  arm a: the baseline
                 │  judge   │  arm w: witness alone — must FAIL
                 └────┬─────┘  arm b: the candidate
                      ▼        one runner, both arms, no secrets
                 ┌──────────┐  adopt-decide → which tree
                 │  adopt   │  one commit: the code AND the certificate
                 └────┬─────┘  the rolling audit pull request
                      ▼
                  loop/main ──▶ a PR you merge when you feel like it
```

**One concurrency group** across every job. That is what makes
fast-forward-only real: there is never a second night interleaving with this
one, so adopt's read-then-commit is atomic in the only sense that matters.

**The judge holds no secrets and asks for `contents: read`.** It is the part of
the loop most exposed to the candidate's own content, because it builds and runs
it, so it is the part least entitled to authority. A verdict becomes real only
when `adopt` — which never runs candidate code — commits the certificate.

**A candidate that does not build is a refusal, not a red run.** A red job files
no certificate, so the milestone that produced it never moves, and under a
schedule that is a silent stall where the same broken file is drafted every
night forever. The *baseline's* build staying fatal is the other half of the
same rule: a baseline that will not build is the branch, not the candidate.

---

## The judgement

Every kind carries the same **J2**, checked before its own criterion is even
looked at:

- suites, claims and checks may not fall;
- the candidate's tests must pass;
- no rail may read `worse` unless the kind declared it in `allow_rails`;
- no rail may read `unstable` — that is a *starved* trial, not a failed one,
  and it raises the budget rather than counting against the milestone.

Then **J1**, which is what the kind is for:

| `j1` | adopted when |
|---|---|
| `witness` | the witness failed on the parent and passes with the fix |
| `claims` | the passing-assertion count strictly rose |
| `rail` | the named rail improved past its floor and survived the correction |
| `cost` | a cost rail improved and nothing else regressed |

`config` refuses at load time a kind with no J1. A kind with no primary
criterion can only ever be adopted on *nothing broke*, which is adoption on the
absence of evidence.

### Why `claims` is the honest bar for new code

A witness must build against the **parent** tree, and a module being created is
by construction absent from it — so the witness arm dies of infrastructure
rather than of its claim, and a greenfield kind judged by fail-then-pass refuses
every candidate it could ever have. What is mechanically derivable instead is
weaker and is stated as such: it builds, it passes, it lost no claim and it
*added* one, so the new code is exercised by something that printed a pass
rather than merely compiling. It does not say the feature is correct.

It is not gameable in the direction that matters. A claim costs running one; the
monotonic counts catch anything traded away for it; `targets` stops a milestone
being aimed at a test file; and the diff budget and path masks are unchanged.

### How a measurement is decided

**The samples are taken by alternating between the two trees**, one reading of
each per round. Measuring all of one arm and then all of the other makes every
baseline reading older than every candidate reading, so a runner that warms up
or a neighbour that arrives lands entirely on one side. On two trees whose
behaviour is byte-for-byte identical, block measurement reported −0.03%, −8.84%
and −28.27% on three consecutive runs; alternating reported +0.15%, +0.44% and
−1.12%. `bench-pair` owns that, because it needs git and `harness` deliberately
does not.

Then, in this order, and the order is the design:

1. **The floor.** Inside its declared floor is not a movement. First, because it
   needs no samples and because a rail whose floor is 5% should not produce a
   confident 0.4% discovery however many times it is measured.
2. **The run's own wobble.** A second reading of the *same* artifact, when the
   caller supplies one. Redundant once the samples are interleaved — the
   within-arm spread is in the samples themselves — and kept for callers taking
   a single reading per arm.
3. **The interval.** With three or more samples, a percentile bootstrap on the
   relative difference of medians plus a permutation p-value. An interval that
   straddles zero is `unstable`.
4. **The correction.** Benjamini–Hochberg across the comparison's discoveries.

**The asymmetry is the safety property.** `better` is corrected; `worse` is not.
A veto that gets weaker the more things you measure is one an author can dilute
by adding rails.

*(The permutation statistic is deliberately not the relative effect: dividing by
the baseline makes it asymmetric under relabelling, so half of all permutations
beat the observed value and every real effect reads p ≈ 0.5. It is the absolute
gap over a pooled scale, and there is a claim asserting it.)*

---

## The budget

A trial that came back `unstable` did not fail — it was **starved**. The
measurement could not tell the change from the day, and repeating it at the same
budget will starve again, every night, for good. So the OOPS schedule doubles:

```
level    consecutive starved trials, capped
minutes  base × 2^level
repeats  base × 2^level      ← what a doubled budget actually buys
half     extend | explore    ← greedy or sampled clade selection
```

`repeats` is the important one, and it is spent as ROUNDS of the alternating
measurement: more samples per arm is the only thing that narrows a confidence
interval, and taking them alternately is the only thing that keeps them about
the trees rather than about the hour.

---

## When the plan is finished

`blueprint phase` answers `done`, and two things change.

The night's card stops carrying phase criteria and starts carrying what
`survey` found. A survey finding is not a lint result: each one states **what a
test of it would have to observe**, because that sentence becomes the
milestone's witness and a finding without one is a complaint. Findings are
ordered unsafe → swallowed → stub → mock → validation → untested, deduplicated
by rule and by location, and capped at five per file so one neglected module
cannot fill the list.

`directions` proposes 2–5 complete replacement plans, one pull request each,
and does nothing at all if any are already open. Each carries a whole
`loop/blueprint.txt` that has already been through `blueprint`'s admission, so
merging one is sufficient for the next night to start building it. `decided.yml`
closes the rest on merge and files a `superseded` event in the ledger — a
change to the blueprint is the most consequential thing that can happen to the
repository without any code moving, and a record that did not mention it would
leave an unexplained discontinuity.

**The promotion job selects the audit pull request by head branch.** That is a
guard, not a lookup: a `direction` pull request asks what the project should
*become*, and the judge has no opinion about that. It knows whether a change
made the project worse against a fixed standard; it cannot tell you which
standard it should have been held to.

## The boundary

The one lane that may edit the evaluator, and the reason this is a self-improving
repository rather than an automated one. It is dispatched by hand and gated in
five places — Epoch, Sane, Moves, Honest, Remembers — described in the README
and implemented in `boundary-judge`. Its output is a pull request behind a
protected environment; it never pushes, not even to `loop/main`.

A boundary proposal may touch **only** evaluator paths: the exact inverse of
every other mask in the repository. A diff reaching into the project as well
would be an ordinary change smuggled through the one lane that does not judge
ordinary changes — adopted on Moves and Honest, which say nothing about whether
the project still works.
