# Cover Letter — Informatica (Slovenian Society Informatika)

**To:**  
Prof. Dr. Matjaž Gams / Editorial Board  
Editors-in-Chief, *Informatica*  

**Date:** August 27, 2026  
**Subject:** Submission of original research paper: *"Agreement Among Explainability Methods: A Cross-Model, Cross-Domain Study"*  
**Processing Tier Selection:** **N (Normal)** — standard processing track (no fee, $0 APC).  

---

Dear Editors-in-Chief and Editorial Board of *Informatica*,

We are pleased to submit our original research manuscript titled **"Agreement Among Explainability Methods: A Cross-Model, Cross-Domain Study"** for consideration as a regular research article in *Informatica*. Our work presents a 100% computational computer science contribution in the core area of Explainable Artificial Intelligence (XAI) and Interpretable Machine Learning, perfectly aligned with the aims and scope of *Informatica*.

In this study, we address a foundational yet under-tested premise in applied machine learning: the implicit assumption that post-hoc feature attribution methods (such as SHAP, LIME, and Permutation Importance) largely converge on the same importance rankings. Through a controlled, cross-domain empirical study spanning **four diverse public tabular benchmarks** (OULAD, Student Dropout, German Credit, and Rice Grain Morphology), **three machine learning model families** (Random Forest, Gradient Boosting/XGBoost, and Logistic Regression), and **ten cross-validation folds** (totaling 360 computed feature rankings), we quantitatively evaluate pairwise concordance using Kendall's $\tau$ and two-way factorial ANOVA. 

Our findings demonstrate that while stability within folds of the same method is high (mean $\tau = 0.54$--$0.89$), agreement between different attribution methods applied to the *identical* trained model is substantially and significantly lower (mean $\tau = 0.28$--$0.47$, $p < 10^{-120}$). Through repeated-seed controls, we rule out estimator sampling noise as the driving mechanism. Furthermore, top-10 feature ranking comparisons reveal that different attribution methods highlight starkly divergent feature subsets for stakeholders. Consequently, we provide concrete guidelines urging practitioners to report concordance across multiple XAI techniques rather than relying on a single unverified explainer.

We confirm that:
1. This manuscript is original, has not been published previously, and is not currently under review elsewhere.
2. The submission adheres strictly to the official *Informatica* LaTeX template (`Informat.sty`) and formatting guidelines.
3. In accordance with the journal's policy on AI assistance, we fully disclose in the manuscript's Acknowledgements and ethical declarations the use of LLM tools for coding assistance, proofreading, and formatting under the authors' sole supervision and verification.
4. We select the **Normal (N)** processing track ($0 APC).

In accordance with the journal's submission policies, we suggest the following three independent expert reviewers in XAI and machine learning interpretability:

1. **Prof. Dr. Przemysław Biecek**  
   *Affiliation:* Faculty of Mathematics and Information Science, Warsaw University of Technology, Poland  
   *E-mail:* `przemyslaw.biecek@pw.edu.pl`  
   *Expertise:* Explainable Artificial Intelligence, Model Interpretability, Attribution Benchmarks  

2. **Prof. Dr. Marko Robnik-Šikonja**  
   *Affiliation:* Faculty of Computer and Information Science, University of Ljubljana, Slovenia  
   *E-mail:* `marko.robniksikonja@fri.uni-lj.si`  
   *Expertise:* Feature Importance, Explainable Machine Learning, Data Mining  

3. **Prof. Dr. Wojciech Samek**  
   *Affiliation:* Department of Artificial Intelligence, Fraunhofer HHI & TU Berlin, Germany  
   *E-mail:* `wojciech.samek@hhi.fraunhofer.de`  
   *Expertise:* Interpretable Machine Learning, Neural Network Attribution, XAI Evaluation  

Thank you very much for your time, editorial evaluation, and consideration of our manuscript.

Sincerely,

**The Authors**  
Department / Faculty  
Institution Name, City, Country  
*Corresponding e-mail:* `author@email.edu`
