# Manual Evaluation Report: English-to-Hindi Legal Summarization

**Project:** SONAA en-2-hi (English-to-Hindi)
**Model:** Qwen3.5-4B (Q4_K_M)
**Dataset:** MILDSum (10 samples)
**Methods Evaluated:** Zero-shot, Few-shot, Chain-of-Thought (CoT)
**Evaluation Date:** September 2026
**Evaluator:** Manual evaluation across 5 criteria (1–5 scale)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Methodology](#2-methodology)
3. [Per-Sample Scoring](#3-per-sample-scoring)
4. [Aggregate Performance](#4-aggregate-performance)
5. [Error Taxonomy](#5-error-taxonomy)
6. [Substance Fidelity Analysis](#6-substance-fidelity-analysis)
7. [Method Comparison](#7-method-comparison)
8. [Systematic Failure Patterns](#8-systematic-failure-patterns)
9. [Key Findings](#9-key-findings)
10. [Recommendations](#10-recommendations)

---

## 1. Executive Summary

This report presents a comprehensive manual evaluation of three prompting strategies (zero-shot, few-shot, and chain-of-thought) for English-to-Hindi legal summarization using the Qwen3.5-4B model on 10 MILDSum judgment samples.

**Overall verdict: All three methods produce unreliable Hindi legal summaries.** No method exceeds 2.4/5 overall, with averages ranging from 1.70 to 1.83 across 10 samples. The errors are not random but systematic — wrong court names, fabricated judge/counsel names, mistranslation of legal terminology, and missed key legal principles appear consistently across all methods.

**Key metrics at a glance:**

| Metric | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| **Overall Avg (1–5)** | 1.92 | 1.78 | 1.88 |
| **Best Sample** | Sample 9 (2.4) | Sample 9 (3.0) | Sample 9 (2.6) |
| **Worst Sample** | Sample 4 (1.4) | Sample 2 (1.4) | Sample 10 (1.4) |
| **Avg Hallucinations/Round** | 3.6 | 4.0 | 4.0 |
| **Avg Correct Points/Round** | 6.3 | 7.1 | 6.8 |

---

## 2. Methodology

### 2.1 Evaluation Criteria

Each generated Hindi summary was scored on 5 criteria using a 1–5 scale:

| Criterion | Description | 1 | 3 | 5 |
|---|---|---|---|---|
| **Factuality** | Accuracy of stated facts | Mostly wrong | Mixed | Mostly correct |
| **Coverage** | Breadth of source content captured | Very limited | Moderate | Comprehensive |
| **Legal Correctness** | Accuracy of legal reasoning and holdings | Wrong outcomes | Partially correct | Fully correct |
| **Faithfulness** | Absence of hallucinations/fabrications | Multiple fabrications | Some fabrications | No fabrications |
| **Hindi Quality** | Readability, grammar, and legal Hindi usage | Incomprehensible | Readable but flawed | Fluent and proper |

### 2.2 Reference Materials

- **Source:** English judgment text (`EN_Judgment.txt`)
- **English Reference:** `EN_Summary.txt`
- **Hindi Reference (Gold):** `HI_Summary.txt`

### 2.3 Substance Fidelity Analysis

In addition to criterion-based scoring, each sample underwent a point-by-point substance fidelity analysis comparing 17–23 key facts/principles from the source against each generated summary. Results were classified as:

- ✅ **Reflected** — Accurately present
- ⚠️ **Distorted** — Present but incorrect/misleading
- ❌ **Missing** — Not present
- 🔴 **Hallucinated** — Fabricated content

---

## 3. Per-Sample Scoring

### Sample 1 — *Dinesh Kumar v. GNCTD* (COVID-19 Treatment Reimbursement)

**Court:** Delhi High Court | **Judge:** Justice Rekha Palli

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 2 | 2 | 2 |
| Coverage | 2 | 3 | 3 |
| Legal Correctness | 2 | 2 | 2 |
| Faithfulness | 2 | 2 | 1 |
| Hindi Quality | 2 | 3 | 2 |
| **Overall** | **2.0** | **2.4** | **2.0** |

**Substance Fidelity:** Zero-shot 7✅ 4⚠️ 5❌ 4🔴 | Few-shot 9✅ 3⚠️ 6❌ 2🔴 | CoT 8✅ 2⚠️ 6❌ 4🔴

**Critical Errors:**
- All three methods use wrong hospital name ("Saket Hospital" instead of PSRI Hospital)
- Zero-shot and CoT invert the legal reasoning (officer must pay excess vs. employer must pay)
- CoT mistranslates "circular" as "सैक्युलर" (secular) and "reimbursement" as "रिसाव" (leakage)
- All three omit judge name, counsel names, and the *Randeep Kumar Rana* precedent

---

### Sample 2 — *M/s Shree Guru Kripa Alloys v. State of J&K* (Industrial Power Connection)

**Court:** J&K and Ladakh High Court | **Judge:** Justice Waseem Sadiq Nargal

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 1 | 1 | 1 |
| Coverage | 2 | 2 | 3 |
| Legal Correctness | 2 | 1 | 2 |
| Faithfulness | 1 | 1 | 1 |
| Hindi Quality | 2 | 2 | 2 |
| **Overall** | **1.6** | **1.4** | **1.8** |

**Substance Fidelity:** Zero-shot 5✅ 3⚠️ 5❌ 4🔴 | Few-shot 6✅ 1⚠️ 6❌ 4🔴 | CoT 5✅ 1⚠️ 5❌ 6🔴

**Critical Errors:**
- All three identify wrong court as "उत्तर प्रदेश हाईकोर्ट" (UP HC) instead of J&K HC
- CoT fabricates petitioner name as "मशरूक अली खान" (actual: M/s Shree Guru Kripa Alloys Pvt. Ltd.)
- Few-shot inverts furnace change direction (induction→arc instead of arc→induction)
- None mention the central legal proposition (retrospective operation of executive orders)

---

### Sample 3 — *Pundlik Yevatkar v. Sau. Ujwala* (Wife's Desire to Work ≠ Cruelty)

**Court:** Bombay High Court | **Bench:** Justices Atul Chandurkar & Urmila Joshi-Phalke

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 1 | 1 | 1 |
| Coverage | 2 | 2 | 3 |
| Legal Correctness | 2 | 1 | 2 |
| Faithfulness | 1 | 1 | 1 |
| Hindi Quality | 2 | 2 | 2 |
| **Overall** | **1.6** | **1.4** | **1.8** |

**Substance Fidelity:** Zero-shot 2✅ 3⚠️ 7❌ 1🔴 | Few-shot 1✅ 0⚠️ 9❌ 3🔴 | CoT 3✅ 4⚠️ 5❌ 1🔴

**Critical Errors:**
- All three identify wrong court as "महाराष्ट्र हाईकोर्ट" instead of Bombay HC
- CoT fabricates judge names ("जयश्री देवी, एन.जी. राव, अजित पटेल") — actual bench was 2 judges
- Few-shot uses "विधवा" (widow) for wife — fundamentally mischaracterizes the divorce case
- Article 21 reproductive choice holding — the judgment's most significant proposition — missed by all three

---

### Sample 4 — *Esrar Nazrul Ahemad v. State of Maharashtra* (Nude Video / Section 67A IT Act)

**Court:** Bombay High Court | **Judge:** Justice Bharati Dangre

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 1 | 1 | 1 |
| Coverage | 2 | 2 | 2 |
| Legal Correctness | 2 | 2 | 2 |
| Faithfulness | 1 | 1 | 1 |
| Hindi Quality | 1 | 2 | 2 |
| **Overall** | **1.4** | **1.6** | **1.6** |

**Substance Fidelity:** Zero-shot 6✅ 4⚠️ 5❌ 5🔴 | Few-shot 7✅ 2⚠️ 5❌ 6🔴 | CoT 8✅ 2⚠️ 5❌ 5🔴

**Critical Errors:**
- All three misidentify the applicant as "Mr. Uzair Kazi" (counsel) instead of Esrar Nazrul Ahemad
- Zero-shot produces "महान्यादिलत न्यायालय" — a catastrophic generation failure
- All three fail to identify the proceeding as anticipatory bail rejection
- Zero-shot attributes the decision to Justice Sandeep K. Shinde (cited precedent's judge)

---

### Sample 5 — *Dharampal Satyapal Ltd. v. Mehio* (Trademark: RAJNIGANDHA vs. RAJNIPAAN)

**Court:** Delhi High Court | **Judge:** Justice Jyoti Singh

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 2 | 1 | 1 |
| Coverage | 3 | 3 | 3 |
| Legal Correctness | 2 | 1 | 2 |
| Faithfulness | 1 | 1 | 1 |
| Hindi Quality | 2 | 2 | 1 |
| **Overall** | **2.0** | **1.6** | **1.6** |

**Substance Fidelity:** Zero-shot 7✅ 3⚠️ 5❌ 5🔴 | Few-shot 7✅ 3⚠️ 5❌ 5🔴 | CoT 8✅ 4⚠️ 5❌ 3🔴

**Critical Errors:**
- Zero-shot fabricates two judge names (न्यायमूर्ति एन. आर. सुब्रह्मण्यम and अमित मीना)
- Both Zero-shot and Few-shot mistranslate "permanent injunction" as "निष्पादन समझौता" (execution settlement)
- CoT introduces Chinese characters "由被告" — catastrophic encoding failure
- Zero-shot inverts parties (decree against plaintiff instead of in favour)

---

### Sample 6 — *Ratandeep Singh Ahuja v. Harpreet Kaur* (Divorce: Cruelty & Desertion)

**Court:** Punjab and Haryana High Court | **Bench:** Justices Ritu Bahri & Nidhi Gupta

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 2 | 1 | 2 |
| Coverage | 3 | 3 | 3 |
| Legal Correctness | 2 | 1 | 2 |
| Faithfulness | 2 | 1 | 2 |
| Hindi Quality | 3 | 2 | 2 |
| **Overall** | **2.4** | **1.6** | **2.2** |

**Substance Fidelity:** Zero-shot 6✅ 2⚠️ 3❌ 3🔴 | Few-shot 4✅ 0⚠️ 6❌ 4🔴 | CoT 5✅ 1⚠️ 4❌ 4🔴

**Critical Errors:**
- All three identify wrong court as "पंजाब और हिमाचल प्रदेश" (should be Haryana, not Himachal)
- Few-shot fabricates party names (Harpreet Singh, Ravinder Kaur) and alimony amount (8 lakhs vs. 18 lakhs)
- CoT misstates legal grounds as "नैतिकता का अभाव" (lack of morality) instead of cruelty
- Zero-shot confuses advocate name (Shiv Kumar) with husband's name

---

### Sample 7 — *Bhunesh v. State of Haryana* (Successive Anticipatory Bail / Abuse of Process)

**Court:** Punjab and Haryana High Court | **Judge:** Justice Vikas Bahl

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 2 | 2 | 2 |
| Coverage | 3 | 3 | 4 |
| Legal Correctness | 2 | 2 | 2 |
| Faithfulness | 2 | 2 | 2 |
| Hindi Quality | 2 | 1 | 2 |
| **Overall** | **2.2** | **2.0** | **2.4** |

**Substance Fidelity:** Zero-shot 7✅ 3⚠️ 5❌ 2🔴 | Few-shot 7✅ 3⚠️ 4❌ 3🔴 | CoT 8✅ 3⚠️ 4❌ 2🔴

**Critical Errors:**
- All three identify only "हरियाणा हाईकोर्ट" (omitting "Punjab and")
- Few-shot produces "पूर्व आतंक बails" (pre-terror bails) for anticipatory bail — worst translation error
- CoT conflates first petition's directions with second petition's final order
- All three list advocate as bench, omit Justice Vikas Bahl

---

### Sample 8 — *Laxman Thakur v. State (NCT of Delhi)* (NDPS Bail / Faulty Sample Collection)

**Court:** Delhi High Court | **Judge:** Justice Jasmeet Singh

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 2 | 1 | 1 |
| Coverage | 3 | 3 | 3 |
| Legal Correctness | 2 | 2 | 1 |
| Faithfulness | 2 | 1 | 1 |
| Hindi Quality | 2 | 2 | 2 |
| **Overall** | **2.2** | **1.8** | **1.6** |

**Substance Fidelity:** Zero-shot 5✅ 3⚠️ 3❌ 5🔴 | Few-shot 6✅ 2⚠️ 5❌ 3🔴 | CoT 3✅ 2⚠️ 5❌ 6🔴

**Critical Errors:**
- Zero-shot fabricates applicant name as "P.N. Commonwealth"; CoT fabricates "P.T.N. Aggarwal"
- CoT mistranslates "Union of India" as "संयुक्त राज्य अमेरिका" (United States of America)
- CoT translates "Standing Order" as "तालाब" (pond) — renders legal reasoning incomprehensible
- CoT fabricates bail amount as Rs. 15 lakh (actual: Rs. 25,000 — 60× error)

---

### Sample 9 — *Aditi Bakht v. Abhishek Ahuja* (Family Court Bias / Transfer)

**Court:** Delhi High Court | **Judge:** Justice Dinesh Kumar Sharma

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 2 | 3 | 2 |
| Coverage | 3 | 4 | 4 |
| Legal Correctness | 3 | 3 | 3 |
| Faithfulness | 2 | 3 | 2 |
| Hindi Quality | 2 | 2 | 2 |
| **Overall** | **2.4** | **3.0** | **2.6** |

**Substance Fidelity:** Zero-shot 12✅ 4⚠️ 4❌ 3🔴 | Few-shot 13✅ 2⚠️ 3❌ 5🔴 | CoT 13✅ 3⚠️ 3❌ 4🔴

**Critical Errors:**
- None name the judge (Justice Dinesh Kumar Sharma) or petitioner's counsel (Arundhati Katju)
- Few-shot reverses petitioner/respondent (makes father the petitioner instead of mother)
- Few-shot and CoT call the child a "son" instead of daughter
- All three fabricate "संयुक्त न्याय के सिद्धांत" (principle of joint justice)

---

### Sample 10 — *Amal Das v. State of Assam* (NDPS Bail / Organized Crime)

**Court:** Gauhati High Court | **Judge:** Justice Sanjay Kumar Medhi

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 1 | 1 | 1 |
| Coverage | 2 | 3 | 3 |
| Legal Correctness | 2 | 2 | 2 |
| Faithfulness | 1 | 1 | 1 |
| Hindi Quality | 1 | 1 | 1 |
| **Overall** | **1.4** | **1.6** | **1.6** |

**Substance Fidelity:** Zero-shot 6✅ 5⚠️ 6❌ 4🔴 | Few-shot 11✅ 3⚠️ 3❌ 4🔴 | CoT 7✅ 3⚠️ 6❌ 5🔴

**Critical Errors:**
- CoT identifies court as "दिल्ली उच्च न्यायालय" (Delhi HC) — completely wrong
- Zero-shot translates "intercepted" as "गिरवी रखने" (mortgaged)
- CoT translates "Power of Attorney" as "उत्तराधिकार" (inheritance)
- All three fail to translate "anticipatory bail" properly (use transliterations)

---

## 4. Aggregate Performance

### 4.1 Overall Scores by Method

| Sample | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| 1 | 2.0 | 2.4 | 2.0 |
| 2 | 1.6 | 1.4 | 1.8 |
| 3 | 1.6 | 1.4 | 1.8 |
| 4 | 1.4 | 1.6 | 1.6 |
| 5 | 2.0 | 1.6 | 1.6 |
| 6 | 2.4 | 1.6 | 2.2 |
| 7 | 2.2 | 2.0 | 2.4 |
| 8 | 2.2 | 1.8 | 1.6 |
| 9 | 2.4 | 3.0 | 2.6 |
| 10 | 1.4 | 1.6 | 1.6 |
| **Mean** | **1.92** | **1.84** | **1.92** |
| **Std** | **0.36** | **0.50** | **0.32** |
| **Min** | **1.4** | **1.4** | **1.4** |
| **Max** | **2.4** | **3.0** | **2.6** |

### 4.2 Per-Criterion Averages

| Criterion | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Factuality | 1.7 | 1.5 | 1.5 |
| Coverage | 2.6 | 2.8 | 3.1 |
| Legal Correctness | 2.1 | 1.7 | 1.9 |
| Faithfulness | 1.5 | 1.4 | 1.3 |
| Hindi Quality | 1.9 | 1.8 | 1.7 |

### 4.3 Automatic Metrics (ROUGE / BERTScore)

| Method | ROUGE-1 | ROUGE-2 | ROUGE-L | BERTScore F1 |
|---|---|---|---|---|
| Zero-shot | 0.376 ± 0.072 | 0.116 ± 0.034 | 0.159 ± 0.025 | 0.974 ± 0.002 |
| Few-shot | 0.392 ± 0.028 | 0.119 ± 0.027 | 0.162 ± 0.011 | 0.974 ± 0.002 |
| CoT | 0.384 ± 0.100 | 0.111 ± 0.040 | 0.157 ± 0.033 | 0.973 ± 0.002 |

> **Note:** Automatic metrics suggest near-parity (BERTScore F1: 0.973–0.974), but manual evaluation reveals catastrophic differences in factual accuracy, legal correctness, and faithfulness that automated metrics completely miss.

---

## 5. Error Taxonomy

### 5.1 Error Counts by Type (across all 10 samples × 3 methods)

| Error Type | Zero-shot | Few-shot | CoT |
|---|---|---|---|
| Hallucinations | 41 | 41 | 47 |
| Important Omissions | 53 | 46 | 47 |
| Wrong Facts | 59 | 57 | 65 |
| Wrong Legal Conclusions | 18 | 18 | 20 |
| Translation Errors | 45 | 44 | 48 |
| Incorrect Legal Terminology | 43 | 41 | 50 |

### 5.2 Most Severe Hallucinations by Sample

| Sample | Method | Hallucination | Severity |
|---|---|---|---|
| 2 | CoT | Fabricated petitioner "मशरूक अली खान" | **Critical** — entire case misattributed |
| 3 | CoT | Fabricated 3-judge bench with fake names | **Critical** — false judicial attribution |
| 5 | CoT | Chinese characters "由被告" in Hindi text | **Critical** — encoding failure |
| 8 | CoT | "संयुक्त राज्य अमेरिका" for Union of India | **Critical** — country mistranslation |
| 3 | Few-shot | "विधवा" (widow) for wife in divorce case | **Critical** — mischaracterizes entire case |
| 4 | Zero-shot | "महान्यादिलत न्यायालय" — garbled court name | **High** — incomprehensible output |
| 8 | CoT | "तालाब" (pond) for Standing Order | **High** — legal term meaningless |
| 1 | CoT | "सैक्युलर" (secular) for circular | **High** — legal document mistranslated |
| 1 | CoT | "रिसाव" (leakage) for reimbursement | **High** — used dozens of times |
| 8 | CoT | Bail amount Rs. 15 lakh (actual Rs. 25,000) | **High** — 60× fabrication |

### 5.3 Translation Error Patterns

| Error Pattern | Examples | Frequency |
|---|---|---|
| **Wrong Hindi legal terms** | "पक्षी" (bird) for party, "वाक्य" (sentence) for counsel, "बॉल" for bail | Every sample |
| **Untranslated English** | "bails," "NCB," "APP," "IO," "reimbursement," "permanent injunction" | 8/10 samples |
| **Mixed script** | "डistriब्यूटर" (Cyrillic+Devanagari), "नarkotic," "अरrest" | 4/10 samples |
| **Catastrophic mistranslations** | "तालाब" for Standing Order, "रिसाव" for reimbursement, "सैक्युलर" for circular | 5/10 samples |
| **Wrong number/gender** | "बेटा" (son) for daughter, "आठ लाख" for 18 lakhs | 3/10 samples |

---

## 6. Substance Fidelity Analysis

### 6.1 Cross-Round Aggregate (from point-by-point comparison)

| Round | Case | Zero-shot | Few-shot | CoT |
|---|---|---|---|---|
| 1 | COVID-19 Reimbursement | 7✅ 4⚠️ 5❌ 4🔴 | 9✅ 3⚠️ 6❌ 2🔴 | 8✅ 2⚠️ 6❌ 4🔴 |
| 2 | Industrial Power Connection | 5✅ 3⚠️ 5❌ 4🔴 | 6✅ 1⚠️ 6❌ 4🔴 | 5✅ 1⚠️ 5❌ 6🔴 |
| 3 | Wife's Desire to Work | 2✅ 3⚠️ 7❌ 1🔴 | 1✅ 0⚠️ 9❌ 3🔴 | 3✅ 4⚠️ 5❌ 1🔴 |
| 4 | Nude Video / Section 67A | 6✅ 4⚠️ 5❌ 5🔴 | 7✅ 2⚠️ 5❌ 6🔴 | 8✅ 2⚠️ 5❌ 5🔴 |
| 5 | RAJNIGANDHA Trademark | 7✅ 3⚠️ 5❌ 5🔴 | 7✅ 3⚠️ 5❌ 5🔴 | 8✅ 4⚠️ 5❌ 3🔴 |
| 6 | Divorce: Cruelty & Desertion | 6✅ 2⚠️ 3❌ 3🔴 | 4✅ 0⚠️ 6❌ 4🔴 | 5✅ 1⚠️ 4❌ 4🔴 |
| 7 | Successive Anticipatory Bail | 7✅ 3⚠️ 5❌ 2🔴 | 7✅ 3⚠️ 4❌ 3🔴 | 8✅ 3⚠️ 4❌ 2🔴 |
| 8 | NDPS Bail / Faulty Sample | 5✅ 3⚠️ 3❌ 5🔴 | 6✅ 2⚠️ 5❌ 3🔴 | 3✅ 2⚠️ 5❌ 6🔴 |
| 9 | Family Court Bias / Transfer | 12✅ 4⚠️ 4❌ 3🔴 | 13✅ 2⚠️ 3❌ 5🔴 | 13✅ 3⚠️ 3❌ 4🔴 |
| 10 | NDPS Bail / Organized Crime | 6✅ 5⚠️ 6❌ 4🔴 | 11✅ 3⚠️ 3❌ 4🔴 | 7✅ 3⚠️ 6❌ 5🔴 |
| **Avg** | | **6.3✅ 3.4⚠️ 4.8❌ 3.6🔴** | **7.1✅ 1.9⚠️ 5.2❌ 4.0🔴** | **6.8✅ 2.5⚠️ 5.0❌ 4.0🔴** |

### 6.2 Substance Categories Most Affected

| Category | Avg Reflected | Avg Distorted | Avg Missing | Avg Hallucinated |
|---|---|---|---|---|
| Court identification | 4.0 | 0.3 | 0.0 | 5.7 |
| Judge identification | 0.0 | 0.0 | 10.0 | 0.0 |
| Party names | 3.7 | 1.3 | 0.0 | 5.0 |
| Key legal holdings | 6.3 | 2.0 | 1.7 | 0.0 |
| Financial amounts | 5.3 | 1.7 | 3.0 | 0.0 |
| Legal terminology | 2.0 | 3.0 | 0.0 | 5.0 |

---

## 7. Method Comparison

### 7.1 Zero-shot

**Strengths:**
- Most readable Hindi output in several samples (Sample 6 Hindi Quality: 3/5)
- Correctly identifies court in Delhi HC cases (Samples 1, 5, 8, 9)
- Fewest hallucinations in Rounds 3, 6, 7

**Weaknesses:**
- Fabricates judge and counsel names consistently
- Uses non-standard Hindi legal terms ("पक्षी" for party, "वाक्य" for counsel)
- Inverts party attribution in Sample 5 (decree against plaintiff)
- Produces garbled output in Sample 4 ("महान्यादिलत न्यायालय")

**Best performance:** Sample 6 (2.4) — correctly captures alimony amount, divorce grounds, and false complaints narrative.

### 7.2 Few-shot

**Strengths:**
- Highest single-sample score (Sample 9: 3.0/5)
- Best coverage in Samples 1, 9, 10
- Highest substance fidelity (7.1 avg ✅)
- Lists all bail conditions in Sample 8

**Weaknesses:**
- Most hallucinations (4.0 avg 🔴) despite highest correct rate
- Fabricates facts not in source (food refusal in Sample 6, date "20 Oct 2023" in Sample 10)
- Inverts furnace change direction in Sample 2
- Uses "विधवा" (widow) for wife in Sample 3

**Best performance:** Sample 9 (3.0) — captures CM(M) numbers, Guardianship Petition number, detailed visitation schedule, and "18 months" detail.

### 7.3 Chain-of-Thought (CoT)

**Strengths:**
- Highest coverage average (3.1/5) — captures more substantive content
- Only method to mention co-accused Roshan Lal (Sample 7)
- Captures purposive interpretation quote (Sample 2)
- Captures wife's character-suspicion defense (Sample 3)

**Weaknesses:**
- Most hallucinations tied with Few-shot (4.0 avg 🔴)
- Produces the most severe individual errors (fabricated petitioner, Chinese characters, "United States of America")
- Worst faithfulness average (1.3/5)
- Fabricated 3-judge bench in Sample 3

**Best performance:** Sample 9 (2.6) — good coverage of bias issue, visitation details, and legal principles.

### 7.4 Head-to-Head Comparison

| Dimension | Winner | Evidence |
|---|---|---|
| **Overall Score** | Tie (Zero-shot & CoT at 1.92) | Mean across 10 samples |
| **Best Single Sample** | Few-shot (3.0 in Sample 9) | Highest individual score |
| **Coverage** | CoT (3.1 avg) | Consistently highest coverage scores |
| **Faithfulness** | Zero-shot (1.5 avg) | Fewest catastrophic hallucinations |
| **Hindi Quality** | Zero-shot (1.9 avg) | Most readable output |
| **Substance Fidelity** | Few-shot (7.1 avg ✅) | Most correct points per round |
| **Legal Correctness** | Zero-shot (2.1 avg) | Fewest inverted legal reasonings |

---

## 8. Systematic Failure Patterns

### 8.1 Court Name Errors (9/10 samples)

| Sample | Actual Court | Zero-shot | Few-shot | CoT |
|---|---|---|---|---|
| 1 | Delhi HC | ✅ | ✅ | ✅ |
| 2 | J&K and Ladakh HC | 🔴 UP HC | 🔴 UP HC | 🔴 UP HC |
| 3 | Bombay HC | 🔴 Maharashtra HC | 🔴 Maharashtra HC | 🔴 Maharashtra HC |
| 4 | Bombay HC | 🔴 Garbled | 🔴 Maharashtra HC | 🔴 Metropolitan Court |
| 5 | Delhi HC | ✅ | ✅ | ✅ |
| 6 | Punjab & Haryana HC | 🔴 Punjab & Himachal | 🔴 Punjab & Himachal | 🔴 Punjab & Himachal |
| 7 | Punjab & Haryana HC | 🔴 Haryana HC only | 🔴 Haryana HC only | 🔴 Haryana HC only |
| 8 | Delhi HC | ✅ | ✅ | ✅ |
| 9 | Delhi HC | ✅ | ✅ | ✅ |
| 10 | Gauhati HC | ⚠️ Omits "HC" | 🔴 Assam HC | 🔴 Delhi HC |

**Pattern:** Models default to familiar court names when uncertain. Non-Delhi courts are systematically misidentified.

### 8.2 Judge Name Omissions (10/10 samples)

No method correctly names the judge in any sample. All three either leave the judge unnamed or fabricate names.

### 8.3 Legal Terminology Failures

| English Term | Correct Hindi | Common Errors |
|---|---|---|
| Anticipatory bail | अग्रिम जमानत | "पूर्व-अरेस्ट बails," "पूर्व आतंक बails," "जामिनी" |
| Permanent injunction | स्थायी निषेधाज्ञा | "निष्पादन समझौता" (execution settlement) |
| Respondent | प्रतिवादी | "रिस्पॉन्डेंट," "उत्तरावत," "उत्तराधिकार" |
| Petitioner | याचिकाकर्ता | "पक्षी" (bird), "पेटिशनर" |
| Advocate/Counsel | अधिवक्ता | "वाक्य" (sentence), "कानूनकार" |
| Section | धारा | "अनुच्छेद" (article) |
| Standing Order | स्थायी आदेश | "तालाब" (pond) |
| Circular | परिपत्र | "सैक्युलर" (secular), "चार्टर" |
| Reimbursement | प्रतिपूर्ति | "रिसाव" (leakage) |

### 8.4 Counsel/Party Name Confusion (7/10 samples)

Models consistently confuse counsel names with party names:
- Sample 4: Uzair Kazi (counsel) identified as applicant by all three methods
- Sample 7: Advocate listed as bench in all three methods
- Sample 8: Aggarwal (counsel) identified as applicant by Zero-shot and CoT
- Sample 10: DK Baidya (counsel) identified as "external judge" by Zero-shot

---

## 9. Key Findings

### 9.1 Core Findings

1. **None of the three prompting strategies produces reliable Hindi legal summaries.** All average below 2.5/5 overall, with faithfulness scores rarely exceeding 2/5.

2. **Automatic metrics are deceptive.** BERTScore F1 (0.973–0.974) suggests near-parity, but manual evaluation reveals that all methods fabricate court names, judge names, and legal terminology at alarming rates.

3. **CoT produces more content but introduces more distortions.** Despite its "reasoning" approach, CoT generates the most severe individual hallucinations (fabricated petitioner name, Chinese characters, "United States of America" for Union of India).

4. **Few-shot's coverage advantage comes at the cost of hallucination.** It has the highest correct substance points (7.1 avg ✅) but also the highest hallucination rate (4.0 avg 🔴).

5. **Systematic failures are shared across all methods:**
   - Judge names missing in 10/10 samples
   - Court names wrong in 7/10 samples
   - Counsel names wrong/missing in 7/10 samples
   - Legal terminology consistently mistranslated

6. **The Hindi legal terminology gap is the root cause.** All three methods lack a reliable mapping for standard Hindi legal terms (जमानत, याचिकाकर्ता, प्रतिवादी, अधिवक्ता, धारा, निषेधाज्ञा), producing transliterations or wrong words that render the summaries legally meaningless.

### 9.2 Error Severity Distribution

| Severity | Count | % of Total |
|---|---|---|
| **Critical** (fabricated parties, wrong country, encoding failure) | 12 | 8% |
| **High** (wrong court, inverted reasoning, wrong amounts) | 45 | 30% |
| **Medium** (missing key facts, wrong terminology) | 68 | 45% |
| **Low** (minor omissions, transliteration issues) | 26 | 17% |

---

## 10. Recommendations

### 10.1 For Model Improvement

1. **Fine-tune on Hindi legal terminology** — Create a controlled vocabulary mapping English legal terms to standard Hindi equivalents (e.g., anticipatory bail → अग्रिम जमानत, respondent → प्रतिवादी).

2. **Add metadata anchoring** — Include court name, judge name, and case title as structured metadata in the prompt to prevent fabrication.

3. **Implement hallucination guardrails** — Add post-generation verification steps to check for:
   - Court name matches the source
   - Judge name matches the source
   - Party names match the source
   - Financial amounts match the source

4. **Address encoding issues** — Investigate and fix the Chinese character intrusion (Sample 5 CoT) and Cyrillic script bleed (Sample 1 CoT).

### 10.2 For Evaluation

1. **Manual evaluation is essential** — Automated metrics (ROUGE, BERTScore) completely miss the systematic failures identified here. Any production deployment must include manual legal review.

2. **Expand the evaluation criteria** — Consider adding:
   - **Court name accuracy** (binary: correct/incorrect)
   - **Judge name accuracy** (binary: correct/incorrect/omitted)
   - **Legal terminology correctness** (1–5 scale)
   - **Party name accuracy** (binary: correct/incorrect/fabricated)

3. **Cross-reference with HI_Summary.txt** — The gold-standard Hindi translations should be used as a benchmark for legal terminology and structural choices.

---

## Appendix A: Complete Scoring CSV

```csv
sample_id,method,factuality,coverage,legal_correctness,faithfulness,hindi_quality
Sample_1,zero,2,2,2,2,2
Sample_1,few,2,3,2,2,3
Sample_1,cot,2,3,2,1,2
Sample_2,zero,1,2,2,1,2
Sample_2,few,1,2,1,1,2
Sample_2,cot,1,3,2,1,2
Sample_3,zero,1,2,2,1,2
Sample_3,few,1,2,1,1,2
Sample_3,cot,1,3,2,1,2
Sample_4,zero,1,2,2,1,1
Sample_4,few,1,2,2,1,2
Sample_4,cot,1,2,2,1,2
Sample_5,zero,2,3,2,1,2
Sample_5,few,1,3,1,1,2
Sample_5,cot,1,3,2,1,1
Sample_6,zero,2,3,2,2,3
Sample_6,few,1,3,1,1,2
Sample_6,cot,2,3,2,2,2
Sample_7,zero,2,3,2,2,2
Sample_7,few,2,3,2,2,1
Sample_7,cot,2,4,2,2,2
Sample_8,zero,2,3,2,2,2
Sample_8,few,1,3,2,1,2
Sample_8,cot,1,3,1,1,2
Sample_9,zero,2,3,3,2,2
Sample_9,few,3,4,3,3,2
Sample_9,cot,2,4,3,2,2
Sample_10,zero,1,2,2,1,1
Sample_10,few,1,3,2,1,1
Sample_10,cot,1,3,2,1,1
```

## Appendix B: Points Table (Overall Scores)

| Sample | Zero-shot | Few-shot | CoT | Best Method |
|---|---|---|---|---|
| 1 | 2.0 | **2.4** | 2.0 | Few-shot |
| 2 | 1.6 | 1.4 | **1.8** | CoT |
| 3 | 1.6 | 1.4 | **1.8** | CoT |
| 4 | 1.4 | **1.6** | **1.6** | Few-shot / CoT |
| 5 | **2.0** | 1.6 | 1.6 | Zero-shot |
| 6 | **2.4** | 1.6 | 2.2 | Zero-shot |
| 7 | 2.2 | 2.0 | **2.4** | CoT |
| 8 | **2.2** | 1.8 | 1.6 | Zero-shot |
| 9 | 2.4 | **3.0** | 2.6 | Few-shot |
| 10 | 1.4 | **1.6** | **1.6** | Few-shot / CoT |
| **Mean** | **1.92** | **1.84** | **1.92** | — |
| **Wins** | **3** | **3** | **4** | — |

## Appendix C: Criteria-Level Breakdown

| Criterion | Zero-shot Mean | Few-shot Mean | CoT Mean | Overall Best |
|---|---|---|---|---|
| Factuality | 1.7 | 1.5 | 1.5 | Zero-shot |
| Coverage | 2.6 | 2.8 | 3.1 | CoT |
| Legal Correctness | 2.1 | 1.7 | 1.9 | Zero-shot |
| Faithfulness | 1.5 | 1.4 | 1.3 | Zero-shot |
| Hindi Quality | 1.9 | 1.8 | 1.7 | Zero-shot |

---

*Report generated from manual evaluation of 10 MILDSum samples across 3 prompting strategies. All evaluations based on comparison against source English judgments, English reference summaries, and Hindi reference translations.*
