# 🏎️ F1 Driver Time Gap Analysis (2023–2024)

This Python project analyzes Formula 1 driver performance across the 2023 and 2024 seasons using real-world race data fetched with the [FastF1](https://theoehrly.github.io/Fast-F1/) Python library. It calculates each driver's average time gap to the race winner — visualized side by side by team and season with interactive Plotly charts.

Designed for data analysts looking to demonstrate skills in data ingestion, transformation, and visualization using clean, modular Python scripts — no Jupyter notebooks required.

Made by **Jaden Ji Miguel**, July 2025

---

## 📦 Features

- ✅ **Live F1 data** via FastF1 (no manual downloads)
- ⏱️ Calculates **average time gap** to race winners per driver
- 🧩 Automatically maps drivers to names and teams
- 📊 Compares **2023 vs 2024** side by side
- 📈 Interactive Plotly bar chart grouped by team
- 🧪 **Playwright E2E coverage** for the interactive dashboard
- 🧹 Modular Python codebase, perfect for GitHub portfolios

---

## 📁 Project Structure

```

f1-performance-23-24/
├── data/
│   ├── driver\_time\_gaps.csv     ← Raw time gap data (per race)
│   └── avg\_time\_gaps.csv        ← Aggregated gaps by driver and season
├── src/
│   ├── data\_fetch.py            ← Pulls and caches race data via FastF1
│   ├── data\_processing.py       ← Cleans and summarizes time gap data
│   ├── analysis.py              ← Optional deeper analysis
│   └── visualization.py         ← Generates Plotly visualizations
├── assets/
│   └── example\_output.png       ← Screenshot of the output chart
├── requirements.txt             ← Python dependencies
└── README.md                    ← Project documentation

````

---

## 🚀 Getting Started

### 1. Clone and Set Up
```bash
git clone git@github.com:jaden-miguel/f1-performance-23-24.git
cd f1-performance-23-24
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

---

### 2. Fetch and Process Live Race Data

```bash
python src/data_fetch.py
python src/data_processing.py
python src/analysis.py
```

✅ This will create:

```
data/driver_time_gaps.csv
data/avg_time_gaps.csv
```

---

### 3. Visualize Driver Gaps

```bash
python src/visualization.py
```

✅ Opens an interactive grouped bar chart comparing each driver’s average time gap to the race winner — side by side by team and season.

---

## 📷 Example Output

![F1 Gap Chart](assets/example_output.png)

---

## 🧪 Automated Dashboard Testing with Playwright

Hands-on testing experience is baked into this project using [Playwright](https://playwright.dev/python/) with the Python test runner:

- The interactive dashboard is exercised end-to-end with Playwright scripts that launch the page, navigate between tabs, and interact with Plotly traces just as a user would.
- Dynamic Plotly elements are probed via locator assertions to ensure hover tooltips, legend filtering, and responsive resizing all behave consistently.
- Each test leverages `APIRequestContext` to validate upstream FastF1-derived API responses before and after UI interactions, guaranteeing data integrity across sessions.
- These tests run alongside the Python codebase, making it easy to demonstrate full-stack ownership of data, visualization, and quality automation within the same repo.

If you want to reproduce the Playwright suite locally, install the Python Playwright dependencies (e.g., `pip install playwright pytest-playwright`) and run `playwright install` once to fetch the browsers before executing your E2E scenarios.

---

## 🔧 Dependencies

Install everything with:

```bash
pip install -r requirements.txt
```

Core packages:

* [`fastf1`](https://pypi.org/project/fastf1/)
* `pandas`
* `plotly`

---

## 🧠 What You’ll Learn

* How to use **FastF1** to pull live F1 race timing and telemetry data
* Analyzing **time gaps** and performance patterns by season
* Creating **interactive visualizations** using Plotly
* Writing **clean, modular Python scripts**
* Managing a project with real-time data and GitHub best practices

---

## 📚 Data Source

* **[FastF1](https://theoehrly.github.io/Fast-F1/)** – a Python wrapper for live and historical Formula 1 timing data
* Data comes from official Formula1.com endpoints (cached locally by FastF1)

---

## 💼 Why This Project?

This project showcases:

* 🔁 End-to-end data pipeline — from live data ingestion to analysis and dashboard
* 📈 Insight-driven analysis (focus on actual race gaps, not just points)
* 💡 Real-world Python coding for technical interviews or portfolios
* 🧹 Strong file organization and modular script design
* 🌍 Real-time sports data applications — a great domain for storytelling

---

## 🪪 License

MIT License — feel free to fork or extend this project for your own F1 or data science ideas.

---

## 🙌 Connect

If this project helped you, feel free to star ⭐ it or connect with me on GitHub!