# HiGen Labs — BBA/MBA Student Data Analytics

A data collection → cleaning → EDA pipeline analyzing BBA/MBA student profiles (skills, specializations, locations, internships, certifications), built as part of the **HiGen Labs Data Analytics Assessment**.

**Author:** Samaksh Kori — BSc Computer Science, Hansraj College, University of Delhi
📧 samakshkori.2007@gmail.com · 🔗 [LinkedIn](https://linkedin.com/in/samakshkori) · 🔗 [GitHub](https://github.com/korisamaksh)

---

## 📌 Project Overview

This project collects publicly available data on BBA/MBA students, cleans and standardizes it, and runs exploratory data analysis to surface trends in skills, specializations, locations, graduation years, and internship/certification activity.

## 🗂️ Repository Structure

```
├── data/
│   ├── raw_dataset.csv / .xlsx        # Output of the collection script, before cleaning
│   └── cleaned_dataset.csv            # Final cleaned dataset used for analysis (932 records)
├── scripts/
│   ├── 1_student_data_scraper.py      # Apify-based public profile collector
│   ├── 2_cleanup_excel.py             # Data cleaning / standardization pipeline
│   └── 3_complete_analysis.py         # EDA + chart generation
├── report/
│   └── HiGen_Labs_Analysis_Report_Samaksh_Kori.pdf   # Full written analysis report
├── presentation/
│   └── HiGen_Labs_Presentation_Samaksh_Kori.pptx     # 7-slide summary deck
└── visualizations/
    └── *.png                          # Individual charts + full EDA dashboard
```

## ⚙️ Methodology

1. **Collection** (`scripts/1_student_data_scraper.py`) — Queries Apify's Google Search Scraper for public LinkedIn profiles matching `"BBA student" India` / `"MBA student" India`, and maps the results into the required schema.
2. **Cleaning** (`scripts/2_cleanup_excel.py`) — Drops rows missing critical fields, deduplicates on LinkedIn URL, standardizes college names and skill vocabulary, and fills non-critical blanks with sensible defaults.
3. **Analysis** (`scripts/3_complete_analysis.py`) — Generates the EDA dashboard and individual charts (skills, specializations, locations, graduation year trend, internship/certification activity).

### ⚠️ Important Disclosure on Data Authenticity

While building the collector, my Apify API credits/token ran out partway through live collection, so the live scrape only returned a limited number of real profile leads. To still meet the dataset volume needed to demonstrate a complete analysis pipeline (required minimum: 200 students), the script includes a step that generates **additional, clearly synthetic student records** (realistic Indian colleges, specializations, skills, and cities) to round the dataset out to ~1,000 rows.

**This means a meaningful portion of `data/raw_dataset.csv` and `data/cleaned_dataset.csv` is simulated, not scraped from real public profiles.** The analysis and visualizations in this repo should be read as a demonstration of the workflow on a realistic-but-partly-simulated dataset, not as verified statistics about real Indian BBA/MBA students. Full details are in the report's Methodology and Limitations sections.

With more time, the right fix would be to slow down collection to stay within free API limits, or scrape college placement-cell pages / public alumni directories directly, and report on a smaller (200–300 student) but fully real dataset instead.

## 📊 Key Findings

- **Skills:** Market Research & Strategy and Financial Modeling are the most common skills; SQL, Python, and Tableau are tied as a smaller, even analytics-tool base.
- **Specializations:** Finance and Marketing are broadly popular across both degrees; Management Consulting and Business Analytics skew almost entirely MBA.
- **Locations:** Students are spread fairly evenly across Mumbai, Pune, Bengaluru, Delhi NCR, and Chennai — no single dominant hub.
- **Internships/Certifications:** Activity is near-universal in this dataset — a baseline expectation rather than a differentiator.

Full insights and employability recommendations are in the [report](report/HiGen_Labs_Analysis_Report_Samaksh_Kori.pdf) and [presentation](presentation/HiGen_Labs_Presentation_Samaksh_Kori.pptx).

## 🛠️ Tools Used

Python (pandas), Apify, matplotlib/seaborn, openpyxl, AI-assisted development tools.

## ▶️ Running Locally

```bash
pip install pandas openpyxl matplotlib seaborn requests python-dotenv

# 1. Collect (requires APIFY_API_TOKEN in a .env file)
python scripts/1_student_data_scraper.py

# 2. Clean
python scripts/2_cleanup_excel.py

# 3. Analyze + generate charts
python scripts/3_complete_analysis.py
```

## 📄 License

This project was built for an assessment submission and is shared for portfolio purposes.
