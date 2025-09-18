# 📊 KPI Analytics Dashboard (Streamlit)
An interactive analytics dashboard built with Streamlit that supports CSV upload, parameterized filters, segment analysis, and exportable snapshots for quick weekly reviews.[3]

## ✨ Features
- File upload for CSV data with basic validation of required columns (Date, Visitors, Orders, Revenue, Segment).[3]
- Interactive filters: date range, multi-select segments, and smart defaults.[3]
- Visualizations with built-in Streamlit and Plotly (line, pie, bar).[3]
- KPI cards: Visitors, Orders, Revenue, Conversion Rate, and helpful deltas.[3]
- Session state to remember selections and a cached sample dataset for performance.[3]
- One‑click exports: filtered data, weekly summary, and segment breakdown as CSV.[3]

## 🧪 Live Demo
Try it here: https://kpi-analytics-dashboard-vut8xjdrdgz5af4sxwq9vx.streamlit.app/.[8]

## 📦 Tech Stack
- Streamlit for UI and app framework.[3]
- Pandas for data loading and transforms.[3]
- Plotly Express for interactive charts.[3]

## 🛠️ Getting Started (Local)
Prerequisites:
- Python 3.9+ recommended.[3]

Clone and run:
1) Clone the repo:
```
git clone https://github.com/Saifali44884488/kpi-analytics-dashboard.git
cd kpi-analytics-dashboard
```

2) Install dependencies:
```
pip install -r requirements.txt
```

3) Start the app:
```
streamlit run app.py
```


## 📄 Data Format
The app expects a CSV with at least these columns:
- Date (YYYY-MM-DD or ISO‑8601)  
- Visitors (int)  
- Orders (int)  
- Revenue (number)  
- Segment (e.g., Mobile, Desktop)  
These columns enable all filters, KPIs, and visuals to function properly.[3]

## 🚀 Deploy (Streamlit Community Cloud)
1) Push app.py and requirements.txt to your main branch.[13]
2) Go to Streamlit Community Cloud, select “Deploy a public app from GitHub,” choose your repo, branch main, and file path app.py, then Deploy.[13]
3) After the build completes, copy the public URL and replace DEMO_LINK above.[8]

## 🧰 Requirements
Minimal requirements.txt for this project:
```
streamlit
pandas
plotly
```
Keeping the list minimal avoids pulling in unrelated local packages and speeds up cloud builds.[14][15]

## 🔒 Notes
- Don’t commit large data files or secrets; use a .gitignore to exclude venv/, __pycache__/, and local caches.[10]
- If a ModuleNotFoundError appears during deploy, add the missing package to requirements.txt and redeploy.[13]

## 📜 License
Choose a license (e.g., MIT) if you plan to share or fork widely; add LICENSE to the repo.[10]
