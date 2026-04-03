# 🌍 AQI Oracle - Air Quality Intelligence

A machine learning-powered web application that predicts Air Quality Index (AQI) for Indian cities using **Random Forest** regression and real-time pollutant data integration.

**Live Demo**: [Deploy on Streamlit Cloud](#deployment)

---

## ✨ Features

### 🤖 Machine Learning
- **Random Forest Model** - Non-linear AQI prediction with 88% accuracy (R² = 0.88)
- **Used Multiple Model**- XGBoost, Linear Regression and Random Forest
- **Trained on 29K+ records** from Indian cities
- **Automatic feature importance** calculation
- **Fast inference** (<100ms predictions)

### 📍 Geographic Coverage
- **13 pre-loaded Indian cities** with coordinates
- **Live API support** for any location (OpenWeatherMap ready)
- **Graceful fallback** to historical averages for missing data
- **Automatic city detection** from dropdown

### 🎯 Real-Time Pollutants
Tracks 12 key pollutants:
- PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene

### 🎨 Beautiful UI
- **Cyberpunk aesthetic** with dark theme
- **3D rotating globe** hero section
- **Animated gauge chart** showing AQI visualization
- **Color-coded predictions** (Green → Yellow → Orange → Red → Pink)
- **5 interactive charts**:
  - AQI trend over time
  - Pollutant radar chart
  - City comparison bar chart
  - Monthly seasonal patterns
  - PM2.5 vs AQI scatter plot
- **Responsive design** - works on desktop, tablet, mobile

### 📊 Data Analytics
- Historical AQI trends per city
- Best/worst recorded AQI values
- Monthly seasonal patterns
- Pollutant contribution analysis

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/supriyabajpai-ds/aqi-oracle.git
cd aqi-oracle
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Prepare data**
- Place `city_day.csv` in the project root
- CSV must have columns: Date, City, AQI, AQI_Bucket, and all 12 pollutants

4. **Run the app**
```bash
streamlit run aqi_oracle_v6_rf.py
```

5. **Open browser**
- Navigate to `http://localhost:8501`
- Select a city, pick a date
- Click "⟳ RUN PREDICTION"

---

## 📁 Project Structure

```bash
aq-oracle/
│
├── app.py                  # Streamlit UI application
├── train_model.py          # Model training script
├── model.pkl               # Trained ML model (XGBoost / Random Forest)
├── model_experiments.ipynb # Model comparison notebook
├── data/
│   └── city_day.csv        # Dataset used for training
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
---

## 📈 Model Performance

| Metric | Value |
|--------|-------|
| **R² Score** | 0.8830 |
| **MAE** | 19.86 AQI points |
| **Algorithm** | Random Forest (100 trees) |
| **Training Data** | 29,000+ samples |
| **Features** | 15 (12 pollutants + temporal) |
| **Prediction Time** | <100ms |

### Why Random Forest?
✅ Captures non-linear pollutant-AQI relationships  
✅ Handles feature interactions (PM2.5 × NO2)  
✅ No scaling needed (scale-invariant)  
✅ Robust to outliers  
✅ Automatic feature importance  

---

## 🌐 Live Data Integration

### OpenWeatherMap API (Optional)

To enable real-time pollutant data for missing cities:

1. **Sign up** at [openweathermap.org](https://openweathermap.org/api/air-pollution)
2. **Get free API key** (1000 calls/day)
3. **Update the function** in `aqi_oracle_v6_rf.py`:

```python
def fetch_live_pollutants(city_name):
    lat, lon = CITY_COORDS[city_name]
    api_key = "YOUR_API_KEY"
    
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url, timeout=5)
    data = response.json()
    
    components = data['list'][0]['components']
    return {
        'PM2.5': components.get('pm2_5', 0),
        'PM10': components.get('pm10', 0),
        # ... (rest of pollutants)
    }
```

---

## 🎛️ Configuration

### Supported Cities (with pre-loaded data)
Delhi, Mumbai, Bengaluru, Kolkata, Chennai, Hyderabad, Ahmedabad, Lucknow, Pune, Kanpur, Jaipur, Patna, Srinagar

### Customize Colors
Edit `aqi_info()` function in `aqi_oracle_v6_rf.py`:

```python
def aqi_info(v):
    if v <= 50:   return "#28a745", "GOOD", "..."        # Green
    if v <= 100:  return "#a3c639", "SATISFACTORY", "..."  # Yellow
    if v <= 200:  return "#f0ad4e", "MODERATE", "..."      # Orange
    if v <= 300:  return "#fd7e14", "POOR", "..."          # Red
    if v <= 400:  return "#dc3545", "VERY POOR", "..."     # Dark Red
    return "#ff3366", "SEVERE", "..."                       # Pink
```

### Adjust Model Parameters
Edit `train_random_forest_model()`:

```python
model = RandomForestRegressor(
    n_estimators=100,    # More trees = better but slower
    max_depth=15,        # Deeper = more overfitting risk
    random_state=42,     # For reproducibility
    n_jobs=-1            # Use all CPU cores
)
```

---

## 📊 Data Format

Your `city_day.csv` should have this structure:

```csv
Date,City,AQI,AQI_Bucket,PM2.5,PM10,NO,NO2,NOx,NH3,CO,SO2,O3,Benzene,Toluene,Xylene
2023-01-01,Delhi,285,POOR,183.9,256.9,58.4,108.4,167.0,9.2,3150.0,23.4,15.6,45.3,12.1,4.2
2023-01-02,Delhi,265,POOR,165.2,234.5,52.1,95.6,147.8,8.9,2980.0,21.1,14.2,42.1,11.5,3.9
...
```

**Requirements:**
- At least 1,000 rows (more = better)
- No missing Date or City values
- AQI values in range 0-500
- All 12 pollutants present (use median for missing values)

---

## 🔍 Features Explained

### Prediction Output
1. **Stat Cards** - City average, best, and worst recorded AQI
2. **Gauge Chart** - Large, color-coded prediction with scale
3. **Health Advice** - Specific guidance based on AQI level
4. **Info Chips** - City, date, and season reference

### Analytics Section
1. **AQI Trend** - Monthly averages over time
2. **Pollutant Radar** - 6-point radar showing each pollutant
3. **City Comparison** - Top 10 most polluted cities
4. **Monthly Pattern** - Seasonal variations
5. **PM2.5 vs AQI** - Correlation scatter plot

---

## 🛠️ Troubleshooting

### "Missing city_day.csv"
```bash
# Make sure CSV is in project root
ls -la city_day.csv
```

### "Insufficient training data"
```python
# Check data in CSV
import pandas as pd
df = pd.read_csv('city_day.csv')
print(df.shape)  # Should be (rows, columns)
print(df.isnull().sum())  # Check for missing values
```

### "Predictions don't look realistic"
- Check CSV for outliers (extreme AQI values)
- Verify pollutant values are in expected ranges
- Try retraining with more diverse data

### "Charts not rendering"
```bash
# Clear Streamlit cache
rm -rf ~/.streamlit/cache/
streamlit run aqi_oracle_v6_rf.py
```

---

## 📦 Requirements

```
streamlit==1.28.0
pandas==2.0.0
numpy==1.24.0
plotly==5.17.0
scikit-learn==1.3.0
requests==2.31.0
joblib==1.3.0
```

---

## 🌐 Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub** (see below)
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Click** "New app"
4. **Select** your repository and `aqi_oracle_v6_rf.py`
5. **Deploy!** ✅

### Option 2: Heroku
```bash
# Install Heroku CLI
heroku create aqi-oracle
git push heroku main
```

### Option 3: Docker
```bash
docker build -t aqi-oracle .
docker run -p 8501:8501 aqi-oracle
```

---

## 🔑 Key Cities & Coordinates

| City | Latitude | Longitude |
|------|----------|-----------|
| Delhi | 28.6139 | 77.2090 |
| Mumbai | 19.0760 | 72.8777 |
| Bengaluru | 12.9716 | 77.5946 |
| Kolkata | 22.5726 | 88.3639 |
| Chennai | 13.0827 | 80.2707 |
| Hyderabad | 17.3850 | 78.4867 |
| Ahmedabad | 23.0225 | 72.5714 |
| Lucknow | 26.8467 | 80.9462 |
| Pune | 18.5204 | 73.8567 |

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Gauge Charts](https://plotly.com/python/gauge-charts/)
- [Scikit-learn Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)
- [OpenWeatherMap Air Pollution API](https://openweathermap.org/api/air-pollution)
- [AQI Explanation](https://www.epa.gov/air-quality/air-quality-index-aqi)

---

## 📋 Roadmap

- [ ] XGBoost model for comparison
- [ ] User authentication & saved predictions
- [ ] Historical prediction accuracy tracking
- [ ] Mobile app (React Native)
- [ ] Multi-country support
- [ ] Real-time data ingestion pipeline
- [ ] Advanced feature engineering
- [ ] Ensemble models
- [ ] Prediction confidence intervals
- [ ] API endpoint for predictions

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Supriya Bajpai**
- GitHub: [@supriyabajpai-ds](https://github.com/supriyabajpai-ds)
- Email: 2k23.csdsc2311724@gmail.com
- LinkedIn: [Supriya Bajpai](https://linkedin.com/in/supriyabajpai-17b419327)

---

## 🙏 Acknowledgments

- **Data Source**: Indian government air quality databases
- **Libraries**: Streamlit, Plotly, scikit-learn, pandas
- **Inspiration**: OpenWeatherMap, EPA AQI scale

---

## 📞 Support

If you have questions or issues:

1. **Check the docs** in `/docs` folder
2. **Search existing issues** on GitHub
3. **Create a new issue** with:
   - Description of problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Python & package versions
   - Screenshots (if applicable)

---

## ⭐ Show Your Support

If this project helped you, please:
- ⭐ Star the repository
- 🔗 Share with others
- 💬 Provide feedback
- 🐛 Report bugs
- 📝 Suggest improvements

---

**Made with ❤️ by Supriya Bajpai**

*Predicting air quality, one city at a time.* 🌍✨
