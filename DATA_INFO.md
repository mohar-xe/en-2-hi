# Dataset Info — MILDSum Samples

**Source:** https://github.com/Law-AI/MILDSum/tree/main/Data/MILDSum_Samples
**Local Path:** `./Data/` (10 samples)
**Pulled:** 2026-09-02
**Paper:** Datta et al. EMNLP 2023 — [https://aclanthology.org/2023.emnlp-main.321/](https://aclanthology.org/2023.emnlp-main.321/)

## Structure
```
Data/
├── Sample_1/  EN_Judgment.txt (1607w)  EN_Summary.txt (796w)  HI_Summary.txt (843w)
├── Sample_2/  EN_Judgment.txt (4332w)  EN_Summary.txt (925w)  HI_Summary.txt (664w)
├── Sample_3/  EN_Judgment.txt (5798w)  EN_Summary.txt (746w)  HI_Summary.txt (751w)
├── Sample_4/  EN_Judgment.txt (995w)   EN_Summary.txt (593w)  HI_Summary.txt (576w)
├── Sample_5/  EN_Judgment.txt (2920w)  EN_Summary.txt (938w)  HI_Summary.txt (952w)
├── Sample_6/  EN_Judgment.txt (5959w)  EN_Summary.txt (744w)  HI_Summary.txt (772w)
├── Sample_7/  EN_Judgment.txt (2035w)  EN_Summary.txt (555w)  HI_Summary.txt (510w)
├── Sample_8/  EN_Judgment.txt (2360w)  EN_Summary.txt (367w)  HI_Summary.txt (360w)
├── Sample_9/  EN_Judgment.txt (2513w)  EN_Summary.txt (633w)  HI_Summary.txt (607w)
└── Sample_10/ EN_Judgment.txt (2268w)  EN_Summary.txt (964w)  HI_Summary.txt (985w)
```

Total: 30 files (10 judgments + 10 EN summaries + 10 HI references)

## Quick Stats
- Avg judgment length: ~2978 words
- Avg Hindi summary length: ~702 words
- All samples contain aligned triplets as per TASK.md spec

## Citation
```bibtex
@inproceedings{datta-etal-2023-mildsum,
  title = "{MILDS}um: A Novel Benchmark Dataset for Multilingual Summarization of {I}ndian Legal Case Judgments",
  author = "Datta, Debtanu and Soni, Shubham and Mukherjee, Rajdeep and Ghosh, Saptarshi",
  booktitle = "Proceedings of EMNLP 2023",
  year = "2023",
  pages = "5291--5302",
  url = "https://aclanthology.org/2023.emnlp-main.321"
}
```
