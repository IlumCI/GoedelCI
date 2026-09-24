# GoedelCI

The CI half of GLaDOS's self-improvement loop, copied here verbatim from
[IlumCI/GLaDOS](https://github.com/IlumCI/GLaDOS)'s `.github/`.

Fifteen workflows, two composite actions and the operator's ruleset notes — 5,317
lines. Nothing has been edited: this is the folder as it stands in the kernel
repository at the commit it was taken from.

## What is here

| | |
|---|---|
| `ci.yml` | builds the kernel and boots it; the gate `main` requires |
| `loop-night.yml` | the nightly cycle — follow, reconsider, propose, judge, adopt |
| `loop-judge.yml` | the two-arm gate a candidate goes through; holds no secrets |
| `loop-proof.yml` | the Phase-1 exit proof: four drills that must fail correctly |
| `boundary.yml` | the only lane that may change the evaluator itself |
| `propose.yml` | applies a machine-authored patch, builds both arms, signs a verdict |
| `evidence-boot/floors/fuzz/sweep` | four evidence factories that produce data and never verdicts |
| `release.yml` | tagged releases: sign, publish, build the ISOs |
| `experimental.yml` | non-release builds into the private channel |
| `site.yml` | regenerates the derived half of `docs/` |
| `pool.yml` | enforces the `#[path]` sharing between `pool/` and the kernel |
| `probe-kvm.yml` | temporary: settles whether the runners have KVM |
| `actions/kvm`, `actions/verify-boot` | the composite actions the above depend on |
| `RULESETS.md` | the branch protections an operator applies by hand |

## They will not work here yet, and that is worth saying plainly

Every one of these expects the kernel's source tree — `Cargo.toml`, `src/`,
`tools/`, `pool/`, `loop/` — and this repository has none of it. So they are
present and live but cannot pass.

What actually fires:

- **`ci.yml`** on any push to `main`, and it fails at the build.
- **Six on a schedule**: `evidence-boot`, `evidence-floors`, `evidence-fuzz`,
  `evidence-sweep`, `loop-night` and `site`. All fail.
- **Nothing else.** `release.yml` filters on `v*` tags, `experimental.yml` on
  `exp/**` branches, `pool.yml` on `pool/**` paths, and the rest are
  `workflow_dispatch` only.

None of them can do damage: they have no secrets here, and the ones that write
(`site.yml`, `loop-night.yml`) fail long before they reach a commit.

## What it would take to make them run

The same shape [IlumCI/glados-pool](https://github.com/IlumCI/glados-pool) uses
for the share audit: check the kernel out rather than copy it.

```yaml
- uses: actions/checkout@v4
  with:
    repository: IlumCI/GLaDOS
    path: glados
```

GLaDOS is public, so that needs no token. Every step then wants a
`working-directory: glados`, and the paths inside `loop-night.yml` and
`loop-judge.yml` — which reach for `loop/ledger/`, `tools/godel.py` and the
`loop/*` branches — need deciding: whether the loop's own ledger lives here or
stays there. That is a real decision rather than a rename, because the ledger's
branch is the loop's memory and two copies of it would be two accounts of one
history.

The secrets are the other half. `propose.yml` wants `VERDICT_SIGNING_KEY` and
`release.yml` wants `UPDATE_SIGNING_KEY`, and **the reason they are separate keys
is exactly the reason to think before copying them here**: `release.yml` ships a
kernel to every machine in the field and is reached by pushing a tag, while
`propose.yml` is reachable by any allowlisted device. One key for both would put
the key that ships kernels into a workflow a machine in the field can start.

## Status

Copied, not adapted. Nothing in this repository has ever passed.
