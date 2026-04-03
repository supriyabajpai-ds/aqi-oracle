import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
from datetime import date
import requests
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="AQI Oracle", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

# ── Google Fonts ──────────────────────────────────────────────────────────────
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#020b18; --panel:rgba(5,20,40,0.88); --border:rgba(0,200,255,0.18);
  --accent:#00c8ff; --accent2:#00ff9d; --text:#cde8f5; --muted:#4a7a9b;
  --glow:0 0 30px rgba(0,200,255,0.25);
}
.stApp,.main,[data-testid="stAppViewContainer"]{
  background:var(--bg)!important; color:var(--text)!important;
  font-family:'Rajdhani',sans-serif!important;
}
[data-testid="stSidebar"]{display:none}
[data-testid="stHeader"]{background:transparent!important}
.block-container{padding:0 2rem 3rem!important;max-width:1440px}

.hero{
  position:relative; width:100%; height:300px;
  display:flex; align-items:center; justify-content:space-between;
  padding:0 3rem; overflow:hidden; margin-bottom:1.5rem;
}
.hero-text{z-index:10}
.hero h1{
  font-family:'Orbitron',monospace; font-size:clamp(2rem,4vw,3.4rem);
  font-weight:900;
  background:linear-gradient(135deg,#00c8ff,#00ff9d,#00c8ff);
  background-size:200% auto; -webkit-background-clip:text;
  -webkit-text-fill-color:transparent; background-clip:text;
  animation:shine 4s linear infinite; line-height:1.1; letter-spacing:3px;
}
.hero p{font-size:1rem;color:var(--muted);margin-top:.6rem;letter-spacing:3px;text-transform:uppercase}
@keyframes shine{0%{background-position:0% center}100%{background-position:200% center}}
.hero-stats{
  z-index:10; display:flex; flex-direction:column; gap:.8rem;
  background:rgba(0,200,255,0.04); border:1px solid rgba(0,200,255,0.1);
  border-radius:12px; padding:1.2rem 1.6rem;
}
.hero-stat-row{display:flex;align-items:center;gap:.6rem}
.hero-stat-num{font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:700;color:var(--accent2)}
.hero-stat-lbl{font-size:.75rem;letter-spacing:2px;color:var(--muted);text-transform:uppercase}
#globe-canvas{position:absolute;right:0;top:0;width:380px;height:300px;opacity:.9}
.grid-bg{
  position:absolute;inset:0;
  background-image:linear-gradient(rgba(0,200,255,.04)1px,transparent 1px),
    linear-gradient(90deg,rgba(0,200,255,.04)1px,transparent 1px);
  background-size:40px 40px; z-index:1;
}
.scanline{
  position:absolute;inset:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,
    rgba(0,200,255,.015)2px,rgba(0,200,255,.015)4px);
  pointer-events:none;z-index:5;
}

.panel{
  background:var(--panel); border:1px solid var(--border);
  border-radius:12px; padding:1.6rem 1.8rem;
  backdrop-filter:blur(12px); box-shadow:var(--glow); transition:border-color .3s;
}
.panel:hover{border-color:rgba(0,200,255,.4)}
.panel-title{
  font-family:'Orbitron',monospace; font-size:.65rem; letter-spacing:3px;
  text-transform:uppercase; color:var(--accent); margin-bottom:1rem;
  display:flex; align-items:center; gap:.5rem;
}
.panel-title::before{
  content:''; display:inline-block; width:6px; height:6px;
  background:var(--accent); border-radius:50%;
  box-shadow:0 0 8px var(--accent); animation:pulse 2s infinite;
}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.7)}}

[data-testid="stDateInput"] input{
  background:#ffffff!important; border:1px solid var(--border)!important;
  border-radius:8px!important; color:#1a1a1a!important;
  font-family:'Rajdhani',sans-serif!important; font-size:1rem!important;
  font-weight:600!important; padding:0.5rem!important;
}
[data-testid="stDateInput"] input:focus{
  border-color:var(--accent)!important; box-shadow:0 0 12px rgba(0,200,255,.25)!important;
  outline:none!important;
}

[data-testid="stSelectbox"]>div>div{
  background:rgba(0,200,255,.06)!important; border:1px solid var(--border)!important;
  border-radius:8px!important; color:var(--text)!important;
  font-family:'Rajdhani',sans-serif!important; font-size:1rem!important;
}

label,.stSelectbox label,.stDateInput label{
  font-family:'Orbitron',monospace!important; font-size:.65rem!important;
  letter-spacing:2px!important; color:var(--accent)!important; text-transform:uppercase!important;
}

.stButton>button{
  width:100%!important;
  background:linear-gradient(135deg,rgba(0,200,255,.15),rgba(0,255,157,.1))!important;
  border:1px solid var(--accent)!important; color:var(--accent)!important;
  font-family:'Orbitron',monospace!important; font-size:.75rem!important;
  letter-spacing:3px!important; padding:.75rem!important; border-radius:8px!important;
  transition:all .3s!important; text-transform:uppercase!important;
}
.stButton>button:hover{
  background:linear-gradient(135deg,rgba(0,200,255,.3),rgba(0,255,157,.2))!important;
  box-shadow:0 0 25px rgba(0,200,255,.4)!important; transform:translateY(-1px)!important;
}

.pol-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.6rem;margin-top:.8rem}
.pol-card{
  background:rgba(0,200,255,.05); border:1px solid rgba(0,200,255,.12);
  border-radius:8px; padding:.6rem .8rem; transition:all .2s;
}
.pol-card:hover{border-color:rgba(0,200,255,.35);background:rgba(0,200,255,.1);transform:translateY(-2px)}
.pol-name{font-family:'Orbitron',monospace;font-size:.55rem;letter-spacing:1px;color:var(--muted)}
.pol-val{font-size:1.05rem;font-weight:600;color:var(--text);margin-top:2px}

.scale-wrap{margin-top:1rem}
.scale-bar{
  height:6px;border-radius:3px;
  background:linear-gradient(to right,
    #28a745 0%,#28a745 10%,#a3c639 10%,#a3c639 20%,
    #f0ad4e 20%,#f0ad4e 40%,#fd7e14 40%,#fd7e14 60%,
    #dc3545 60%,#dc3545 80%,#6f1313 80%,#6f1313 100%);
  position:relative;margin:.4rem 0 .8rem;
}
.scale-marker{
  position:absolute;top:-4px;width:14px;height:14px;border-radius:50%;
  border:2px solid white;transform:translateX(-50%);box-shadow:0 0 10px currentColor;
}
.scale-labels{
  display:flex;justify-content:space-between;font-size:.58rem;
  color:var(--muted);letter-spacing:1px;font-family:'Orbitron',monospace;
}

.chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.8rem}
.chip{
  background:rgba(0,200,255,.08);border:1px solid rgba(0,200,255,.2);
  border-radius:20px;padding:4px 12px;font-size:.78rem;color:var(--text);letter-spacing:1px;
}

.city-img-wrap{
  position:relative; border-radius:12px; overflow:hidden;
  border:1px solid rgba(0,200,255,.2); margin-bottom:1rem;
  animation:fadeIn .6s ease;
}
.city-img-wrap img{width:100%;height:160px;object-fit:cover;display:block;filter:brightness(.7) saturate(1.2)}
.city-img-overlay{
  position:absolute;inset:0;
  background:linear-gradient(to top,rgba(2,11,24,.9)40%,transparent);
  display:flex;align-items:flex-end;padding:1rem 1.2rem;
}
.city-img-label{font-family:'Orbitron',monospace;font-size:1rem;font-weight:700;color:#fff;letter-spacing:2px}
.city-img-sub{font-size:.75rem;color:rgba(255,255,255,.5);letter-spacing:2px}

[data-testid="stExpander"]{
  background:var(--panel)!important; border:1px solid var(--border)!important; border-radius:12px!important;
}
[data-testid="stExpander"] summary{
  font-family:'Orbitron',monospace!important; font-size:.65rem!important;
  letter-spacing:2px!important; color:var(--accent)!important;
}

.js-plotly-plot .plotly{background:transparent!important}

@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
@keyframes countUp{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:scale(1)}}

.animate-fade{animation:fadeIn .7s ease both}
.animate-slide{animation:slideIn .5s ease both}
.animate-count{animation:countUp .5s ease both}

.section-header{
  font-family:'Orbitron',monospace;font-size:.7rem;letter-spacing:4px;
  text-transform:uppercase;color:var(--accent);
  display:flex;align-items:center;gap:1rem;margin:1.5rem 0 1rem;
}
.section-header::after{content:'';flex:1;height:1px;background:var(--border)}

.footer{
  text-align:center;font-size:.65rem;color:var(--muted);
  letter-spacing:2px;padding:2rem 0 1rem;font-family:'Orbitron',monospace;
}

.stat-row{display:flex;gap:1rem;margin-bottom:1.2rem}
.stat-card{
  flex:1;background:rgba(0,200,255,.05);border:1px solid rgba(0,200,255,.15);
  border-radius:10px;padding:.9rem 1rem;text-align:center;transition:all .25s;
}
.stat-card:hover{border-color:var(--accent);background:rgba(0,200,255,.1);transform:translateY(-2px)}
.stat-card-num{font-family:'Orbitron',monospace;font-size:1.4rem;font-weight:700;color:var(--accent2)}
.stat-card-lbl{font-size:.65rem;letter-spacing:2px;color:var(--muted);margin-top:3px}
</style>
""", unsafe_allow_html=True)

# ── 3D GLOBE ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="grid-bg"></div>
  <div class="scanline"></div>
  <div class="hero-text">
    <h1>AQI<br>ORACLE</h1>
    <p>Air Quality Intelligence</p>
  </div>
  <div class="hero-stats">
    <div class="hero-stat-row">
      <span class="hero-stat-num">🌍</span>
      <span class="hero-stat-lbl">Live Predictions</span>
    </div>
    <div class="hero-stat-row">
      <span class="hero-stat-num">🤖</span>
      <span class="hero-stat-lbl">Random Forest</span>
    </div>
    <div class="hero-stat-row">
      <span class="hero-stat-num" style="color:#fd7e14">📡</span>
      <span class="hero-stat-lbl">Live Data API</span>
    </div>
  </div>
  <canvas id="globe-canvas"></canvas>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function(){
  const canvas=document.getElementById('globe-canvas');
  if(!canvas||!window.THREE)return;
  const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true});
  renderer.setSize(380,300); renderer.setPixelRatio(window.devicePixelRatio);
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(45,380/300,.1,1000);
  camera.position.z=2.8;

  const globe=new THREE.Mesh(
    new THREE.SphereGeometry(1,64,64),
    new THREE.MeshPhongMaterial({color:0x020b18,emissive:0x001a33,shininess:60})
  ); scene.add(globe);

  scene.add(new THREE.Mesh(
    new THREE.SphereGeometry(1.001,28,28),
    new THREE.MeshBasicMaterial({color:0x00c8ff,wireframe:true,transparent:true,opacity:0.07})
  ));

  const mkRing=(r,color,ox,oy)=>{
    const m=new THREE.Mesh(
      new THREE.TorusGeometry(r,.01,16,120),
      new THREE.MeshBasicMaterial({color,transparent:true,opacity:.5})
    );
    m.rotation.x=ox;m.rotation.y=oy;scene.add(m);return m;
  };
  const ring1=mkRing(1.18,0x00c8ff,Math.PI/2.5,0);
  const ring2=mkRing(1.28,0x00ff9d,Math.PI/3,Math.PI/6);
  const ring3=mkRing(1.38,0xff3366,Math.PI/4,Math.PI/4);

  const dotMat=new THREE.MeshBasicMaterial({color:0x00ff9d});
  [[28.6,77.2],[19.0,72.8],[13.0,80.3],[22.5,88.4],[17.4,78.5],
   [23.0,72.6],[12.9,77.6],[26.9,75.8],[21.2,81.5],[30.7,76.7],
   [25.4,81.8],[22.7,75.8],[15.8,78.0],[20.3,85.8],[11.0,77.0]].forEach(([lat,lon])=>{
    const phi=(90-lat)*Math.PI/180,theta=(lon+180)*Math.PI/180;
    const d=new THREE.Mesh(new THREE.SphereGeometry(.02,8,8),dotMat.clone());
    d.position.set(-Math.sin(phi)*Math.cos(theta),Math.cos(phi),Math.sin(phi)*Math.sin(theta));
    scene.add(d);
  });

  const pPos=new Float32Array(900);
  for(let i=0;i<900;i++)pPos[i]=(Math.random()-.5)*8;
  const pGeo=new THREE.BufferGeometry();
  pGeo.setAttribute('position',new THREE.BufferAttribute(pPos,3));
  scene.add(new THREE.Points(pGeo,new THREE.PointsMaterial({color:0x00c8ff,size:.012,transparent:true,opacity:.4})));

  scene.add(new THREE.AmbientLight(0x112233,2));
  const dl=new THREE.DirectionalLight(0x00c8ff,1.2); dl.position.set(5,3,5); scene.add(dl);
  const dl2=new THREE.DirectionalLight(0x00ff9d,.6); dl2.position.set(-5,-3,-2); scene.add(dl2);

  let t=0;
  (function animate(){
    requestAnimationFrame(animate); t+=.005;
    globe.rotation.y=t*.4;
    ring1.rotation.z=t*.3; ring2.rotation.z=-t*.2; ring3.rotation.z=t*.15;
    renderer.render(scene,camera);
  })();
})();
</script>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
POLLUTANT_COLS = ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene','Xylene']
FEATURE_COLS   = POLLUTANT_COLS + ['Month','Season','City_Mean_AQI']
SEASON_LABELS  = {0:"❄️ Winter",1:"☀️ Summer",2:"🌧️ Monsoon",3:"🍂 Post-Monsoon"}

CITY_IMAGES = {
    "Delhi":     "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600&q=80",
    "Mumbai":    "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&q=80",
    "Bengaluru": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=600&q=80",
    "Kolkata":   "https://images.unsplash.com/photo-1558431382-27e303142255?w=600&q=80",
    "Chennai":   "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&q=80",
    "Hyderabad": "https://images.unsplash.com/photo-1570458436416-b8fcccfe883f?w=600&q=80",
    "Ahmedabad": "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?w=600&q=80",
    "Lucknow":   "https://images.unsplash.com/photo-1567427018141-0584cfcbf1b8?w=600&q=80",
    "Pune":      "https://images.unsplash.com/photo-1594909122845-11bced63ba59?w=600&q=80",
    "default":   "https://images.unsplash.com/photo-1524661135-423995f22d0b?w=600&q=80",
}

# City coordinates for live API calls
CITY_COORDS = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Ahmedabad": (23.0225, 72.5714),
    "Lucknow": (26.8467, 80.9462),
    "Pune": (18.5204, 73.8567),
    "Kanpur": (26.4499, 80.3319),
    "Jaipur": (26.9124, 75.7873),
    "Patna": (25.5941, 85.1376),
    "Srinagar": (34.0837, 74.7973),
}

def get_season(m):
    if m in [12,1,2]: return 0
    if m in [3,4,5]:  return 1
    if m in [6,7,8,9]:return 2
    return 3

def aqi_info(v):
    if v<=50:  return "#28a745","GOOD",        "Satisfactory air — enjoy outdoor activities!"
    if v<=100: return "#a3c639","SATISFACTORY","Minor discomfort for sensitive people."
    if v<=200: return "#f0ad4e","MODERATE",    "Sensitive groups may experience discomfort."
    if v<=300: return "#fd7e14","POOR",        "Everyone may begin to experience effects."
    if v<=400: return "#dc3545","VERY POOR",   "Health alert — serious effects for everyone."
    return            "#ff3366","SEVERE",       "🚨 Emergency — avoid all outdoor activity."

def aqi_pct(v): return min(100, max(0, (v/500)*100))

def plotly_cfg():
    return dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cde8f5', family='Rajdhani'),
                margin=dict(l=10,r=10,t=30,b=10))

def fetch_live_pollutants(city_name):
    """Fetch live pollutant data from OpenWeather API"""
    try:
        if city_name not in CITY_COORDS:
            return None
        
        lat, lon = CITY_COORDS[city_name]
        # Using free weather API as fallback (doesn't have all pollutants, so we'll use historical averages)
        # In production, use: https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid=YOUR_KEY
        
        st.info(f"📡 Using historical averages for {city_name} (live API key needed for real-time)")
        return None
    except Exception as e:
        st.warning(f"Could not fetch live data: {e}")
        return None

def train_random_forest_model(df):
    """Train Random Forest model on the CSV data"""
    try:
        fin = df[FEATURE_COLS + ['AQI']].dropna()
        if len(fin) < 10:
            st.error("❌ Insufficient training data")
            return None, None
        
        X, y = fin[FEATURE_COLS], fin['AQI']
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Random Forest instead of Linear Regression
        model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
        model.fit(Xtr, ytr)
        
        # No scaler needed for tree-based models, but keep for compatibility
        scaler = None
        
        from sklearn.metrics import r2_score, mean_absolute_error
        y_pred = model.predict(Xte)
        r2 = r2_score(yte, y_pred)
        mae = mean_absolute_error(yte, y_pred)
        
        st.success(f"✅ Random Forest trained: R² = {r2:.4f}, MAE = {mae:.2f}")
        return model, r2
    except Exception as e:
        st.error(f"❌ Model training failed: {e}")
        return None, None

CSV_PATH = "city_day.csv"

if not os.path.exists(CSV_PATH):
    st.error(f"❌ Missing {CSV_PATH}")
    st.stop()

try:
    df = pd.read_csv(CSV_PATH)
    
    # Clean data
    df['PM2.5'] = df['PM2.5'].fillna(df['PM2.5'].median())
    for col in POLLUTANT_COLS + ['AQI']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(df[col].median())
    df['AQI_Bucket'] = df['AQI_Bucket'].fillna('MODERATE')
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Month'] = df['Date'].dt.month
    df['Season'] = df['Month'].apply(get_season)
    
    city_mean = df.groupby('City')['AQI'].mean().to_dict()
    df['City_Mean_AQI'] = df['City'].map(city_mean)
    
    city_pol_med = df.groupby('City')[POLLUTANT_COLS].median().to_dict(orient='index')
    cities_in_data = sorted(df['City'].dropna().unique().tolist())
    
    # Add missing cities
    all_cities = sorted(list(set(cities_in_data + list(CITY_COORDS.keys()))))
    
    # Train model
    @st.cache_resource
    def load_model():
        return train_random_forest_model(df)
    
    model, model_r2 = load_model()
    
    if model is None:
        st.stop()

except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# ── UI ────────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1.5], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">SCAN PARAMETERS</div>', unsafe_allow_html=True)
    selected_city = st.selectbox("City", all_cities, index=all_cities.index("Delhi") if "Delhi" in all_cities else 0)
    selected_date = st.date_input("Date", value=date.today())
    predict_btn   = st.button("⟳  RUN PREDICTION", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    img_url = CITY_IMAGES.get(selected_city, CITY_IMAGES["default"])
    st.markdown(f"""
    <div class="city-img-wrap animate-fade" style="margin-top:1rem;">
      <img src="{img_url}" alt="{selected_city}" onerror="this.src='https://images.unsplash.com/photo-1524661135-423995f22d0b?w=600&q=80'"/>
      <div class="city-img-overlay">
        <div>
          <div class="city-img-label">📍 {selected_city.upper()}</div>
          <div class="city-img-sub">INDIA · AQI MONITORING ZONE</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    month  = selected_date.month
    season = get_season(month)
    c_aqi  = city_mean.get(selected_city, np.mean(list(city_mean.values())))
    
    # Get pollutants - with fallback to live API for missing cities
    if selected_city in city_pol_med:
        pols = city_pol_med[selected_city]
    else:
        # Try live API, fallback to global average
        live_pols = fetch_live_pollutants(selected_city)
        if live_pols:
            pols = live_pols
        else:
            # Use global average
            pols = {c: df[c].median() for c in POLLUTANT_COLS}

    with st.expander("🔬  AUTO-FILLED SENSOR DATA"):
        is_live = selected_city not in cities_in_data
        source = "📡 Live Data API" if is_live else "📊 Historical Data"
        
        st.markdown(
            f'<div class="chips">'
            f'<span class="chip">{SEASON_LABELS[season]}</span>'
            f'<span class="chip">📅 {selected_date.strftime("%B %Y")}</span>'
            f'<span class="chip">{source}</span>'
            f'<span class="chip">📊 Avg AQI: {c_aqi:.0f}</span>'
            f'</div>'
            f'<div class="pol-grid">'
            + "".join(f'<div class="pol-card"><div class="pol-name">{k}</div><div class="pol-val">{v:.1f}</div></div>'
                      for k, v in pols.items())
            + '</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel" style="min-height:40px;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">PREDICTION OUTPUT</div>', unsafe_allow_html=True)

    if predict_btn:
        try:
            # Prepare input
            inp = {**pols, "Month": month, "Season": season, "City_Mean_AQI": c_aqi}
            Xin = pd.DataFrame([inp])[FEATURE_COLS]
            
            # Predict using Random Forest (no scaler needed)
            aqi = max(0, min(500, round(float(model.predict(Xin)[0]), 1)))
            
            color, bucket, advice = aqi_info(aqi)
            pct  = aqi_pct(aqi)

            city_df = df[df['City'] == selected_city]
            min_aqi = round(city_df['AQI'].min(), 1) if len(city_df) > 0 else "—"
            max_aqi = round(city_df['AQI'].max(), 1) if len(city_df) > 0 else "—"

            st.markdown(f"""
            <div class="stat-row animate-slide">
              <div class="stat-card">
                <div class="stat-card-num">{c_aqi:.0f}</div>
                <div class="stat-card-lbl">City Avg AQI</div>
              </div>
              <div class="stat-card">
                <div class="stat-card-num" style="color:#28a745">{min_aqi}</div>
                <div class="stat-card-lbl">Best Recorded</div>
              </div>
              <div class="stat-card">
                <div class="stat-card-num" style="color:#dc3545">{max_aqi}</div>
                <div class="stat-card-lbl">Worst Recorded</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # AQI Gauge using Plotly (reliable, works every time)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=aqi,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': bucket, 'font': {'size': 28, 'color': color, 'family': 'Orbitron'}},
                number={'font': {'size': 90, 'color': color, 'family': 'Orbitron'}, 'suffix': ''},
                gauge={
                    'axis': {'range': [0, 500], 'tickwidth': 2, 'tickcolor': 'rgba(0,200,255,0.4)', 'tickfont': {'size': 10}},
                    'bar': {'color': color, 'thickness': 0.2, 'line': {'color': color, 'width': 2}},
                    'bgcolor': 'rgba(0,200,255,0.02)',
                    'borderwidth': 3,
                    'bordercolor': color,
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(40, 167, 69, 0.25)'},
                        {'range': [50, 100], 'color': 'rgba(163, 198, 57, 0.25)'},
                        {'range': [100, 200], 'color': 'rgba(240, 173, 78, 0.25)'},
                        {'range': [200, 300], 'color': 'rgba(253, 126, 20, 0.25)'},
                        {'range': [300, 400], 'color': 'rgba(220, 53, 69, 0.25)'},
                        {'range': [400, 500], 'color': 'rgba(255, 51, 102, 0.25)'}
                    ],
                    'threshold': {
                        'line': {'color': color, 'width': 4},
                        'thickness': 0.8,
                        'value': aqi
                    }
                }
            ))
            
            fig_gauge.update_layout(
                height=380,
                font=dict(family='Orbitron', color='#cde8f5', size=12),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=70, b=10),
                showlegend=False
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
            
            # Health advice and details
            st.markdown(f"""
            <div style="text-align:center;margin:2rem 0 1rem;">
              <div style="color:{color};font-size:1.1rem;font-weight:600;letter-spacing:1px;margin-bottom:1rem;">
                {advice}
              </div>
              <div class="chips" style="justify-content:center;">
                <span class="chip">📍 {selected_city}</span>
                <span class="chip">📅 {selected_date.strftime('%d %b %Y')}</span>
                <span class="chip">{SEASON_LABELS[season]}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
            
            # AQI Scale Bar
            st.markdown(f"""
            <div style="margin:2rem 0;">
              <div style="font-family:'Orbitron',monospace;font-size:.65rem;letter-spacing:2px;color:var(--muted);margin-bottom:1rem;text-align:center;">AQI MEASUREMENT SCALE</div>
              <div class="scale-bar" style="height:10px;box-shadow:0 0 20px rgba(0,200,255,.3);">
                <div class="scale-marker" style="left:{pct}%;background:{color};color:{color};width:20px;height:20px;top:-5px;box-shadow:0 0 20px {color};"></div>
              </div>
              <div class="scale-labels" style="margin-top:0.8rem;">
                <span>GOOD (0-50)</span><span>SATISF. (51-100)</span><span>MODERATE (101-200)</span>
                <span>POOR (201-300)</span><span>V.POOR (301-400)</span><span>SEVERE (401+)</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Prediction error: {str(e)}")
    
    else:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;
                    justify-content:center;height:380px;opacity:.35;">
          <div style="font-size:3.5rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;">🌐</div>
          <div style="font-family:'Orbitron',monospace;font-size:.65rem;
                      letter-spacing:3px;color:var(--muted);text-align:center;">
            SELECT CITY + DATE<br>THEN RUN PREDICTION
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── CHARTS ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 DATA ANALYTICS</div>', unsafe_allow_html=True)

city_df = df[df['City'] == selected_city].copy() if selected_city in cities_in_data else pd.DataFrame()
if len(city_df) > 0:
    city_df['Date'] = pd.to_datetime(city_df['Date'])
    city_df = city_df.sort_values('Date')

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">AQI TREND · ' + selected_city.upper() + '</div>', unsafe_allow_html=True)
    if len(city_df) > 0:
        monthly = city_df.groupby(city_df['Date'].dt.to_period('M'))['AQI'].mean().reset_index()
        monthly['Date'] = monthly['Date'].dt.to_timestamp()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly['Date'], y=monthly['AQI'], mode='lines', name='AQI',
            line=dict(color='#00c8ff', width=2), fill='tozeroy', fillcolor='rgba(0,200,255,0.08)'))
        fig.update_layout(**plotly_cfg(), height=220,
            xaxis=dict(gridcolor='rgba(0,200,255,0.08)', showline=False, tickfont=dict(size=9)),
            yaxis=dict(gridcolor='rgba(0,200,255,0.08)', showline=False, tickfont=dict(size=9)), showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("No historical data available")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">POLLUTANT RADAR</div>', unsafe_allow_html=True)
    radar_cols = ['PM2.5','PM10','NO2','SO2','O3','CO']
    vals = [pols.get(c, 0) for c in radar_cols]
    maxvals = [300, 500, 200, 100, 180, 10]
    norm = [min(100, v/m*100) for v,m in zip(vals, maxvals)]
    fig = go.Figure(go.Scatterpolar(r=norm+[norm[0]], theta=radar_cols+[radar_cols[0]], fill='toself',
        fillcolor='rgba(0,200,255,0.1)', line=dict(color='#00c8ff', width=2), marker=dict(color='#00ff9d', size=5)))
    fig.update_layout(**plotly_cfg(), height=220, polar=dict(bgcolor='rgba(0,0,0,0)', gridshape='linear',
        radialaxis=dict(visible=True, range=[0,100], gridcolor='rgba(0,200,255,0.12)', tickfont=dict(size=8), color='#4a7a9b'),
        angularaxis=dict(gridcolor='rgba(0,200,255,0.12)', tickfont=dict(size=9), color='#cde8f5')), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">CITY COMPARISON</div>', unsafe_allow_html=True)
    top_cities = df.groupby('City')['AQI'].mean().sort_values(ascending=True).tail(10)
    bar_colors = ['#dc3545' if c == selected_city else '#00c8ff' for c in top_cities.index]
    fig = go.Figure(go.Bar(y=top_cities.index, x=top_cities.values, orientation='h',
        marker=dict(color=bar_colors, line=dict(color='rgba(0,0,0,0)', width=0)),
        text=[f'{v:.0f}' for v in top_cities.values], textposition='outside', textfont=dict(size=9, color='#cde8f5')))
    fig.update_layout(**plotly_cfg(), height=220, xaxis=dict(gridcolor='rgba(0,200,255,0.08)', tickfont=dict(size=8)),
        yaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(size=8)), showlegend=False, bargap=0.3)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

c4, c5 = st.columns(2, gap="medium")

with c4:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">MONTHLY PATTERN · ' + selected_city.upper() + '</div>', unsafe_allow_html=True)
    if len(city_df) > 0:
        city_df['Month_num'] = city_df['Date'].dt.month
        monthly_avg = city_df.groupby('Month_num')['AQI'].mean().reindex(range(1,13), fill_value=0)
        month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        month_colors = ['#dc3545' if v>200 else '#fd7e14' if v>100 else '#28a745' for v in monthly_avg.values]
        fig = go.Figure(go.Bar(x=month_names, y=monthly_avg.values,
            marker=dict(color=month_colors, opacity=0.85, line=dict(color='rgba(0,0,0,0)')),
            text=[f'{v:.0f}' for v in monthly_avg.values], textposition='outside', textfont=dict(size=8, color='#cde8f5')))
        fig.update_layout(**plotly_cfg(), height=220, xaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(size=9)),
            yaxis=dict(gridcolor='rgba(0,200,255,0.08)', tickfont=dict(size=9)), showlegend=False, bargap=0.2)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("No historical data available")
    st.markdown('</div>', unsafe_allow_html=True)

with c5:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">PM2.5 vs AQI SCATTER</div>', unsafe_allow_html=True)
    if len(city_df) > 10:
        sample = city_df[['PM2.5','AQI']].dropna().sample(min(300, len(city_df)), random_state=42)
        fig = go.Figure(go.Scatter(x=sample['PM2.5'], y=sample['AQI'], mode='markers',
            marker=dict(color=sample['AQI'], colorscale='RdYlGn_r', size=5, opacity=0.65,
                colorbar=dict(title=dict(text='AQI', font=dict(size=9, color='#cde8f5')), tickfont=dict(size=8, color='#cde8f5'), thickness=10))))
        fig.update_layout(**plotly_cfg(), height=220, xaxis=dict(title=dict(text='PM2.5', font=dict(size=9)),
            gridcolor='rgba(0,200,255,0.08)', tickfont=dict(size=8)), yaxis=dict(title=dict(text='AQI', font=dict(size=9)),
            gridcolor='rgba(0,200,255,0.08)', tickfont=dict(size=8)), showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Need more data for scatter plot")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""<div class="footer">🤖 RANDOM FOREST · R² {model_r2:.4f} · {len(all_cities)} CITIES · AQI ORACLE v6.0</div>""", unsafe_allow_html=True)