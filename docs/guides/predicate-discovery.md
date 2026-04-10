# Predicate Device Discovery via openFDA API

Finding a suitable predicate device is one of the first and most critical steps in preparing a 510(k) submission. This guide explains how to use the FDA SaMD Toolkit to discover and rank predicate devices automatically.

---

## Overview

The predicate discovery feature searches the FDA's 510(k) database via the public openFDA API and ranks results by relevance to your device:

1. **Search** the openFDA database for existing cleared devices
2. **Score and rank** results based on device description and intended use
3. **Export** the results as a markdown report for your submission

This is a simple, rule-based v1 that removes the biggest friction point for new submissions. It is not AI-powered like commercial solutions (e.g., Cruxi) but gives regulatory teams instant, free access to the predicate landscape.

---

## Step 1: Prepare Your Device Description

Gather the following information about your device:

- **Device Description**: A clear, technical description of what your device does. Examples:
  - "12-lead ECG arrhythmia classifier using deep learning"
  - "Wearable blood glucose monitor with Bluetooth connectivity"
  - "Ultrasound image segmentation system for cardiac chamber quantification"

- **Intended Use Statement** (optional): How your device will be used clinically. Examples:
  - "Detection of atrial fibrillation in adult outpatients"
  - "Continuous glucose monitoring in Type 1 diabetes patients"
  - "Automated measurement of left ventricular volume"

- **Product Code** (optional): If you already know the FDA product code your device will fall under (e.g., `DQK` for ECG devices), providing it can boost matching.

---

## Step 2: Run the Discovery Command

Use the `fda-samd predicate discover` command to search:

```bash
fda-samd predicate discover \
  --device-description "12-lead ECG arrhythmia classifier" \
  --intended-use "Detection of atrial fibrillation in adult patients" \
  --limit 10
```

### Command Options

- `--device-description TEXT` (required): Description of your device
- `--intended-use TEXT` (optional): Clinical intended use statement
- `--product-code TEXT` (optional): FDA product code (e.g., DQK)
- `--limit INTEGER` (default 10, max 100): Number of results to return
- `--output FILE` (optional): Write markdown report to a file

### Example with All Options

```bash
fda-samd predicate discover \
  --device-description "12-lead ECG machine with automatic rhythm analysis" \
  --intended-use "Detection of cardiac arrhythmias" \
  --product-code DQK \
  --limit 5 \
  --output predicates.md
```

---

## Step 3: Interpret the Results

The command prints a rich table with the following columns:

| Column | Meaning |
|--------|---------|
| **Rank** | Position in relevance ranking |
| **K Number** | FDA 510(k) clearance number (e.g., K790739) |
| **Device Name** | Marketing name of the predicate |
| **Applicant** | Manufacturer of the predicate |
| **Product Code** | FDA device classification code |
| **Match Score** | Relevance to your query (0-100%) |
| **Reasoning** | Why this device ranked highly |

### Understanding Match Scores

Scores are computed as:
- 50% device description fuzzy matching
- 30% intended use keyword overlap
- 20% FDA product code match (if applicable)

A score of 80%+ indicates strong relevance. Scores below 50% may indicate the predicate is from a different device category and should be verified carefully.

---

## Step 4: Export and Use Results

### Terminal Output

By default, results are shown in the terminal:

```bash
fda-samd predicate discover \
  --device-description "ECG classifier" \
  --intended-use "Arrhythmia detection" \
  --limit 3
```

### Markdown Export

To generate a markdown report for your submission:

```bash
fda-samd predicate discover \
  --device-description "ECG classifier" \
  --intended-use "Arrhythmia detection" \
  --output predicates.md
```

The markdown file includes:
- Search criteria (device description, intended use, product code)
- Ranked table of top predicates
- K-numbers suitable for inclusion in your 510(k)
- Attribution to openFDA

You can then include or reference this table in your 510(k) submission's "Comparison to Predicate" section.

---

## Example Workflow

### Scenario: Building an ECG AI Device

1. **Gather Requirements**
   ```
   Device: 12-lead ECG deep learning classifier
   Intended Use: Detect atrial fibrillation in outpatient settings
   Product Code: DQK (anticipated)
   ```

2. **Run Discovery**
   ```bash
   fda-samd predicate discover \
     --device-description "12-lead ECG deep learning classifier" \
     --intended-use "Detect atrial fibrillation in outpatient settings" \
     --product-code DQK \
     --limit 10 \
     --output ecg_predicates.md
   ```

3. **Review Results**
   - Open `ecg_predicates.md`
   - Identify top 3-5 predicates with highest match scores
   - Manually verify each predicate in the FDA 510(k) database to confirm substantial equivalence

4. **Use in Submission**
   - Include K-numbers of selected predicates in your predicate comparison section
   - Cite the openFDA database in references

---

## Important Notes

### Accuracy and Limitations

- This tool performs **rule-based matching**, not AI-powered analysis. It may miss semantically similar devices.
- Always manually verify each predicate in the FDA's official 510(k) database to confirm substantial equivalence.
- Match scores are heuristic estimates. Final predicate selection should be based on regulatory judgment and substantial equivalence analysis.

### Rate Limits

The openFDA API enforces a rate limit of 240 requests per minute. Normal usage will not hit this limit. If you receive a rate limit error, wait a moment and retry.

### Citations

If you use the openFDA API in your submission, include this citation:

> Results obtained from the U.S. Food and Drug Administration's openFDA API. For more information, see https://open.fda.gov/.

---

## Troubleshooting

### "No matching predicates found"

- Try a simpler, more general device description (e.g., "ECG device" instead of "12-lead automated ECG arrhythmia classifier with deep learning")
- Try searching without an intended use filter
- Search by product code alone if you know it

### Low match scores on all results

- Your device description may be very novel or in an emerging category
- Manually search the FDA 510(k) database for comparators
- Consider consulting with a regulatory consultant

### Network or API errors

- Check your internet connection
- The openFDA API may be temporarily unavailable; retry in a few minutes
- For persistent issues, report a GitHub issue

---

## Next Steps

1. **Verify Substantial Equivalence**: Manually review each predicate's 510(k) summary on the FDA website to confirm it is a true comparator
2. **Build Your Comparison**: Use the predicate information to draft the "Comparison to Predicate(s)" section of your 510(k)
3. **Consult Regulatory Experts**: Substantial equivalence determination is a key FDA decision; work with experienced regulatory consultants if unsure
4. **Document Selection**: In your submission, explain why each selected predicate is appropriate for your device

---

## References

- [FDA 510(k) Premarket Notification Database](https://www.accessdata.fda.gov/cdrh_docs/cfr/cfr806.html)
- [openFDA API Documentation](https://open.fda.gov/)
- [FDA Substantial Equivalence Guidance](https://www.fda.gov/medical-devices/510k-premarket-notification)
