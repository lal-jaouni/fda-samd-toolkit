# FDA SaMD Overview: Regulations, Pathways, and AI/ML

This guide explains the FDA regulatory landscape for Software-as-a-Medical-Device (SaMD), particularly AI and machine learning systems. No regulatory background required.

---

## What is SaMD?

SaMD stands for **Software-as-a-Medical-Device**. It's software that diagnoses, treats, mitigates, or monitors a disease or medical condition. Examples:

- AI algorithm that reads mammograms to detect breast cancer
- Wearable app that monitors heart rhythm for atrial fibrillation
- NLP system that extracts clinical findings from radiology reports
- Predictive model that estimates patient risk of hospital readmission

Key distinction: SaMD runs on general-purpose computing platforms (tablets, phones, servers) rather than in hardware. The software itself is the device.

### Why Regulate Medical Software?

A medical device can harm patients if it:

- Makes an incorrect diagnosis (false negative: missed disease)
- Causes harm from a wrong treatment recommendation
- Fails unexpectedly in a critical moment
- Degrades in performance over time
- Behaves differently for certain populations

FDA's job is to ensure software reaches patients with known, acceptable risk.

---

## FDA's Approach to AI/ML SaMD

FDA issued major guidance in 2021 and 2024 to address AI/ML medical devices:

- **AI/ML Action Plan (2021)**: Framework for transparency, validation, and monitoring of AI/ML systems
- **PCCP Guidance (December 2024)**: Predetermined Change Control Plan for post-market ML modifications
- **Good Machine Learning Practice (2021)**: Best practices for designing and validating ML models in healthcare

**Core principle**: FDA wants to see:

1. **How was the model trained?** (Data sources, size, preprocessing)
2. **How does it perform?** (Accuracy, sensitivity, specificity, on different populations)
3. **What happens when it changes?** (Retraining, data drift, failure modes)
4. **How will you monitor it?** (Ongoing performance tracking, drift detection)
5. **What's your failure plan?** (Thresholds for retraining, rollback procedures)

---

## Three FDA Approval Pathways

FDA has three main pathways for getting a medical device to patients. All three can apply to SaMD. Which one you use depends on your device's risk level.

### 1. 510(k): Substantial Equivalence

**Risk Level**: Low to moderate

**What it means**: You show that your device is "substantially equivalent" to a device already on the market (a predicate device). If similar devices exist, you use this pathway.

**Timeline**: 3-6 months

**Requirements**:

- Find a predicate device (similar algorithm, similar intended use, similar performance)
- Demonstrate performance equals or exceeds predicate
- Show your device poses no greater risks
- Submit 510(k) summary (usually 20-50 pages)

**For AI/ML**: You'll need to document:

- Training data characterization (size, diversity, sources)
- Algorithm performance on different populations (age, sex, comorbidities)
- Comparison to predicate device or alternative (human readers, older algorithms)
- Plan for monitoring performance post-market (data drift detection)
- Plan for retraining and versioning

**Example**: An AI ECG analyzer compared to a cleared predicate AI ECG analyzer (Philips algorithm). You show your model performs as well on a similar training dataset and patient population.

### 2. De Novo: First-of-its-Kind

**Risk Level**: Moderate

**What it means**: Your device is novel (no predicate exists), but the risks are manageable through special controls. De Novo creates the regulatory classification for your device type.

**Timeline**: 3-6 months

**Requirements**:

- Demonstrate the device meets a reasonable need
- Describe risks and how you mitigate them
- Propose special controls (post-market surveillance, labeling, performance standards)
- Submit De Novo summary

**For AI/ML**: You'll need everything in 510(k) plus:

- Justification for why no predicate exists
- Risk analysis showing risks are manageable (not unreasonable)
- Special controls specific to AI/ML (validation protocols, monitoring plans, update procedures)

**Example**: First AI system to diagnose a rare genetic disease from genome sequencing. No existing device does this, but you can show the risk is manageable through post-market surveillance and genetic expert review.

### 3. PMA: Premarket Approval

**Risk Level**: High

**What it means**: Your device is high-risk (treats serious conditions, has significant failure modes). PMA requires extensive clinical data proving safety and effectiveness before launch.

**Timeline**: 1-3 years

**Requirements**:

- Controlled clinical trials (usually multicenter, randomized)
- Safety and effectiveness data from real patients
- Manufacturing controls and quality systems
- Post-market surveillance plans
- Periodic safety updates

**For AI/ML**: You'll need everything above plus:

- Large clinical datasets (often 500+ patients)
- Independent validation on held-out test sets
- Controlled studies showing performance on intended population
- Risk analysis for edge cases and failure modes
- Monitoring and retraining procedures

**Example**: AI system that decides whether to start a patient on a high-risk cancer treatment. High stakes (toxicity, patient burden). Requires prospective clinical trial data.

---

## Which Pathway for Your Device?

Ask these questions:

| Question | Answer | Implication |
|----------|--------|-------------|
| Does a similar device already exist on the market? | Yes | Start with 510(k) |
| | No | De Novo or PMA |
| Could a failure of this device cause serious harm? | Yes | De Novo or PMA |
| | No | Probably 510(k) |
| Are you diagnosing or treating a serious disease? | Yes | Higher risk pathway |
| | No | Lower risk pathway |
| Does it require clinical data to prove it works? | Yes | De Novo or PMA |
| | No | Possibly 510(k) |

**Talk to FDA early** (via a pre-submission meeting, Q-submission) to confirm which pathway is right for your device.

---

## FDA's AI/ML Specific Concerns

FDA has emphasized these concerns for AI/ML SaMD:

### 1. Data Quality and Provenance

**Concern**: Models trained on biased or poor-quality data make biased or poor predictions.

**FDA expectation**: You document where your training data comes from, its size, demographic composition, and limitations. You show how you handled missing values, outliers, and data quality issues.

### 2. Sub-Population Performance

**Concern**: A model might work well on average but fail on specific groups (elderly patients, women, patients of color).

**FDA expectation**: You show performance broken down by age, sex, race, comorbidities, and other clinically relevant groups. If performance varies significantly, you explain why and whether it's acceptable.

### 3. Performance Monitoring and Drift

**Concern**: Model performance degrades over time as real-world data differs from training data (data drift). The model was validated on 2022 data, but in 2024 it fails more often.

**FDA expectation**: You have a plan to monitor performance post-market (using metrics like calibration, AUC, sensitivity on recent data). You have thresholds that trigger retraining or review.

### 4. Transparency and Explainability

**Concern**: Black-box models make it hard to understand failures or regulatory decisions.

**FDA expectation**: You explain how the model makes decisions (feature importance, decision boundaries). For high-stakes decisions, you may need interpretability.

### 5. Modification and Retraining

**Concern**: Companies retrain models post-market without FDA oversight, changing what the device does.

**FDA expectation**: You have a PCCP (Predetermined Change Control Plan) that defines what changes are allowed (retraining on new data, updating decision thresholds) and what changes require new approval.

---

## Key FDA Guidance Documents

These are essential references. All are free and public:

### PCCP Final Guidance (December 2024)

[Link](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)

Defines what a PCCP is, what it must contain, and how to write one. This is what the toolkit helps you generate.

**Core sections**:
- Device classification and intended use
- Algorithm overview (architecture, training approach)
- Training data characterization
- Performance documentation
- Change control procedures
- Monitoring and retraining triggers
- Failure mode analysis

**Length**: 25 pages of regulatory text. The toolkit reduces this to a questionnaire.

### AI/ML Action Plan (2021)

[Link](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-software-medical-device)

High-level framework. Key principles:

- Transparency in algorithms and training data
- Validation before and after deployment
- Risk management (what can go wrong, how do you prevent it)
- Real-world performance monitoring
- Clear update procedures (what changes can you make without FDA approval)

### Good Machine Learning Practice (2021)

[Link](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/good-machine-learning-practice-medical-device-development)

Best practices for ML medical devices:

- Performance testing on diverse datasets
- Model validation and versioning
- Handling of edge cases and failure modes
- Documentation standards
- Risk management

---

## Key Concepts: Terms You'll Encounter

### Predicate Device

An already-approved device similar to yours. If you're filing 510(k), you need a predicate. FDA requires that you're "substantially equivalent" to it.

Example: Your AI ECG analyzer's predicate is the existing Philips AI ECG analyzer. You show your model has similar performance.

### Substantial Equivalence

Your device performs the same function, in the same way, with the same or lower risk as the predicate.

For AI/ML: Same intended use, similar algorithm approach (CNN for images, RNN for time series), similar training data size/diversity, similar performance on the same types of patients.

### Indications for Use (IFU)

The official statement of what your device is intended to do. Very specific.

Good IFU: "Automated detection of atrial fibrillation from 12-lead ECG in adult patients (age 18-85) presenting to emergency or inpatient settings."

Bad IFU: "AI heart analyzer" (too vague, unclear patient population, unclear clinical setting).

### Intended Use Population (IUP)

The specific patients your device is meant for. Age, gender, comorbidities, clinical setting, etc.

Example IUP: "Adult patients (age 50-85), with at least one cardiovascular risk factor (hypertension, diabetes, prior MI), monitored in hospital telemetry units."

### Sensitivity and Specificity

Standard ML metrics FDA requires:

- **Sensitivity** (true positive rate): Of patients who actually have the condition, how many does your device detect? (Important: you don't want false negatives)
- **Specificity** (true negative rate): Of patients who don't have the condition, how many does your device correctly exclude? (Important: you don't want false alarms)

FDA usually wants both high. Rarely, you accept lower sensitivity to get higher specificity (fewer false alarms).

### Data Drift

When the real-world data your model sees differs from training data, performance changes. This is expected and must be monitored.

Example: Your model was trained on ECGs from patient population A (healthy volunteers, ages 20-40). In production, you get ECGs from population B (hospitalized patients, ages 60-90, on multiple medications). The ECGs look different, and your model's performance drops.

### Retraining

Updating the model weights with new data. Retraining changes what the device does. Must be controlled and monitored.

FDA's question: If you retrain on 2024 data, is the model still substantially equivalent to the cleared version? If yes, you can do it automatically. If no, you need approval.

---

## SaMD Definition: What Counts?

FDA's SaMD definition is broad. Your software is SaMD if it:

1. Is intended to diagnose, treat, mitigate, or monitor a disease or condition
2. Supports diagnosis or treatment decisions (even indirectly)
3. Provides medical insight about a patient's health

**Examples that ARE SaMD**:

- AI diagnosis system
- Decision support system (recommends a treatment)
- Monitoring system (alerts on abnormal values)
- Predictive model (estimates disease risk)
- Data analysis tool that informs medical decisions

**Examples that are NOT SaMD**:

- Electronic health record (stores data, doesn't diagnose)
- Electronic messaging system (HIPAA secure communication)
- General wellness app (no disease or condition mentioned)
- Software that manages medical practice (scheduling, billing)

When in doubt, FDA has a 3-part test. Consult FDA's "Definition of SaMD" document or ask in a pre-submission meeting.

---

## Regulatory Timeline

Typical timelines:

| Pathway | Preparation | FDA Review | Total |
|---------|------------|-----------|-------|
| 510(k) | 2-4 months | 1-3 months | 3-6 months |
| De Novo | 3-6 months | 3-6 months | 6-12 months |
| PMA | 6-18 months | 6-12 months | 1-3 years |

These are estimates. Your device may be faster or slower depending on complexity and FDA questions.

---

## Next Steps

1. **Deep dive into PCCP**: See [What is a PCCP?](pccp-explained.md)
2. **Build your PCCP**: See [PCCP Generator Guide](../guides/pccp-generator.md)
3. **Plan your 510(k)**: See [510(k) Templates Guide](../guides/510k-templates.md)
4. **Talk to FDA**: Pre-submission meeting (free, confidential). Ask: "Is 510(k) the right pathway for my device?" FDA will tell you.

---

## Key References

All free, all public:

- [FDA SaMD Definition](https://www.fda.gov/medical-devices/digital-health/software-medical-device-samd)
- [AI/ML Action Plan (2021)](https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-software-medical-device)
- [PCCP Guidance (Dec 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/predetermined-change-control-plans-machine-learning-enabled-medical-devices)
- [Good ML Practice (2021)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/good-machine-learning-practice-medical-device-development)
- [IEC 62304: Software Lifecycle](https://en.wikipedia.org/wiki/IEC_62304)

Questions? Open a [GitHub discussion](https://github.com/lal-jaouni/fda-samd-toolkit/discussions).
