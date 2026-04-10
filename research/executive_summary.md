# Executive Summary: FDA SaMD Toolkit "Must-Use" Features

**Research Period:** April 6-10, 2026  
**Methods:** Internal FDA data mining + web research + competitor analysis + regulatory guidance review  
**Evidence Base:** FDA guidance (Dec 2024 PCCP, Jan 2025 AI/ML Lifecycle & GMLP, June 2025 Cybersecurity), 18 ranked AI/cardiac companies, 100+ research sources, real clearance examples (Anumana, Eko, Innolitics K232613)

## The Finding

The FDA SaMD Toolkit can become irresistible by building 5 features that solve the most acute pain points regulatory teams face. Evidence shows these features are:
1. **Mandatory** (eSTAR Oct 2023, SBOM June 2025, bias Jan 2025)
2. **Expensive to outsource** ($5-16K per feature via consultants)
3. **Missing from open source** (no competing tool covers all 5)
4. **Directly requestable by target users** (Cardiosense, Salomatic, Anumana, Eko all actively hiring RA staff; 18 ranked companies have $50M+ consulting pipeline)

## Top 5 Features (Ranked by Pull)

| Rank | Feature | Pull | Effort | Why Build | Blocker? |
|------|---------|------|--------|-----------|----------|
| 1 | **eSTAR Package Builder** | 8/10 | 2 wks | Auto-generate FDA submission package in mandatory eSTAR format (required Oct 2023). Consultant cost: $3-8K. Saves 1-2 weeks. | Reverse-engineer eSTAR PDF structure |
| 2 | **Cybersecurity SBOM Generator** | 8/10 | 1 wk | Generate machine-readable SBOM (NTIA format) now mandatory per June 2025 FDA guidance. No open-source tool exists. | Define component schema |
| 3 | **Bias Evaluation Report** | 7/10 | 1 wk | Jan 2025 FDA guidance requires demographic bias analysis (race/ethnicity/sex/age). No template exists. Consultant cost: $8-15K. | Pydantic schema + Jinja template |
| 4 | **Real-World Monitoring Plan** | 7/10 | 1 wk | FDA soliciting input on post-market AI monitoring (critical for PCCP approval). Companies have no standard approach. | Define metrics, thresholds, escalation |
| 5 | **IEC 62304 Integration** | 6/10 | 2 wks | Fold in OpenRegulatory MIT-licensed software lifecycle templates to complete submission scaffold (currently missing). | License check + integrate workflow |

## Quick Wins (Next 2 Weeks)

Implement features 2-4 immediately (total ~4-6 hrs each):
- Bias Evaluation Generator: YAML input -> markdown report
- Training Data Characterization: Demographics + splits + representativeness argument
- Post-Market Monitoring Plan: Data sources + metrics + drift triggers + rollback procedures
- Update CardioGuard example to show full workflow

**Expected impact:** +50-100 GitHub stars, 2-3 consultant inquiries, regulatory community buzz.

## Big Bets (Next 1-3 Months)

1. **eSTAR Package Builder** (2 weeks) -- Only open-source tool doing this; positions toolkit as alternative to Cruxi ($2-5K/submission)
2. **Regulatory Intelligence Ingestion** (2 weeks) -- Auto-update toolkit when FDA guidance changes; living document advantage
3. **GMLP End-to-End** (2 weeks) -- Map 10 GMLP principles to toolkit generators; position as "FDA expects this"

## Distribution

- **Launch channels:** Hacker News, r/MachineLearning, Product Hunt, RAPS conference 2026
- **Target users:** AI/ML startup CTOs (8 weeks before submission), regulatory directors (evaluating tools), consultants (productizing deliverables)
- **Success metrics:** 500+ GitHub stars (3 months), 1-2 public company adopters, 2-3 consultant partnerships

## Why This Wins

**Open source:** No per-seat, per-submission, or SaaS costs. Companies control their docs.  
**Regulatory authority:** Built on actual FDA guidance (not consultant opinions). Auto-updates when guidance changes.  
**Speed:** Generates regulatory scaffolding in hours, not weeks. Users spend time on science, not paperwork.  
**Complete:** Only tool covering PCCP (Dec 2024) + GMLP (Jan 2025) + AI/ML Lifecycle (Jan 2025) + Cybersecurity (June 2025) + IEC 62304 + ISO 14971 in one unified workflow.

## Investment

- **Time:** ~50-60 hours over 12 weeks (quick wins 4 wks, eSTAR 2 wks, integration/misc 2 wks)
- **Revenue potential:** Consulting ($500-2K per custom implementation), corporate licenses (for internal tool customization), conference speaking gigs
- **Market size:** 18 ranked target companies + 100+ smaller AI/medical device startups filing 510(k)s annually

---

*Full analysis at: /home/laith/workspaces/fda-samd-toolkit/research/must_use_features.md*
