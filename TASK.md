# Cross-Lingual Legal Summarization — Task Brief

> **Deadline:** 3 Days | **Discussion:** Saturday | **Contact:** Mohar

---

## 1. Objective

Evaluate **English → Hindi legal summarization** using the **MILDSum** dataset by comparing three prompting approaches:

1.  **Zero-shot**
2.  **Few-shot**
3.  **Chain-of-Thought (CoT)**

The main goal is to understand **which approach works better and why**, rather than only comparing metric scores.

---

## 2. Dataset

Use the **10 samples** available at:
**https://github.com/Law-AI/MILDSum/tree/main/Data/MILDSum_Samples**

Each sample contains:

| File | Description |
| :--- | :--- |
| `EN_Judgment.txt` | English judgment (Model Input) |
| `EN_Summary.txt` | English reference summary |
| `HI_Summary.txt` | Hindi reference summary (Evaluation Reference) |

**Instruction:** Use **all 10 samples** for evaluation. The English judgment will be the model input, and the Hindi summary will be used as the reference.

---

## 3. Model Selection

You can use **any one** of the following models (choose based on availability):

*   **Gemma 4** — 2B or 4B
*   **Qwen 3.5** — 2B or 4B
*   **Llama 3.2** — 2B or 4B

> **Note:** Choose **one** model and briefly explain why you selected it. Do not spend time comparing multiple models. The main comparison should be between the three prompting strategies.

---

## 4. Experiments

### 4.1 Zero-Shot
Create a prompt that asks the model to generate a **Hindi summary** of the English legal judgment. Run it on **all 10 cases**.

### 4.2 Few-Shot
Create a few-shot prompt using a small number of **English judgment → Hindi summary** examples. Run it on the same 10 cases.

> **Requirement:** Clearly mention which examples you used.

### 4.3 Chain-of-Thought (CoT)
Create a prompt that asks the model to **first identify the important information** in the judgment, such as:
*   Main facts
*   Legal issue
*   Court reasoning
*   Final decision

...and **then** generate the Hindi summary. Run it on the same 10 cases.

---

## 5. Automatic Evaluation

Compare the generated Hindi summaries with the reference Hindi summaries using:

*   **ROUGE-1**
*   **ROUGE-2**
*   **ROUGE-L**
*   **BERTScore**

#### 5.1 Overall Comparison Table

| Method | ROUGE-1 | ROUGE-2 | ROUGE-L | BERTScore |
| :--- | :---: | :---: | :---: | :---: |
| **Zero-shot** |  |  |  |  |
| **Few-shot** |  |  |  |  |
| **CoT** |  |  |  |  |

#### 5.2 Per-Case Results
Also record the result for **each individual case** (10 cases x 3 methods).

---

## 6. Manual Evaluation

Read the outputs and evaluate them on the following criteria (use a **1–5 scale** for each):

| Criterion | Description |
| :--- | :--- |
| **Factuality** | Are the facts correct? |
| **Coverage** | Are important points included? |
| **Legal Correctness** | Is the legal issue and final decision correct? |
| **Faithfulness** | Did the model add information that is not in the judgment? (Hallucination check) |
| **Hindi Quality** | Is the Hindi clear and understandable? |

---

## 7. Error Analysis

Identify common errors in the generated summaries. Look for:

*   Hallucinations
*   Important omissions
*   Wrong facts
*   Wrong legal conclusions
*   Translation errors
*   Incorrect legal terminology

Create a simple table showing **how often these errors occur for each method**.

| Error Type | Zero-shot | Few-shot | CoT |
| :--- | :---: | :---: | :---: |
| Hallucinations |  |  |  |
| Important Omissions |  |  |  |
| Wrong Facts |  |  |  |
| Wrong Legal Conclusions |  |  |  |
| Translation Errors |  |  |  |
| Incorrect Legal Terminology |  |  |  |

### 7.1 Compare Metrics with Manual Evaluation

Answer the following:

1.  Does the method with the highest ROUGE/BERTScore also look best manually?
2.  Are there cases where the metric gives a good score but the summary is actually wrong?
3.  Are there cases where the metric gives a low score but the summary is actually good?

> This is an important part of the analysis.

---

## 8. Select 2–3 Interesting Cases

Show examples where:

*   One prompting method clearly performs better
*   One method makes an important mistake
*   Automatic metrics and manual evaluation disagree

For each case, show:
1.  The relevant part of the judgment
2.  The three generated summaries (Zero-shot, Few-shot, CoT)
3.  A short explanation

---

## 9. Final Presentation (8–10 Slides)

Prepare a presentation covering:

1.  Problem
2.  Dataset
3.  Model and Experimental Setup
4.  Three Prompting Strategies
5.  Automatic Evaluation Results
6.  Manual Evaluation Results
7.  Error Analysis
8.  Interesting Examples
9.  Key Findings
10. Limitations and What You Would Do Next

---

## 10. Evaluation Criteria

The main evaluation will be based on the **quality of your final analysis and presentation**, not just whether the code runs.

We will look at:

*   [ ] Whether the experiment was designed fairly
*   [ ] Whether the evaluation is well thought out
*   [ ] Whether you can identify meaningful errors
*   [ ] Whether you can explain why one method performs better or worse
*   [ ] Whether you understand the limitations of ROUGE/BERTScore
*   [ ] Whether you can clearly communicate your findings

> **Important:** Do not assume that CoT or few-shot will perform better. The goal is to find out what the evidence shows. Since the dataset contains only 10 cases, treat the results as an **exploratory experiment** and avoid making broad claims.

---

## 11. Expected Final Deliverables

1.  **Code** — Maintain a git repo for all three experiments
2.  **Generated Summaries** — For all 10 cases (3 methods)
3.  **Automatic Evaluation Results** — Tables + per-case scores
4.  **Manual Evaluation and Error Analysis** — Scored tables + analysis
5.  **Final Presentation** — 8–10 slides

### Central Question to Answer

> **What did you learn about English-to-Hindi legal summarization from this experiment, and what evidence supports your conclusion?**

---

*Task saved as `TASK.md` — SONAA Workspace*
