# 🌍 AQI Oracle - Air Quality Intelligence

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![ML](https://img.shields.io/badge/MachineLearning-Model-green)

A **machine learning-powered web application** that predicts Air Quality Index (AQI) for Indian cities using **Random Forest regression** and historical pollutant data.

---

## 🌍 Why This Project?

Air pollution is a major issue in India. This project helps:

* Predict AQI levels for better planning
* Provide health recommendations
* Analyze pollution trends using data science

---

## 🚀 Live Demo

👉 https:[//your-app.streamlit.app *(add after deployment)*](://aqi-oracle-ypzzz6uypkpwp4tskv8qhb.streamlit.app/)

---

## ✨ Features

### 🤖 Machine Learning

* Compared multiple models:

  * Linear Regression
  * Random Forest
  * XGBoost
* **Final Model: Random Forest (R² ≈ 0.88)**
* Handles non-linear AQI patterns
* Fast predictions (<100ms)

---

### 📍 Input

* City selection
* Date selection

---

### 📊 Output

* AQI prediction (0–500 scale)
* AQI category (Good → Severe)
* Health recommendations

---

### 📈 Visualizations

* AQI Trend over time
* Pollutant Radar Chart
* City Comparison
* Monthly Patterns
* PM2.5 vs AQI Scatter

---

## 📸 Screenshots

### Dashboard

![Dashboard](images/ui.png)

### Prediction Output

![Prediction](images/output.png)

### Charts

![Charts](images/charts.png)

---

## 📁 Project Structure

```bash
aq-oracle/
│
├── app.py                  # Streamlit UI
├── AQI_PREDICTION.ipynb   # Model experimentation
├── aqi_model.pkl          # Trained Random Forest model
├── scaler.pkl             # (optional)
│
├── data/
│   └── city_day.csv
│
├── docs/
│   ├── project_overview.md
│   └── api.md
│
├── .streamlit/
│   └── config.toml
│
├── Dockerfile
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📊 Model Comparison

| Model             | R² Score | Notes            |
| ----------------- | -------- | ---------------- |
| Linear Regression | 0.72     | Baseline         |
| Random Forest     | 0.88 ✅   | Selected         |
| XGBoost           | 0.87     | High performance |

👉 **Final Model Used in App: Random Forest**

---

## 📈 Model Performance

| Metric        | Value     |
| ------------- | --------- |
| R² Score      | ~0.88     |
| MAE           | ~20 AQI   |
| Training Data | 29K+ rows |
| Features      | 15        |

---

## ⚙️ How It Works

```
User Input → Data Processing → ML Model → Prediction → Visualization
```

---

## 🛠️ Installation

### 1. Clone repo

```bash
git clone https://github.com/supriyabajpai-ds/aq-oracle.git
cd aq-oracle
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add dataset

Place:

```
data/city_day.csv
```

### 4. Run app

```bash
streamlit run app.py
```

---

## 📦 Requirements

```
streamlit
pandas
numpy
plotly
scikit-learn
requests
joblib
```

---

## 🌐 Deployment

### Streamlit Cloud

1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Select repo + `app.py`
4. Deploy 🚀

---

## 🧠 Key Highlights

* End-to-end ML project
* Real-world dataset
* Interactive dashboard
* Clean UI with animations
* Deployment-ready

---

## 📋 Future Improvements

* Add XGBoost deployment
* Real-time API integration
* Mobile app
* Multi-country support

---

## 👤 Author

**Supriya Bajpai**

* GitHub: https://github.com/supriyabajpai-ds
* LinkedIn: https://www.linkedin.com/in/supriya-bajpai-17b419327
* Email: [2k23.csdsc2311724@gmail.com](mailto:2k23.csdsc2311724@gmail.com)

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🔗 Share it
* 🐛 Report issues

---

**Made with ❤️ using Machine Learning + Streamlit**
