# FDA SaMD Toolkit Success Metrics

This document defines how we measure success for the FDA SaMD Toolkit, distinguishing between input metrics (leading indicators), output metrics (lagging indicators), and the single north-star metric.

## North Star Metric

**Real FDA 510(k) submissions where the toolkit is cited in the design history file (DHF) by end of 2026.**

Target: 3+ real submissions cite the toolkit in their design history file or submission package by EOY 2026.

### Why This Metric

1. **Proxy for real product-market fit.** Downloads and GitHub stars measure attention; a company's decision to cite the toolkit in a formal FDA submission measures conviction that the toolkit solved an acute problem.
2. **Irreversible signal.** Once cited in an FDA submission, the toolkit becomes part of regulatory history for that device. This is not a vanity metric that can be gamed.
3. **Moves the needle on broader adoption.** Each real submission creates a case study, attracts similar companies, and generates social proof in the regulatory community.
4. **Directly aligns with consultant persona value.** If regulatory consultants see companies using the toolkit successfully, they become advocates.
5. **Non-obvious to game.** You can't buy citations or artificially inflate them without real implementation work.

---

## Leading Indicators (Input Metrics)

These measure activity, engagement, and pipeline health. Leading indicators help us course-correct early.

### GitHub Activity

| Metric | 3-month target | 6-month target | 12-month target | Data source | Collection method | Cadence |
|--------|---|---|---|---|---|---|
| GitHub stars | 200 | 500 | 1,200 | GitHub API | `curl https://api.github.com/repos/lal-jaouni/fda-samd-toolkit` (`.stargazers_count`) | Weekly (automated) |
| GitHub forks | 30 | 80 | 200 | GitHub API | Same endpoint (`.forks_count`) | Weekly (automated) |
| Open issues | 15+ | 25+ | 40+ | GitHub API | `curl https://api.github.com/repos/lal-jaouni/fda-samd-toolkit/issues?state=open` | Weekly (automated) |
| Pull requests merged | 12+ | 30+ | 80+ | GitHub API | PRs merged to master branch | Weekly (automated) |
| External contributors | 2+ | 5+ | 15+ | GitHub API | Unique authors of merged PRs, excluding maintainer | Weekly (automated) |
| Release cadence | v0.2 shipped | v0.3 shipped | v1.0 stable | GitHub releases | Releases page | Manual review |

**Success bar:** By 6 months, >300 stars and >2 external contributors signals healthy open-source adoption.

### Package Distribution

| Metric | 3-month target | 6-month target | 12-month target | Data source | Collection method | Cadence |
|--------|---|---|---|---|---|---|
| PyPI downloads/month | 500 | 1,500 | 5,000 | PyPI Stats | https://pypistats.org/packages/fda-samd-toolkit | Weekly (automated) |
| PyPI download growth rate | Month-over-month increase | Sustained >20% MoM | Peak post-release spikes | PyPI Stats | Same tool, trending | Weekly |

**Success bar:** By 12 months, 5,000+ monthly downloads. (Context: projects with 500+ DownloadedDocs stars typically see 1,000-3,000 monthly downloads; we're aiming above median.)

### Content Engagement

| Metric | 3-month target | 6-month target | 12-month target | Data source | Collection method | Cadence |
|---|---|---|---|---|---|---|
| Documentation page views | 2,000 | 6,000 | 20,000 | MkDocs Material (with analytics) | Google Analytics on docs site (if enabled) or server logs | Weekly (automated) |
| Blog post views (if published) | 1,000 | 3,000 | 10,000 | Blog platform (Medium, Substack, or personal site) | Platform analytics | Weekly |
| Links to toolkit in external blogs/articles | 3+ | 8+ | 20+ | Manual search + Google Alerts | Search "fda-samd-toolkit" on Google, GitHub search for issues linking toolkit | Monthly (manual) |

**Success bar:** By 6 months, >3 credible external links (from healthcare/regulatory blogs, investor sites, FDA observer sites) indicate traction beyond founder network.

### Community Signals

| Metric | 3-month target | 6-month target | 12-month target | Data source | Collection method | Cadence |
|---|---|---|---|---|---|---|
| Hacker News upvotes (if launched) | 100+ | N/A | N/A | HN API | Post ranked top 30 on HN | One-time (day of launch) |
| Reddit mentions (r/MachineLearning, r/healthcare, r/FDA) | 2+ | 5+ | 15+ | Reddit API or manual search | reddit.com site search, Reddit scraper | Monthly (manual) |
| Slack/Discord community messages | N/A (not planned v0.2) | TBD | 50+ monthly | Community platform analytics | If Slack workspace created | N/A until launched |
| Twitter/LinkedIn mentions | 5+ | 15+ | 50+ | Twitter API or manual search | Twitter search "fda-samd-toolkit", LinkedIn posts | Weekly (manual) |

**Success bar:** By 6 months, mentions in 2-3 regulatory or healthcare tech communities indicate credibility.

---

## Lagging Indicators (Outcome Metrics)

These measure real-world impact and prove product-market fit. They lag by weeks or months.

### Adoption by Real Companies

| Metric | 3-month target | 6-month target | 12-month target | Data source | Collection method | Cadence |
|---|---|---|---|---|---|---|
| Known companies using toolkit | 0 | 2+ | 5+ | User feedback, GitHub discussions, consulting outreach | User interviews, GitHub "Discussions" feature, inbound inquiries | Monthly (manual) |
| Real 510(k) submissions citing toolkit | 0 | 1+ | 3+ | FDA CBER/CDRH submissions (via eSTAR or DHF), company outreach | Direct company feedback, FDA submission search, toolkit citations in design history files | Quarterly (manual) |
| Regulatory consultant partnerships | 0 | 1+ | 3+ | Consulting inquiries, joint case studies | Inbound inquiries, explicit partnership agreements | Quarterly (manual) |

**Success bar:** North-star metric achieved = 3+ real submissions by EOY 2026.

### Professional Recognition

| Metric | 3-month target | 6-month target | 12-month target | Data source | Collection method | Cadence |
|---|---|---|---|---|---|---|
| Academic/professional paper citations | 0 | 0+ | 2+ | Google Scholar, ResearchGate | Google Scholar search for "fda-samd-toolkit", paper cross-references | Quarterly (manual) |
| Regulatory conference talks (RAPS, FDA AI Council, etc.) | 0 | 1+ | 2+ | Conference websites (RAPS annual meeting, FDA AI Council sessions), LinkedIn | Call for papers tracking, inbound speaking requests | Quarterly (manual) |
| Case studies published (with company permission) | 0 | 1+ | 2+ | Blog, Medium, toolkit documentation | User interviews, published case studies | Quarterly (manual) |

**Success bar:** By 12 months, 1+ conference talk and 1+ peer-reviewed mention indicate credibility in regulatory/healthcare AI circles.

### Revenue Signals (If Applicable)

| Metric | 3-month target | 6-month target | 12-month target | Data source | Collection method | Cadence |
|---|---|---|---|---|---|---|
| Consulting inquiries citing toolkit | 0 | 2+ | 10+ | Inbound email, LinkedIn | Direct inbound, tracked in CRM | Monthly (manual) |
| Productized service launches based on toolkit | 0 | 0+ | 1+ | Custom service offerings, productized workshops | Consulting engagements that started as toolkit users | Quarterly (manual) |

**Success bar:** By 12 months, 10+ inbound consulting inquiries from companies who discovered toolkit independently (not direct outreach).

---

## Anti-Metrics (What NOT to Optimize)

These metrics look good but don't indicate real success. Avoid over-optimizing these.

1. **GitHub stars from viral HN post** without sustained interest (stars spike to 300 in week 1, then flatline at 320 by month 3). Real adoption shows steady growth.

2. **Downloads from CI bots and automated scanners** that pull the package but never use it. (PyPI tracks intentional installs; we trust PyPI data but monitor for anomalies like 1,000 downloads in a single IP.)

3. **Comments on issues from people who don't actually use the toolkit** (e.g., feature requests based on blog posts they read, not actual pain points).

4. **Links to toolkit in spam blogs or SEO-farming sites.** Track only links from credible healthcare, regulatory, or AI sources.

5. **Documentation page views from bots.** (Discount bot traffic; rely on Google Analytics "Engaged sessions" not raw pageviews.)

6. **"Launches" on multiple platforms (Product Hunt, Hacker News, Dev.to, etc.) without substance.** One launch on HN is valuable; launching the same project on 5 platforms is false momentum.

---

## How to Instrument These Metrics

### GitHub Metrics (Automated)

Create a GitHub Actions workflow (`.github/workflows/metrics.yml`) that runs weekly:

```bash
curl -s https://api.github.com/repos/lal-jaouni/fda-samd-toolkit \
  | jq '.stargazers_count, .forks_count, .open_issues_count' \
  > metrics/github-$(date +%Y-%m-%d).json
```

Store results in a `metrics/` directory, commit weekly. Generate a simple dashboard from this data.

### PyPI Metrics (Manual or Automated)

Weekly check: `https://pypistats.org/packages/fda-samd-toolkit`

Or use the pypistats API:
```bash
curl https://pypistats.org/api/packages/fda-samd-toolkit/recent?period=month \
  | jq '.data' > metrics/pypi-$(date +%Y-%m-%d).json
```

### Documentation Metrics

If using MkDocs Material:
- Add Google Analytics to `mkdocs.yml` (requires Google Analytics setup)
- Or parse server logs if self-hosted
- Baseline: expect ~500-1000 pageviews/month at launch

### Adoption Metrics (Manual)

Quarterly check-in:
- Search GitHub for repos forking and citing the toolkit
- Query GitHub Discussions for user stories
- Reach out to known users (Tier 1 consulting candidates) for quotes
- Search FDA CBER/CDRH websites for submissions citing the toolkit (manual or via FOIA if needed)

### Social / Community Metrics (Manual)

Monthly:
- Google Alerts for "fda-samd-toolkit" + relevant keywords
- Reddit search across healthcare/ML/FDA subreddits
- Twitter/LinkedIn search

---

## Reporting Cadence

1. **Weekly**: GitHub activity, PyPI downloads (automated dashboard)
2. **Monthly**: Community mentions, social signals (manual)
3. **Quarterly**: Adoption stories, consulting inquiries, professional recognition (manual interview + search)
4. **Annually**: v1.0 retrospective, full goal scorecard

---

## Success Milestones (Timeline)

| Milestone | Timeline | Metrics |
|-----------|----------|---------|
| **v0.2 launch buzz** | End of May 2026 | 100+ GitHub stars, 200+ PyPI downloads (first month) |
| **Sustained adoption** | End of Q2 2026 | 300+ stars, 500+ monthly downloads, 2+ external contributors |
| **First real user story** | Q3 2026 (by Sept 30) | 1+ company confirms using toolkit in real submission |
| **Regulatory community traction** | Q4 2026 | 1+ conference talk, 3+ external links from credible sources |
| **North-star achieved** | EOY 2026 | 3+ real 510(k) submissions cite toolkit in design history |

---

## Decision Framework

**When to prioritize v0.3 features:** If north-star metric is on track (1+ real submission by mid-2026), continue momentum with v0.3. If north-star is at risk, shift focus to marketing and adoption enablement.

**When to declare success:** Toolkit is successful if EOY 2026 shows 3+ real submissions, 5+ known users, and 1+ regulatory consulting partnership. This proves product-market fit in the core use case (primary persona: AI/ML startup CTO).

**When to declare failure:** If by Q4 2026, north-star metric is 0 (no real submissions citing toolkit), despite 5+ external features shipped and 500+ stars, the toolkit may be solving a nice-to-have rather than a must-have. Pivot to secondary use case (consultant partners) or reassess problem fit.
