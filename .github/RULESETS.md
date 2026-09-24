# The protections this assumes, applied by hand

Everything in code refuses; these are the walls GitHub itself holds up. Apply
them after the first push and before the first schedule.

Settings → Rules → Rulesets, or `gh api /repos/:owner/:repo/rulesets`.

---

## Ruleset `main` — branch `main` (or your default)

- Require a pull request before merging.
- Required status checks: **`ci / machine`**, **`ci / project`**,
  **`proof / ledger`**, **`proof / drill (pass)`** and **`proof / drill (fail)`**.

`proof` is required and not optional. It is the only thing that checks the
seams between the actions rather than each one alone, and the only thing that
checks the claims the epoch rules make about a *sequence* of certificates —
which no single night can. Every bug that has actually shipped here lived in
one of those two places.
- Block force pushes. Restrict deletions.

The loop's token never pushes your default branch anyway — the audit pull
request is its only path there — but a wall that exists only in a token's habits
is a comment.

## Ruleset `loop` — branch `loop/**`

- Block force pushes. Restrict deletions.

Fast-forward-only is constructed by the `loop-main` concurrency group plus
`adopt`'s index plumbing. This ruleset is the backstop against a human hand
doing history surgery on the ledger by accident, which would break `fsck` for
good: sequence numbers are a permutation of `1..N`, and a rebase does not
preserve that.

## Ruleset `boundary` — branch `boundary/**`

- Block force pushes. Restrict deletions.

---

## Restrict who may write the machine

If your plan supports file-path rules:

- Restrict file paths **`.github/**`** for all non-admin actors.

Belt to braces. The loop's `GITHUB_TOKEN` already has no `workflows` write, so
GitHub rejects such a push at the token layer; this covers every other
non-admin credential too.

---

## Actions may open a pull request

**Settings → Actions → General → Allow GitHub Actions to create and approve pull
requests.**

Off by default, and `adopt`'s last step fails on it with

```
GraphQL: GitHub Actions is not permitted to create or approve pull requests
(createPullRequest)
```

*after* everything else in the night has already succeeded — the certificate
filed, `loop/main` pushed, the candidate ref tidied. So the symptom is a red
square on a night that worked, which is the shape that gets ignored.

**It does not widen what the loop may do**, which is why it is safe to grant.
The audit pull request is the machine's *only* path to your default branch, and
a pull request is a request: the token still has no `workflows` write, the
branch is still protected, and merging is still your decision. Withholding this
does not contain the loop, it silences it — the work keeps happening on
`loop/main` and stops being offered to anybody.

The "approve" half of the setting's name is GitHub's, not a grant to this loop.
Nothing here approves anything, and `boundary`'s write job still sits behind a
required reviewer.

---

## If you are running it autonomously

`[loop] autonomous = true` means a night that gets past the judge asks GitHub
to merge its own pull request. Two settings make that work, and one of them is
the difference between removing the human and removing the gate.

- **Settings → General → Allow auto-merge.** Without it the loop says so in a
  warning and the adoption sits in the pull request waiting for somebody.
- **Keep the required status checks above.** Auto-merge lands the change *when
  its checks pass*, so `ci` still re-verifies every adoption on a job the loop
  does not control, and a red one leaves the request open rather than merging
  it. This is why the loop asks for auto-merge rather than pushing to your
  default branch directly: a direct push would work and would also walk past
  every gate you configured.

  Required checks are what makes this real, and not only as policy. A push
  made with `GITHUB_TOKEN` does not trigger a workflow, so the night asks for
  its own `ci` run by dispatch -- and a required check that has not reported
  yet holds auto-merge open until it does. With no required checks configured,
  auto-merge lands the adoption the moment GitHub considers the branch
  mergeable, which may be before anything has looked at it.

What is removed is the waiting. What is kept is the checking.

Two further things are worth setting before you walk away:

- **`[harness] verify` must exercise the built thing.** `config` refuses to
  load with autonomy on and no verify command, because unit tests do not know
  whether the product still runs — every function in a site that 500s on every
  route still passes.
- **`[loop] give_up_after`.** After that many consecutive nights adopting
  nothing, the loop stands down instead of spending a runner a night forever
  on a milestone it cannot write. Zero means never.

## The `direction` label

`directions` opens competing pull requests carrying that label, and
`decided.yml` closes the losers when one is merged. Two things make it work:

- **The label makes itself.** `directions` creates it if it is not there,
  before it pushes anything, because `gh pr create --label` fails on a missing
  label *after* the branch exists -- which leaves orphan branches and half a
  set of alternatives. Nothing to do here.
- **Do not add `direction` to any auto-merge rule.** The promotion job already
  refuses to touch them — it merges only the audit pull request, selected by
  head branch — but a repository-level automerge rule would go around that and
  let the machine choose its own objective, which is the one thing this whole
  arrangement exists to prevent.

`decided.yml` runs on `pull_request_target`, which executes the *base*
branch's workflow rather than the merged head's. That is what makes it safe to
give it write permission: nothing from the merged branch runs.

## Environment `evaluator`

Only needed once you intend to use the `boundary` lane.

- **Required reviewer:** you.
- **Secret `EVALUATOR_TOKEN`:** a fine-grained PAT, this repository only,
  permissions `contents: write` + `workflows: write` + `pull requests: write`.

It exists nowhere else, and `boundary`'s write job cannot start — the secret
does not resolve — until a human approves the run. That is the first of the two
human decisions; merging the pull request it opens is the second.

---

## The whole secret surface

| where | name | held by | why |
|---|---|---|---|
| repository secret | `GOEDEL_INFERENCE_KEY` | `loop-night` (`plan`, `draft`) | the only credential the nightly loop needs |
| repository variable | `GOEDEL_INFERENCE_URL` | the same | only for a non-default endpoint |
| environment `evaluator` | `EVALUATOR_TOKEN` | `boundary`'s write job only | may write `.github/**`; gated on a human |

**`loop-judge` holds no secrets at all** and asks for `contents: read`. It is
the job that builds and runs candidate code, so it is the one least entitled to
authority. Everything it produces is an artifact, and a verdict becomes real
only when `adopt` — which never runs candidate code — commits it.

`ci`, `proof` and `floors` need nothing.

---

## A note on what this does and does not contain

The token boundary and the branch protections stop the loop reaching your
default branch or the machine's own code. They do not stop it doing something
silly *inside* `allow` — that is what the judge is for, and the judge is code
that can be wrong.

The things actually standing between this and a bad night are, in order of how
much work they do:

1. the counts that may not fall, checked in the certificate format itself;
2. the candidate's own tests having to pass;
3. the path masks, checked against the diff rather than the declaration;
4. the diff budget per kind;
5. you, reading the audit pull request before you merge it.

The fifth one is not optional, and the first four exist to make it cheap.
