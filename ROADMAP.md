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

## v0.1: Shipped (April 2026)

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

## v0.2: Planned

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

## v0.3+ Candidates

Features identified in [`research/must_use_features.md`](research/must_use_features.md)
that did not make the v0.2 cut but remain on the table for v0.3 and beyond. Effort
labels follow the same S/M/L/XL scale used in the research doc. Not a commitment,
a backlog.

| Rank | Candidate | Effort | Source | Notes |
|---|---|---|---|---|
| 1 | Imaging AI clinical validation worked example (CT/MRI/X-ray, e.g. K201439 Caption Health dissection) | M | research Big Bets | Unlocks v1.0 device class 2 |
| 2 | NLP/EHR AI clinical validation worked example (clinical note summarization, risk prediction) | M | research Big Bets | Unlocks v1.0 device class 3 |
| 3 | GMLP evidence template mapping all 10 IMDRF principles to toolkit outputs | M | Jan 2025 FDA guidance | Reviewers directly ask for this |
| 4 | Regulatory intelligence auto-ingest (pull FDA guidance changes into templates via `market-intel` collectors) | L | must-use research | Pulls from existing FDA monitoring pipeline on this VM |
| 5 | Predicate device discovery helper (openFDA API + substantial equivalence scoring) | M | research Quick Wins | Reduces predicate search from hours to minutes |
| 6 | Cybersecurity threat modeling (beyond the SBOM in #14: STRIDE, attack surface, mitigation templates) | M | June 2025 FDA cybersecurity guidance | Natural extension of v0.2 SBOM work |
| 7 | Post-market performance monitoring dashboard (extends #16 with Grafana/Streamlit example) | L | research Big Bets | Stretch goal, depends on #16 landing |
| 8 | IEC 62366 usability engineering scaffolding (summative evaluation, use errors, risk analysis) | L | IEC standard | Adjacent standard many reviewers ask for |
| 9 | De Novo pathway support (first-of-a-kind devices, alternative to 510(k) substantial equivalence) | XL | FDA guidance | Currently out of v1.0 scope per `docs/product/scope.md` |
| 10 | CLI-first real cleared device dissection tool (ingest public 510(k) summaries, compare to generated output) | L | research Community Strategy | Builds social proof via "we match real clearances" |

Each candidate will be evaluated against the decision rule in
[`docs/product/scope.md`](docs/product/scope.md) before it gets promoted to a
milestone: at least 50% of the three documented personas must benefit, it must be
covered by an FDA guidance document or standard we already implement, and it must
be implementable in under 30% of a release cycle's effort budget.

## How decisions get made

The product planning docs at [`docs/product/`](docs/product/) are the source of
truth for scope, priority, and quality bar decisions:

- **What we're building and why** → [`docs/product/personas.md`](docs/product/personas.md)
  and [`docs/positioning.md`](docs/positioning.md)
- **What success looks like** → [`docs/product/metrics.md`](docs/product/metrics.md)
  (north-star: 3+ real 510(k) submissions citing the toolkit by EOY 2026)
- **What we will and will not build** → [`docs/product/scope.md`](docs/product/scope.md)
- **When features ship** → [`docs/product/release-cadence.md`](docs/product/release-cadence.md)
- **What v1.0 means** → [`docs/product/v1.0-definition.md`](docs/product/v1.0-definition.md)
- **When a feature is done** → [`docs/product/definition-of-done.md`](docs/product/definition-of-done.md)
- **Quality bar per PR** → [`docs/quality.md`](docs/quality.md) and
  [`docs/qa-checklist.md`](docs/qa-checklist.md)

A scope-expansion request gets accepted if and only if it passes the decision rule
in `scope.md`. A v0.3+ candidate gets promoted to a milestone if it has a user
willing to try it, an FDA guidance reference, and a clear effort estimate. Everything
else goes in this backlog section.
