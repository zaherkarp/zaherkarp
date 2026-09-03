<h1 align="center">Zaher Karp, M.P.H.</h1>

<p align="center">
  <!-- title:start -->
  <strong>Manager, Data Science and Engineering</strong> · Baltimore Health Analytics
  <!-- title:end -->
  <br>
  Production analytics in regulated healthcare: CMS Star Ratings, HEDIS, and value-based care.
</p>

<p align="center">
  <a href="https://zaherkarp.com"><img alt="Website" src="https://img.shields.io/badge/Website-0A5C54?style=flat-square&logo=googlechrome&logoColor=white"></a>
  <a href="https://linkedin.com/in/zkarp"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white"></a>
  <a href="https://scholar.google.com/citations?user=exrRbXMAAAAJ"><img alt="Google Scholar" src="https://img.shields.io/badge/Google_Scholar-4285F4?style=flat-square&logo=googlescholar&logoColor=white"></a>
  <a href="https://public.tableau.com/app/profile/zaher.karp/vizzes"><img alt="Tableau Public" src="https://img.shields.io/badge/Tableau_Public-E97627?style=flat-square&logo=tableau&logoColor=white"></a>
  <a href="https://zaherkarp.com/blog/"><img alt="Writing" src="https://img.shields.io/badge/Writing-0A5C54?style=flat-square&logo=rss&logoColor=white"></a>
  <a href="https://zaherkarp.com/resume.pdf"><img alt="Resume" src="https://img.shields.io/badge/Resume-B31B1B?style=flat-square&logo=adobeacrobatreader&logoColor=white"></a>
  <a href="mailto:me@zaherkarp.com"><img alt="Email" src="https://img.shields.io/badge/Email-0A5C54?style=flat-square&logo=gmail&logoColor=white"></a>
</p>

---

## About

I build and govern production analytics systems in regulated healthcare: pipelines, semantic layers, and CMS Star Ratings quality-measure systems that clinical, operational, and executive teams can trust and act on.

I started as a news writer and book editor, moved into healthcare research at UW-Madison, and now lead data engineering. That path still shapes how I work: clear questions, defensible methods, and results that change decisions. Today I'm a player-coach manager, building and running the pipelines while managing the engineers who own them.

## What I work on

- **Production data pipelines** — EHR data modeling across Epic, Cerner, Veradigm, and athenahealth; ETL/ELT on AWS and Databricks; stored procedures built to survive edge cases in regulated populations
- **Analytics governance** — semantic layers, metric definitions, and dbt-versioned models that give stakeholders one version of truth
- **Value-based care analytics** — ACO, MSSP, HEDIS, and CMS Medicare Stars performance tracking; benchmarking and significance testing against CMS methodology
- **Platform reliability** — observability, incident response, and cost optimization across cloud data infrastructure

## Featured projects

- **Stars Cliff Simulator** — interactive teaching demo of the 4.0★ Quality Bonus Payment cliff in CMS Star Ratings. Pure vanilla JS, no dependencies, synthetic weights.  
  [Live demo](https://zaherkarp.com/star-rating-predictor/) · [Methodology](https://zaherkarp.com/blog/star-rating-predictor-methodology/) · [Source](https://github.com/zaherkarp/zaherkarp.github.io/tree/main/star-rating-predictor)
- **Medicare Advantage Insight Engine** — a self-running daily feed that separates CMS Medicare Advantage rulemaking signal from press-release noise.  
  [Live feed](https://zaherkarp.com/medicare-advantage-insight-engine/) · [Repo](https://github.com/zaherkarp/medicare-advantage-insight-engine) · [Write-up](https://zaherkarp.com/blog/medicare-advantage-insight-engine/)
- **Healthcare Workforce Transition Platform (SkillSprout)** — an O\*NET-based model estimating reskilling transition probabilities across the healthcare workforce.  
  [Repo](https://github.com/zaherkarp/skillsprout) · [Write-up](https://zaherkarp.com/blog/onet-reskilling-probabilities/)
- **ECDS Shock Index** — a HEDIS Electronic Clinical Data Systems (ECDS) measure prototype and worked example.  
  [Repo](https://github.com/zaherkarp/ecds-shock-index) · [Write-up](https://zaherkarp.com/blog/ecds-shock-index/)
- **Stochastic Epidemic Simulator** — a SEIRV epidemic model that runs entirely in the browser via Pyodide, with Plotly charts.  
  [Live demo](https://zaherkarp.com/epidemic-simulation/) · [Write-up](https://zaherkarp.com/blog/two-states-one-pathogen/)

## Selected impact

- **Baltimore Health Analytics** — Manage two data scientists (a lead and an IC); own measure methodology, pipeline reliability, and release governance for a Medicare Advantage Stars analytics platform. Built a self-service forecast-versus-actual Stars cutpoint dashboard adopted by data science and the CEO.
- **Health Catalyst** — Led the post-acquisition migration of all analytics to a multi-cloud (AWS + Azure/Databricks) stack. Cut monthly storage cost ~50% and weekly load latency by 24+ hours; standardized SQL into reusable stored procedures (~70% codebase reduction).
- **healthfinch** — First analytics hire. Built a HIPAA- and HITRUST-compliant platform from scratch unifying app data and four EHR systems; authored Epic Clarity report libraries deployed across 50+ health systems; governed dashboards absorbed 7× user growth and saved 400+ prep hours per quarter.

## Writing

Long-form essays on healthcare data engineering, Stars methodology, and measurement. A few recent ones:

<!-- writing:start -->
- [My Cap Falls by a Third. My Work Falls by a Sixth.](https://zaherkarp.com/blog/cap-falls-third-work-falls-sixth/)
- [BTEQ Still Has a Job](https://zaherkarp.com/blog/bteq-still-has-a-job/)
- [The Metric Isn't Wrong. It's Just Not Where Quality Lives.](https://zaherkarp.com/blog/what-the-metric-cannot-see/)
- [One API call, three ways to split it: a FRED case study](https://zaherkarp.com/blog/one-api-call-three-ways-to-split-it/)
- [Should I Buy RAM Now?](https://zaherkarp.com/blog/should-i-buy-ram-now/)
<!-- writing:end -->

Full archive at [zaherkarp.com/blog](https://zaherkarp.com/blog/).

## Research

Peer-reviewed work on accountable care (Medicare Shared Savings), clinic design and team efficiency, and EHR optimization in primary care, from my years at UW-Madison.

<!-- research:start -->
6 peer-reviewed publications ([Google Scholar](https://scholar.google.com/citations?user=exrRbXMAAAAJ), [ResearchGate](https://www.researchgate.net/profile/Zaher-Karp)). The two most cited:

- [Approaches and challenges to optimizing primary care teams' electronic health record usage](https://pubmed.ncbi.nlm.nih.gov/25584902/) — *Journal of Innovation in Health Informatics* (2014)
- [Influence of environmental design on team interactions across 3 family medicine clinics](https://pubmed.ncbi.nlm.nih.gov/30913920/) — *Health Environments Research & Design Journal* (2019)
<!-- research:end -->

## Tech stack

<!-- stack:start -->
**Engineering & data**  
![SQL](https://img.shields.io/badge/SQL-0A5C54?style=flat-square) ![Python](https://img.shields.io/badge/Python-0A5C54?style=flat-square&logo=python&logoColor=white) ![dbt](https://img.shields.io/badge/dbt-0A5C54?style=flat-square&logo=dbt&logoColor=white) ![Ruby on Rails](https://img.shields.io/badge/Ruby_on_Rails-0A5C54?style=flat-square&logo=rubyonrails&logoColor=white) ![Clojure](https://img.shields.io/badge/Clojure-0A5C54?style=flat-square&logo=clojure&logoColor=white) ![Perl](https://img.shields.io/badge/Perl-0A5C54?style=flat-square&logo=perl&logoColor=white) ![SAS](https://img.shields.io/badge/SAS-0A5C54?style=flat-square) ![Stata](https://img.shields.io/badge/Stata-0A5C54?style=flat-square) ![R](https://img.shields.io/badge/R-0A5C54?style=flat-square&logo=r&logoColor=white) ![git](https://img.shields.io/badge/git-0A5C54?style=flat-square&logo=git&logoColor=white)

**Cloud & BI**  
![AWS](https://img.shields.io/badge/AWS-334155?style=flat-square&logo=amazonwebservices&logoColor=white) ![Azure](https://img.shields.io/badge/Azure-334155?style=flat-square&logo=microsoftazure&logoColor=white) ![Databricks](https://img.shields.io/badge/Databricks-334155?style=flat-square&logo=databricks&logoColor=white) ![Okta](https://img.shields.io/badge/Okta-334155?style=flat-square&logo=okta&logoColor=white) ![Sisense](https://img.shields.io/badge/Sisense-334155?style=flat-square) ![Periscope](https://img.shields.io/badge/Periscope-334155?style=flat-square) ![Power BI](https://img.shields.io/badge/Power_BI-334155?style=flat-square&logo=powerbi&logoColor=white) ![Grafana](https://img.shields.io/badge/Grafana-334155?style=flat-square&logo=grafana&logoColor=white) ![Datadog](https://img.shields.io/badge/Datadog-334155?style=flat-square&logo=datadog&logoColor=white)

**Healthcare**  
![HEDIS](https://img.shields.io/badge/HEDIS-6A6A6A?style=flat-square) ![CMS Medicare Stars](https://img.shields.io/badge/CMS_Medicare_Stars-6A6A6A?style=flat-square) ![ACO](https://img.shields.io/badge/ACO-6A6A6A?style=flat-square) ![MSSP](https://img.shields.io/badge/MSSP-6A6A6A?style=flat-square) ![HIPAA](https://img.shields.io/badge/HIPAA-6A6A6A?style=flat-square) ![HITRUST](https://img.shields.io/badge/HITRUST-6A6A6A?style=flat-square) ![ICD-10](https://img.shields.io/badge/ICD--10-6A6A6A?style=flat-square) ![RxNorm](https://img.shields.io/badge/RxNorm-6A6A6A?style=flat-square) ![HL7](https://img.shields.io/badge/HL7-6A6A6A?style=flat-square) ![Epic](https://img.shields.io/badge/Epic-6A6A6A?style=flat-square) ![Cerner](https://img.shields.io/badge/Cerner-6A6A6A?style=flat-square) ![Veradigm](https://img.shields.io/badge/Veradigm-6A6A6A?style=flat-square) ![athenahealth](https://img.shields.io/badge/athenahealth-6A6A6A?style=flat-square)
<!-- stack:end -->

## Education

**M.P.H., Biostatistics** (2015) and **B.A., English Literature** (2007), University of Wisconsin-Madison. Graduate Certificate in Patient Safety / Human Factors Engineering (2015).

---

<p align="center"><sub>Title, stack, writing, and research above are generated from <a href="https://zaherkarp.com">zaherkarp.com</a>'s sources of truth (see the <a href="https://zaherkarp.com/colophon/">colophon</a>). · Madison, WI · Remote</sub></p>
