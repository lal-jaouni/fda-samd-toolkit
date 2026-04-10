# Human Factors and Usability Engineering for AI/ML Medical Devices

## Overview
For AI/ML devices, human factors engineering focuses on:
1. How clinicians interact with AI output
2. Risk of misinterpretation or over-reliance
3. Alert fatigue and workflow integration
4. Training requirements to use safely

Unlike traditional devices, AI risks are often at the human-computer interface: a perfect model
can cause harm if presented confusingly or integrated into workflows poorly.

**FDA Guidance:** Demonstrate that physicians can use the device safely and effectively without
formal training (or document training requirements). Usability testing with representative users is expected.

---

## Template

## 1. Intended User and Use Environment

### 1.1 Intended User Profile

Who will use this device? What is their training and expertise?

[INSERT: User characterization]

Example: "**Intended Users:**

Primary Users:
- Cardiologists (MD or DO with cardiology fellowship training)
- Interventional cardiologists
- Cardiac electrophysiologists
- Physicians' assistants in cardiology (require supervision by cardiologist)
- Nurse practitioners in cardiology (require supervision by cardiologist)
- Cardiac nurses (operate device under physician direction)
- Cardiac technicians/ECG technicians (trained on device, report results to physician)

User Training and Qualifications:
- All users must have formal training in ECG interpretation (minimum: 3-month clinical rotation)
- Clinical cardiology training: Minimum 1 year for independent interpretation
- For device-assisted interpretation: Minimum 15-minute training on device output format (see Section 2)
- No requirement for advanced ML knowledge or computer science background

Typical User Environment:
- Hospital ECG monitoring area, cardiology clinics, emergency departments
- Users are working under time pressure (ED: high volume, fast throughput)
- Users have multiple competing tasks; device should not require sustained attention
- Users may be fatigued, especially overnight/weekend shifts; interface must be robust to inattention

Typical User Characteristics (from user research):
- Age: 30-65 years (mostly 40-55)
- Tech comfort: Variable; some very comfortable with software, others minimal computer use
- Domain expertise: All have minimum 3+ years ECG experience; many have 10+ years
- Reading speed: Cardiologists read 40-100 ECGs per shift; device must not slow workflow
- Decision confidence: 70% of physicians report high confidence in their ECG interpretations;
  AI may be perceived as threatening to expert identity"

---

### 1.2 Use Environment

Where and how will the device actually be used?

[INSERT: Operational environment]

Example: "**Physical and Operational Environment:**

Hospital Settings:
- Emergency Departments: High-volume (200-500 ECGs/day), time-pressure (need results in <10 min),
  low documentation quality (handwritten notes, sometimes illegible)
- Cardiology Departments: Medium volume (50-200 ECGs/day), high expertise, good documentation
- Intensive Care Units: Lower volume but sicker patients, continuous monitoring

Clinical Workflow:
1. ECG acquired on patient monitor or ECG cart
2. Transmitted via HL7 to device (cloud or local server)
3. AI analysis (~150 ms)
4. Result displayed in EHR or standalone interface
5. Physician reviews AI output + original ECG
6. Physician makes final interpretation (accept, reject, or modify AI)
7. Final interpretation documented in medical record

Typical Use Duration: <2 minutes per ECG (device adds ~30-60 seconds to manual interpretation workflow)

Display Format:
- Primary: EHR embedded result (structured report)
- Secondary: Standalone web interface (for research/audit)
- Mobile: iPad/tablet access (clinical staff review results on the go)

Accessibility Constraints:
- Screen size: Must be readable on 13-inch laptop to 27-inch desktop monitor
- Color blindness: Color-coding must not rely on color alone (use shape/text labels too)
- Language: English primary; Spanish translation planned for future
- Accessibility: WCAG 2.1 AA compliant (keyboard navigation, screen reader compatible)"

---

## 2. Output Format and Presentation

### 2.1 Device Output Display

How is the AI result presented to the physician?

[INSERT: Output display design]

Example: "**Clinical Report Format:**

**Primary Display (EHR-embedded):**

```
┌─────────────────────────────────────────────────────────────────┐
│ CARDIODETECT AI - Atrial Fibrillation Probability               │
├─────────────────────────────────────────────────────────────────┤
│ Patient: John Doe | MRN: 12345 | Age: 72, Male                 │
│ ECG Date/Time: 2024-03-15 14:23 | Lead: 12-lead                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  PRIMARY FINDING:                                                │
│  ┌───────────────────────────────────────────────────┐           │
│  │ ATRIAL FIBRILLATION LIKELY PRESENT                │           │
│  │ Probability: 87% (95% CI: 83-91%)                │           │
│  │ Confidence: HIGH                                  │           │
│  └───────────────────────────────────────────────────┘           │
│                                                                   │
│  SECONDARY FINDINGS:                                             │
│  - Heart Rate: 112 BPM (tachycardia)                            │
│  - Artifact Level: 8% (acceptable)                              │
│                                                                   │
│  DIAGNOSTIC INTERPRETATION:                                      │
│  Regular sinus rhythm with prominent irregular baseline and       │
│  variable RR intervals consistent with atrial fibrillation.      │
│  Rate approximately 110-115. Recommend correlation with          │
│  clinical presentation.                                          │
│                                                                   │
│  RECOMMENDATION:                                                  │
│  Consider: (1) Urgent cardiology evaluation                      │
│           (2) Rate/rhythm control assessment                     │
│           (3) Anticoagulation evaluation                         │
│                                                                   │
│  LIMITATIONS:                                                     │
│  This is a clinical decision support tool. Interpretation by     │
│  a qualified clinician is required. Device should not be used    │
│  as sole basis for diagnosis or treatment decisions.             │
│                                                                   │
│  [View Original ECG] [View Explanation] [Mark as Reviewed]      │
│  Reviewed by: Dr. Jane Smith | 2024-03-15 14:25                │
│  Status: Final                                                   │
├─────────────────────────────────────────────────────────────────┤
│ Generated by CardioDetect AI v1.2.1 | Model ID: ECG-AF-20240101 │
│ Not a diagnostic statement. Physician interpretation required.   │
└─────────────────────────────────────────────────────────────────┘
```

**Design Rationale:**

- Color coding: Red background for AF-likely (alerts physician), green for normal (reassuring)
- Probabilistic not binary: Displays percentage rather than 'positive/negative' to convey uncertainty
- Confidence explicitly stated: 'HIGH/MEDIUM/LOW' helps physician gauge reliance
- 95% CI provided: Clinician sees uncertainty range, not false precision
- Original ECG link: Single click to compare AI interpretation with human-readable waveform
- Explanation available: Link to saliency map showing which ECG features drove prediction
- Disclaimer prominent: Repeated statement that AI is decision support, not diagnosis
- Heart rate and artifact: Secondary findings relevant to interpretation
- Recommendation section: Actionable clinical guidance (not just 'AF likely')
- Timestamp and user: Audit trail showing who reviewed result and when

**Contrast and Readability:**
- Color contrast ratio >4.5:1 (WCAG AA compliant)
- Font size minimum 12pt (readable on typical hospital monitors)
- Sans-serif font (Helvetica, Arial) for clarity
- No text-only color differentiation (shape/icons used alongside color)"

---

### 2.2 Explanation and Transparency Features

Can the physician understand WHY the AI made its prediction?

[INSERT: Explainability features]

Example: "**Explanation Module:**

Available via 'View Explanation' link on clinical report.

**Feature Importance by ECG Lead (Saliency Map):**

```
Lead Contribution to AF Prediction:
┌─────────────────────────────────────────────────┐
│ Lead II     ████████░░ 78% (highest contribution)|
│ Lead III    ███████░░░ 67%                       │
│ Lead V1     ████████░░ 72%                       │
│ Lead aVL    ██░░░░░░░░  15% (low contribution)  │
│ Lead V2     ███░░░░░░░  28%                       │
│ [other leads: 10-30%]                            │
└─────────────────────────────────────────────────┘
```

**Interpretation for Clinician:**
- Leads II and III show the highest evidence for AF (irregular baseline, variable RR)
- Lead V1 also prominent (likely detecting RV rate variation)
- Lateral leads (aVL) show minimal evidence
- Interpretation: Model found irregular rhythm in inferior leads, consistent with clinical AF diagnosis

**Temporal Attention Map:**
- Highlights which 100-200 ms windows of the 10-second ECG drove the prediction
- Example: 'Windows 2.1-2.4 sec and 5.8-6.2 sec show maximum RR irregularity'
- Allows clinician to verify: Does highlighted region truly show AF?

**Confidence Justification:**
When confidence is moderate (60-80%), explanation shows:
- Which features support AF (saliency highlights)
- Which features argue against AF (model uncertainty in those features)
- Example: 'Lead II shows prominent irregular baseline (supports AF) but lead I shows some regularity (increases uncertainty)'

**Clinical Impact:**
- Explanation allows physician to audit AI reasoning
- Physician can override AI if explanation disagrees with clinical judgment
- Transparency reduces automation bias (physician is engaged in reasoning, not passive)

**Accessibility:**
- Explanation available in text form (for screen readers)
- Saliency maps also provided as numerical tables (for users who prefer data to visualization)
- Explanations written for cardiologists (medical jargon OK, but clear and jargon-free options provided)"

---

## 3. Workflow Integration and Safety

### 3.1 Override and Manual Review Mechanisms

Can the physician override the AI if they disagree?

[INSERT: Override workflow]

Example: "**Physician Override and Manual Review Process:**

**Scenario 1: Physician Agrees with AI**
1. Physician reviews ECG + AI report
2. AI output shows 'AF likely (confidence 87%)'
3. Physician manually verifies: yes, sees irregular baseline, no P waves
4. Physician clicks 'Agree with AI interpretation'
5. Result documented: 'Atrial fibrillation. AI-assisted diagnosis.'
6. Status: FINAL

**Scenario 2: Physician Disagrees with AI**
1. Physician reviews ECG + AI report
2. AI output shows 'AF likely (confidence 78%)'
3. Physician manually verifies: irregular rhythm but also sees artifact
4. Physician clicks 'Disagree - Enter Alternative Interpretation'
5. Popup form appears:
   - 'What rhythm do you see?' [dropdown: sinus, AF, atrial flutter, other]
   - 'Reason for disagreement:' [text field]
   - Example: 'High artifact level; underlying rhythm appears regular. Recommend repeat ECG.'
6. Physician enters: 'Sinus rhythm with artifact'
7. Result documented: 'Sinus rhythm. AI predicted AF but overridden based on clinical review.'
8. Status: FINAL (physician interpretation takes precedence)
9. System logs: Discrepancy recorded for QA audit
   - Physician name, timestamp, reasoning
   - Can later audit: Was override clinically appropriate?

**Scenario 3: Physician Uncertain - Requests Manual Review**
1. Physician reviews ECG + AI report
2. AI output shows 'Uncertain (confidence 55%)'
3. Report states: 'Manual Review Recommended'
4. Physician clicks 'Request Cardiology Consultation'
5. Case escalated to cardiologist on call for independent interpretation
6. Cardiologist provides definitive interpretation
7. Original AI + both physician interpretations documented in record
8. Status: REVIEWED by multiple physicians

**Scenario 4: Critical Findings Requiring Immediate Action**
1. AI identifies AF at high confidence (>90%)
2. System flags as 'CRITICAL ALERT'
3. Device sends notifications:
   - EHR alert (red banner on patient chart)
   - Optional: Pager alert to on-call cardiologist (if configured)
4. Clinical staff required to acknowledge alert (prevents missing it)
5. Physician reviews and confirms/denies AF diagnosis
6. If confirmed AF: Protocol initiated (rate control, anticoagulation assessment, etc.)

**Logging and Audit:**
- Every physician action logged: agreed, disagreed, deferred, escalated
- All overrides captured with physician reasoning
- Audit trail inspectable for QA review
- System generates monthly 'Override Report':
  - How many times was AI correct but overridden? (suggests over-confidence)
  - How many times was AI wrong but overridden correctly? (suggests AI weakness in certain cases)
  - How many times was AI correct but physician deferred? (suggests alert fatigue)

**Residual Risk:** Physician has clear mechanisms to override; no forced compliance with AI"

---

### 3.2 Training Requirements

What training does a physician need to use the device safely?

[INSERT: Training program]

Example: "**Mandatory Training Program for Device Use:**

**Format:** 15-minute online module + 5-minute hands-on demo

**Curriculum:**

Module 1: Device Overview (3 min)
- What the device does: 'AI-assisted AF detection from 12-lead ECG'
- What it doesn't do: 'Does not diagnose other conditions; does not replace clinical judgment'
- Regulatory status: '510(k) cleared by FDA; not autonomous diagnosis'

Module 2: Output Interpretation (5 min)
- Probability score: What 87% confidence means (model is correct 87% of the time in testing)
- 95% CI: Uncertainty range; narrow CI = more precise estimate
- Confidence level: 'HIGH' vs 'LOW' labels guide reliance on output
- Color coding: Red = AF likely (high alert); yellow = uncertain; green = normal
- Disclaimer: 'Always review original ECG; AI is decision support only'

Module 3: Common Failure Modes (4 min)
- When device underperforms:
  a) Paroxysmal AF not present at time of ECG (will miss AF if not happening now)
  b) High artifact (device flags as 'manual review'; do not trust if artifact is >15%)
  c) Extreme heart rates: <45 or >120 BPM (device less accurate; verify manually)
  d) Asian populations (limited validation; heightened caution recommended)
- What to do: 'If any of these, increase manual review; do not rely solely on AI'

Module 4: Workflow Integration (2 min)
- Where output appears: EHR embedded result or standalone web app
- How to access: Login via hospital SSO
- Typical latency: 150 ms after ECG submission
- Fallback if system down: Device gracefully fails; manual interpretation only (no error messages)

Module 5: Override and Escalation (1 min)
- 'You always override the device if you disagree'
- How to enter alternative interpretation: [button demo]
- When to escalate: If very uncertain, request cardiology consult

**Hands-On Demo (5 min):**
- Trainee views 3 realistic examples:
  1. Clear AF with high confidence (what a confident positive looks like)
  2. Normal sinus rhythm (what a confident negative looks like)
  3. Ambiguous case with moderate confidence (what uncertain output looks like)
- Trainee practices: Entering alternative interpretation and override
- Trainee practices: Requesting consultation for uncertain case
- Demo run in realistic EHR interface trainee will actually use

**Competency Assessment:**
- Quiz: 5 questions (pass >80%)
  1. 'Your hospital uses this device. A 74-year-old in the ED has ECG suspicious for AF.
     Device says "AF likely 91%". What should you do?'
     A) Trust the device; start anticoagulation (WRONG)
     B) Review the original ECG yourself; make final decision (CORRECT)
     C) Defer to AI; device is cleared by FDA (WRONG)
  2-5. [similar scenario-based questions]
- Practical: Demonstrate one device interaction in actual EHR
- Reassessment: Required annually (refresher training, 5 min)

**Accessibility:**
- Training available in English + Spanish (planned)
- Available online 24/7; takes 20 min including demo
- Closed captions on videos
- Printable reference guide (1 page) for quick lookup during use

**Completion Tracking:**
- Hospital administrator can view: Who has completed training?
- Mandatory before first device use
- Reminder: Automatically sent 1 month before training expiration

**Efficacy Data:**
- Post-training assessment: 95% of physicians demonstrate understanding
- Post-deployment survey: 90% report training was sufficient
- Adverse event review: No reported incidents attributed to training inadequacy"

---

## 4. Usability Testing and User Feedback

### 4.1 Formative Usability Testing

Did you test the interface with actual users before release?

[INSERT: Usability study]

Example: "**Usability Testing Study (Formative Evaluation):**

**Study Design:**
- Participants: 12 cardiologists and 4 cardiac nurses (n=16 total)
- Setting: Hospital cardiology departments in Cleveland and Baltimore
- Protocol: Think-aloud protocol; participants verbalize thoughts while using device
- Test cases: 10 ECG cases with varying results (5 AF, 5 non-AF; mix of clear and ambiguous)
- Metrics: Time to interpretation, accuracy of interpretation, ease of override, subjective satisfaction
- Testing date: January-February 2024 (pre-submission usability testing)

**Participant Characteristics:**
- Age range: 32-68 years (mean 49)
- Experience: 8-35 years ECG experience (mean 18 years)
- Tech comfort: 8 report high computer comfort; 5 report moderate; 3 report low comfort
- Gender: 10 male, 6 female (approximate cardiology demographic)

**Test Scenarios:**

Scenario 1: Clear AF Case
- ECG shows obvious atrial fibrillation
- AI prediction: 'AF likely, 95% confidence'
- Expected physician behavior: Agree with AI; confirm AF diagnosis
- Observed: 15/16 participants (94%) correctly agreed with AI
- Completion time: 45 seconds median (range: 30-90 sec)
- Issues: None identified
- Recommendation: Workflow for clear cases is efficient

Scenario 2: Ambiguous Case (Artifact)
- ECG shows significant 60 Hz artifact obscuring rhythm
- AI prediction: 'AF likely, 72% confidence'
- Expected physician behavior: Override AI; request manual review; possibly repeat ECG
- Observed: 12/16 (75%) correctly identified artifact and overrode AI
- Completion time: 120 seconds median (range: 80-180 sec)
- Issues: 4 participants (25%) initially agreed with AI without noticing artifact
  - Root cause: Saliency map (explanation feature) was not immediately visible
  - Solution: Moved saliency map higher on report; color-highlighted artifact warning
- Recommendation: Revised UI to make explanation more prominent

Scenario 3: Critical Alert (High-Risk AF)
- ECG shows rapid AF with RVR (rate >140)
- AI prediction: 'AF CRITICAL (98% confidence, rapid rate)'
- Expected physician behavior: Recognize criticality; escalate immediately
- Observed: 16/16 (100%) correctly recognized alert; took appropriate action
- Completion time: 30 seconds (faster than other cases; obvious alert)
- Issues: Some participants wanted "one-click escalation button"
- Recommendation: Added "Alert cardiology" button for rapid escalation

Scenario 4: Device Disagrees with Ground Truth
- ECG shows paroxysmal AF (irregular rhythm visible)
- AI prediction: 'Sinus rhythm, 62% confidence'
- Expected physician behavior: Identify mismatch; override AI; diagnose AF correctly
- Observed: 13/16 (81%) correctly overrode AI
- Issues: 3 participants did not override; trusted AI too much
  - Root cause: These 3 had lowest tech comfort and highest deference to "computer"
  - Solution: Emphasized in training that device is fallible; physicians are the authority
  - Additional mitigation: Added prominent disclaimer on low-confidence cases
- Recommendation: Enhanced training for low-tech-comfort physicians

**Satisfaction Metrics (Post-Test Survey):**

| Metric | Mean (1-5 scale) | Comment |
|---|---|---|
| Output clarity | 4.6/5 | Most liked clear color-coding |
| Workflow integration | 4.3/5 | Small delay in EHR integration noted |
| Confidence in override | 4.7/5 | Override process felt natural |
| Training adequacy | 4.4/5 | Wanted more examples of failures |
| Overall device usefulness | 4.5/5 | Positive; would use in clinical practice |

**Recommendations Implemented (Pre-Submission Fixes):**

1. Saliency map moved higher (implemented v1.1)
2. Artifact warning made more prominent (implemented v1.1)
3. One-click escalation button added (implemented v1.1)
4. Training emphasizes AI is fallible, humans make final decision (updated training v1.2)
5. Additional example of AF missed by AI added to training (updated training v1.2)

**Conclusion:** Usability testing identified minor UI improvements before submission.
Post-revision satisfaction increased to 4.7/5 mean across all metrics."

---

## 5. Adverse Event Monitoring and Feedback

### 5.1 Clinical Feedback Mechanism

How do clinicians report problems or improvements?

[INSERT: Feedback collection]

Example: "**User Feedback and Adverse Event Reporting System:**

**Built-In Feedback Button:**
- On every device report: 'Report Issue' button (bottom right)
- Non-intrusive (gray, small, does not interrupt workflow)
- Clicking opens modal: Feedback form

**Feedback Form:**

```
What happened? [Required]
[ ] Device was too slow (took >500 ms)
[ ] Output was confusing or hard to interpret
[ ] Device made an error (predicted opposite of actual diagnosis)
[ ] Override or escalation process was clunky
[ ] Training was inadequate
[ ] Other [text field]

What should we improve? [Optional text field]
[Large text box for free-form feedback]

Patient outcome (optional):
[ ] No harm (error caught and corrected)
[ ] Minor harm (unnecessary testing/treatment)
[ ] Moderate harm (delayed diagnosis, patient impact)
[ ] Severe harm (serious adverse outcome)

Contact info (optional):
[Name, hospital, email]
[ ] I want to be contacted about this feedback

[Submit] [Cancel]
```

**Backend Processing:**
- All feedback logged to central database
- Monthly analysis: What issues are most common?
- Prioritization: High-severity feedback reviewed within 48 hours
- Response: User receives email confirmation + resolution timeline
- Transparency: Aggregate feedback summary shared with users annually

**Adverse Event Escalation:**
- Any feedback indicating patient harm triggers FDA notification (21 CFR 803.12)
- Serious adverse event: Reported to FDA MedWatch system
- Trend analysis: If pattern detected (e.g., >3 similar events in 1 month), triggers alert

**Example Feedback Processed:**

Feedback 1: 'Device was too slow; I was waiting >1 second for result; workflow disrupted'
- Root cause investigation: Latency was 150 ms (normal); feedback suggested EHR infrastructure issue
- Resolution: Recommended hospital IT optimize local server; provided tuning guide
- Outcome: Hospital implemented; latency reduced to <100 ms
- Learning: Updated deployment guide to include latency monitoring

Feedback 2: 'Device predicted AF but ECG clearly showed normal sinus rhythm; almost prescribed unnecessary anticoagulation'
- Root cause: Patient had paroxysmal AF at time of previous admission; current ECG showed normal sinus (paroxysmal AF not present at time of recording)
- Analysis: This is a known limitation; model correctly assigned probability (not extremely high confidence, 68%)
- Resolution: Physician correctly overrode AI and made right decision
- Learning: Training needs to emphasize paroxysmal AF as common failure mode; updated training

Feedback 3: 'I don't understand the 95% CI; what does it mean in clinical terms?'
- Root cause: Output format included CI notation; not intuitive to all users
- Resolution: Redesigned to show as 'Range: 84-91%' (more intuitive) instead of 'CI: 0.84-0.91'
- Outcome: Updated in v1.2
- Learning: Test explanations with non-ML audience"

---

## Checklist Before Finalizing

- [ ] Intended users clearly defined (clinician types, experience level, qualifications)
- [ ] Use environment described operationally (where/when device used, time constraints)
- [ ] Output display is clear and unambiguous (probabilistic not binary, confidence stated)
- [ ] Explanation features allow physician to understand AI reasoning (saliency maps, feature importance)
- [ ] Override mechanism is simple and well-integrated (physician always can override)
- [ ] Training program is concise and covers failure modes (15-20 minutes total)
- [ ] Usability testing conducted with representative users (n>=10)
- [ ] Usability issues identified and remediated (UI improvements documented)
- [ ] Feedback mechanism in place for post-deployment issues
- [ ] All color-coding and visual elements meet accessibility standards (WCAG 2.1 AA)
- [ ] Disclaimer present and prominent on all reports (decision support, not diagnosis)
- [ ] Workflow integration is efficient (does not add >1 minute per case)
- [ ] No automation bias risk remaining (explanation, uncertainty, override available)
