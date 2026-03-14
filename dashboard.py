import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.neural_network import MLPRegressor
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="EcoSmart AI Ultra", layout="wide")

# تحديث تلقائي كل 5 ثواني
st_autorefresh(interval=5000, key="refresh")

# ===============================
# 🎨 تصميم احترافي جداً
# ===============================
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
.metric-card {
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 EcoSmart Gabès - AI ULTRA")
st.subheader("Neural Environmental Intelligence System")

# ===============================
# قراءة البيانات
# ===============================
conn = sqlite3.connect("ecosmart_gabes.db")
df = pd.read_sql_query("SELECT * FROM air_data", conn)
conn.close()

if df.empty:
    st.warning("لا توجد بيانات حالياً.")
    st.stop()

latest = df.iloc[-1]

# ===============================
# 🎯 بطاقات احترافية
# ===============================
col1, col2, col3, col4 = st.columns(4)

metrics = {
    "🌫 PM2.5": ("pm25", "#ff4b4b"),
    "🫁 CO2": ("co2", "#9467bd"),
    "🌡 Temp": ("temperature", "#1f77b4"),
    "💧 Humidity": ("humidity", "#2ca02c"),
}

i = 0
for title, (col, color) in metrics.items():
    if col in df.columns:
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card" style="background-color:{color};">
            {title}<br>{round(latest[col],2)}
            </div>
            """, unsafe_allow_html=True)
        i += 1

st.divider()

# ===============================
# 📊 مؤشر AQI احترافي (Gauge)
# ===============================
if "pm25" in df.columns:
    aqi_value = latest["pm25"]

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi_value,
        title={'text': "Air Quality Index (PM2.5)"},
        gauge={
            'axis': {'range': [0, 200]},
            'bar': {'color': "red"},
            'steps': [
                {'range': [0, 35], 'color': "green"},
                {'range': [35, 75], 'color': "yellow"},
                {'range': [75, 150], 'color': "orange"},
                {'range': [150, 200], 'color': "red"},
            ],
        }
    ))

    fig_gauge.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_gauge, use_container_width=True)

# ===============================
# 🤖 شبكة عصبية للتنبؤ
# ===============================
if "pm25" in df.columns and len(df) > 10:

    st.subheader("🤖 Neural Network Prediction")

    X = np.arange(len(df)).reshape(-1, 1)
    y = df["pm25"].values

    model = MLPRegressor(hidden_layer_sizes=(50,50),
                         max_iter=500,
                         random_state=42)

    model.fit(X, y)

    future_steps = 15
    future_X = np.arange(len(df), len(df)+future_steps).reshape(-1,1)
    predictions = model.predict(future_X)

    fig_ai = go.Figure()

    fig_ai.add_trace(go.Scatter(
        y=df["pm25"],
        mode='lines',
        name="Current Data"
    ))

    fig_ai.add_trace(go.Scatter(
        x=list(range(len(df), len(df)+future_steps)),
        y=predictions,
        mode='lines',
        line=dict(dash="dash"),
        name="Neural Forecast"
    ))

    fig_ai.update_layout(
        template="plotly_dark",
        title="AI Neural Forecast - PM2.5",
        height=500
    )

    st.plotly_chart(fig_ai, use_container_width=True)

# ===============================
# 📍 خريطة تفاعلية (Gabès)
# ===============================
st.subheader("📍 Monitoring Location")

map_data = pd.DataFrame({
    "lat": [33.8815],
    "lon": [10.0982]
})

st.map(map_data)

# ===============================
# 🚨 نظام إنذار ذكي
# ===============================
st.subheader("⚠ Smart Alert System")

value = latest.get("pm25", 0)

if value > 150:
    st.error("🚨 Severe Pollution - Emergency Level")
elif value > 75:
    st.warning("⚠ High Pollution")
elif value > 35:
    st.info("🌤 Moderate Pollution")
else:
    st.success("✅ Air Quality Good")

st.caption("EcoSmart AI ULTRA - Real Time Neural Intelligence")