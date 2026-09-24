# What this borrows, and from where

Self-improving coding agents went from a curiosity to a crowded field between
2024 and 2026. This template is not a research artefact and does not claim a
result; it is an attempt to take the parts of that work that survive contact
with a real repository and a nightly cron, and leave out the parts that need a
benchmark harness and a research budget.

Every section below says what the idea is, where it lives in this repository,
and — the part usually left out — **what is not done**.

---

## The original claim

**Gödel machine** — Schmidhuber, 2003. A machine that rewrites its own code
only when it can *prove* the rewrite raises expected future utility. The proof
requirement is what makes it optimal and what makes it unimplementable: for any
interesting utility over an open world, the proofs are not available.

**What this does instead.** Measures, with a confidence interval, at a bar that
is written down in a file, and keeps a record that lets the measurement be
re-checked. Where the theory says *provably better*, this says *better on this
evidence, at this bar*. That is a much weaker claim and it is stated as one
everywhere it appears.

**Not done.** Nothing here proves anything. A certificate is a record of a
decision procedure having run, not a proof that the decision was right.

---

## Open-ended self-modification

**Darwin Gödel Machine** — Zhang et al., [arXiv:2505.22954][dgm]. Drops the
proof requirement and keeps an archive: agents self-modify, are benchmarked, and
the archive is sampled to pick the next parent. Open-ended exploration over a
growing tree rather than hill-climbing on one agent.

**Here.** The ledger *is* the archive. Every certificate names the one it
descends from (`lineage`), so the record is a tree rather than a list, and
`archive` reconstructs it. Adopted trees are nodes; refusals are evaluations
attached to the node they were tried from.

**Not done.** DGM keeps every variant alive and can resume any of them. This has
one working tree and one history, so it can move *up* its own lineage and not
sideways to a cousin — see the no-sideways-moves note in `archive/action.yml`.
That is a real reduction in what the search can reach, taken deliberately,
because restoring a cousin would make the record stop describing the files.

---

## Which node to grow from

**Huxley-Gödel Machine** — Wang et al., [arXiv:2510.21614][hgm]. Identifies the
*metaproductivity–performance mismatch*: the agent that scores best now is not
reliably the one whose descendants score best later, so expanding the current
best expands the wrong thing. Proposes **clade metaproductivity** (CMP) —
aggregate the performance of a node's whole lineage of descendants — and
Thompson-samples over it.

**Here.** `archive` computes CMP as the posterior mean of Beta(1+S, 1+F) over a
clade's successes and trials, and selects by Thompson sampling seeded from the
night's own identifier. The uniform prior is load-bearing: without it a node
with one adopted trial out of one reads 1.000 and beats nine-of-ten forever.
`reconsider` uses the same selection to decide whether to backtrack.

**Not done.** HGM decouples expansion from evaluation and runs them
asynchronously for parallelism. One night is one trial here, so there is nothing
to decouple. The evidence floor (six counted trials) means CMP does nothing at
all for the first week of a new repository, which is honest and also means the
mechanism is untested where it matters most.

---

## What evidence a self-modification is conditioned on

**Mendel Gödel Machine** — Liu et al., [arXiv:2608.07645][mgm]. Observes that
the archive is used only as a leaderboard for *sampling*, while the
self-modification step still looks at a single failure trajectory. Adds two
operators: **reaction-norm** (condition on one agent's failures across several
tasks — a recurring failure is a property of the genotype, not the task) and
**cross-lineage hybridisation** (condition on another lineage's attempt at the
same task).

**Here.** `draft` chooses between all three and records which it used in the
envelope and the certificate:

| operator | when | what the card carries |
|---|---|---|
| `cross-lineage` | another lineage was refused on this same milestone | its refusal, and "do not repeat it" |
| `reaction-norm` | this lineage was refused on ≥2 different targets | all of them, and "the problem is likely how it works" |
| `clonal` | neither | the last refusal on this target |

Cross-lineage is preferred, because it is the only one that transfers a
behaviour rather than repeating a search.

**Not done.** MGM's π-sampling allocates between evaluation and expansion under
a budget and proves a convergence result on an additive fitness landscape. The
policy here is three `if`s in priority order, chosen because it is inspectable,
not because it is optimal. Recording the operator is what would eventually let
the ledger say which one is worth doing; nothing reads that column yet.

---

## Changing the standard you are judged by

**Red Queen Gödel Machine** — Iacob et al., [arXiv:2606.26294][rqgm]. Existing
self-improvement assumes a stationary evaluator. Real evolution changes the
environment too. RQGM allows the utility to evolve, and makes it coherent by
**controlled utility evolution**: search runs in epochs, the criterion is fixed
*within* an epoch, and may change only at a boundary — so the improvement
guarantee holds per epoch.

**Here.** Every certificate carries `utility`, the digest of every file the
evaluator masks cover, and `epoch`. `ledger fsck` enforces three things as
properties of the record: entries within one epoch carry one utility digest,
epochs advance by exactly one, and only at a multiple of `epoch_len`. Without
those, two certificates are two different machines' opinions and nothing
downstream can tell.

`boundary` is the lane that changes the evaluator, and RQGM's adversarial
finding — that a naive judge over-accepts what it should refuse — is why
`boundary-judge` asks *Honest* (every disagreement must side with recorded
ground truth) rather than only *Moves*.

**Not done.** RQGM co-evolves the evaluator automatically, with an agent-as-judge
panel. Here an evaluator change is dispatched by a human, gated on archived
anchors, and lands as a pull request behind a protected environment needing a
second human. That is much weaker and much slower, and it is the right trade
when the artefact is somebody's actual repository.

---

## Not forgetting what you already caught

**HarnessEvolve** — [arXiv:2609.00829][he]. Self-evolving harnesses suffer
credit-assignment failure, shortcut learning, and catastrophic forgetting.
Proposes dual gating: a change must improve on what it targets *and* not
regress on what already worked.

**Here.** `boundary-judge`'s **Remembers** gate: every archived anchor the
current judge refuses and ground truth calls noise must still be refused by the
proposed one. *Honest* does not cover this — a proposal can be perfectly honest
about the anchors it moves and quietly lose a refusal it was already making,
because that anchor is not a disagreement in the direction Honest looks at.

**Not done.** No error clustering, and no reference trajectories. The anchor
stock accumulates automatically from every decided night, but the `ground` label
— *was this movement real or was it the weather* — is written by a human or not
at all. Unlabelled anchors abstain rather than vote, which is the conservative
choice and also means the gate is only as good as somebody's labelling.

---

## Naming what is actually happening

**Generalized Agent Iteration** — [arXiv:2609.13406][gai]. A framework putting
classical policy iteration and recursive self-improvement on one footing, with
two dials: *is the improving mechanism part of the agent*, and *is the standard
it is measured against grounded outside it*. The second dial sets the system's
**polarity**: anchored (the standard is external and fixed), goal drift (the
agent can rewrite it), or fully self-referential (no external standard).

**Where this sits.** Mostly **anchored**, deliberately. The standard is your
test suite, your benchmark and `goedel.toml`, and the ordinary lane cannot touch
any of them. `boundary` is a bounded excursion toward goal drift: the standard
can move, only at epoch boundaries, only through two human decisions, and only
when the move survives Moves, Honest and Remembers against evidence that
predates it.

This is the most useful thing in the reading list for deciding what *not* to
build. A fully self-referential loop is reachable from here in about fifty lines
— let `boundary` run unattended — and those fifty lines are the ones that
remove every reason to trust the record.

---

## Also read, and visibly not implemented

- **Gödel Agent** — [arXiv:2410.04444][ga]. Self-reference via runtime monkey
  patching. Elegant, and the wrong shape for something whose whole audit trail
  is a git history.
- **Live-SWE-agent** — [arXiv:2511.13646][live]. Evolves its scaffold *during* a
  task rather than between tasks. Nothing here changes mid-night.
- **SICA** — Robeyns et al., 2025. The minimal self-improving coding agent; the
  ancestor of the `draft`/`judge` split.
- **Self-Harness** — [arXiv:2606.09498][sh]. Harnesses that find their own
  failure modes and propose minimal fixes, validated by regression testing.
  This is what `boundary` would look like if the machine wrote the proposals;
  today a human does.
- **VeRO** — [arXiv:2602.22480][vero]. Versioned snapshots and controlled
  evaluation for agents optimising agents. The certificate is a thinner version
  of the same instinct.
- **What Do Evolutionary Coding Agents Evolve?** — [arXiv:2605.20086][what].
  Most gains come from a few edit types, and code gets re-introduced after being
  removed. The `kind` and `operator` columns exist so that this question is
  answerable about your repository; nothing answers it yet.

---

## Honest summary

| idea | state here |
|---|---|
| archive as a lineage tree | implemented |
| clade metaproductivity, Thompson selection | implemented, untested below six trials |
| three conditioning operators | implemented, chosen by a fixed priority |
| epoch-scoped utility | implemented and enforced by fsck |
| adversarial / forgetting gates on evaluator change | implemented, human-labelled evidence |
| paired comparison with FDR control | implemented |
| proof of improvement | **not attempted** |
| sideways moves in the archive | **not possible** by construction |
| automatic evaluator co-evolution | **deliberately not done** |

[dgm]: https://arxiv.org/abs/2505.22954
[hgm]: https://arxiv.org/abs/2510.21614
[mgm]: https://arxiv.org/abs/2608.07645
[rqgm]: https://arxiv.org/abs/2606.26294
[he]: https://arxiv.org/abs/2609.00829
[gai]: https://arxiv.org/abs/2609.13406
[ga]: https://arxiv.org/abs/2410.04444
[live]: https://arxiv.org/abs/2511.13646
[sh]: https://arxiv.org/abs/2606.09498
[vero]: https://arxiv.org/abs/2602.22480
[what]: https://arxiv.org/abs/2605.20086
