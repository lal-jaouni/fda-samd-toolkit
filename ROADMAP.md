# Roadmap

This file is the human-readable index for what's shipped, what's next, and how work
is tracked. It mirrors GitHub milestones and labels so contributors don't have to
click through the issues UI to see the picture.

## Tracking model

We use **two parallel tracking surfaces** so neither is a single point of failure:

| Surface | Purpose | How to filter |
|---|---|---|
| **Milestones** | Hard release boundaries (v0.1, v0.2, v0.3) | `is:issue milestone:v0.2` on GitHub |
| **Labels** | Cross-cutting tags that survive milestone changes | `is:issue label:must-use label:quick-win` |

The standard labels are:

| Label | Color | Meaning |
|---|---|---|
| `v0.1`, `v0.2`, ... | green / blue | Mirrors the milestone, lets you query without milestone access |
| `must-use` | red | Feature identified by user research as high-pull (people will adopt for this alone) |
| `quick-win` | yellow | Small effort, ships in under a week, creates immediate buzz |
| `big-bet` | purple | Larger effort, would make this a category-defining tool |
| `enhancement`, `bug`, `documentation` | default | Standard GitHub triage |

Why two surfaces? Milestones are the FDA-style binary "in this release / not in this
release" cut, but labels let us slice the backlog by *intent* (must-use vs nice-to-have)
across releases. If GitHub milestones break for any reason (scope perms, org transfer,
fork) the labels still tell the story.

## v0.1 — Shipped (April 2026)

All 8 issues closed and merged. See [milestone v0.1](https://github.com/lal-jaouni/fda-samd-toolkit/milestone/1).

- PCCP Generator with Pydantic schemas, Jinja templates, ECG and imaging examples
- 510(k) AI/ML Section Templates (7 sections: IFU, device description, substantial
  equivalence, performance testing, training data characterization, risk analysis,
  human factors)
- FDA-Extended Model Card Generator (Mitchell et al. 2019 plus FDA fields)
- Clinical Validation Framework with modality guidance (imaging, signals, NLP,
  multimodal)
- Submission Readiness Checklist (58 items across 8 categories)
- Click + Rich CLI with `pccp`, `templates`, `model-card`, `checklist` subcommands
- GitHub Actions CI matrix (Python 3.11, 3.12) and release workflow
- MkDocs Material documentation site with guides and references
- CardioGuard ECG-AI complete worked example tying everything together
- 157 passing tests

## v0.2 — Planned

See [milestone v0.2](https://github.com/lal-jaouni/fda-samd-toolkit/milestone/2). Features
will be added based on the must-use research report at `research/must_use_features.md`.

The bar for v0.2: every feature must either be a `must-use` (red label) backed by user
research, or a `quick-win` (yellow label) that ships in under a week.

## How to propose new work

1. Open an issue using one of the templates in `.github/ISSUE_TEMPLATE/`.
2. If you have evidence the feature is high-pull (job posting, FDA guidance, user
   complaint thread) link it in the issue body.
3. Add the milestone you're targeting and the relevant labels.
4. The maintainer will tag it `must-use` or `quick-win` if it qualifies.
