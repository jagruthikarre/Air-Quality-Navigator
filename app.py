import streamlit as st
import pandas as pd
import requests
from sklearn.linear_model import LinearRegression
import random

# -------------------------------
# 🔹 Load Dataset
# -------------------------------
df = pd.read_csv("city_day.csv")

df = df[['PM2.5', 'PM10', 'NO2', 'SO2', 'CO']]
df = df.fillna(df.mean())

# -------------------------------
# 🔹 Create AQI
# -------------------------------
df['AQI'] = (0.5 * df['PM2.5'] + 
             0.3 * df['PM10'] + 
             0.2 * df['NO2'])

# -------------------------------
# 🔹 Train Model
# -------------------------------
X = df[['PM2.5', 'PM10', 'NO2', 'SO2', 'CO']]
y = df['AQI']

model = LinearRegression()
model.fit(X, y)

# -------------------------------
# 🌍 UI
# -------------------------------
st.title("🌍 Air Quality Navigator")

if st.button("Get Air Quality"):

    API_KEY = "4f11c0cfb847d55331d5a66896479d0f"

    lat = 17.3850
    lon = 78.4867

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    try:
        data = requests.get(url).json()

        # ✅ If API works
        if 'list' in data:
            comp = data['list'][0]['components']

            pm2_5 = comp.get('pm2_5', 0)
            pm10 = comp.get('pm10', 0)
            no2 = comp.get('no2', 0)
            so2 = comp.get('so2', 0)
            co = comp.get('co', 0) / 1000

            st.success("✅ Real-time data fetched")

        else:
            raise Exception("API failed")

    except:
        # 🔥 BACKUP (NO API)
        st.warning("⚠️ Using dataset sample (API not working)")

        sample = df.sample(1).iloc[0]

        pm2_5 = sample['PM2.5']
        pm10 = sample['PM10']
        no2 = sample['NO2']
        so2 = sample['SO2']
        co = sample['CO']

    # -------------------------------
    # 🔹 Prediction
    # -------------------------------
    predicted_aqi = model.predict([[pm2_5, pm10, no2, so2, co]])

    # -------------------------------
    # 🔹 Output
    # -------------------------------
    st.subheader("📊 Pollutants")
    st.write({
        "PM2.5": pm2_5,
        "PM10": pm10,
        "NO2": no2,
        "SO2": so2,
        "CO": co
    })

    st.subheader("🌫 Predicted AQI")
    st.write(round(predicted_aqi[0], 2))

    # Alerts
    if predicted_aqi[0] >= 150:
        st.error("⚠️ High Pollution! Stay indoors.")
    elif predicted_aqi[0] >= 100:
        st.warning("😷 Moderate Pollution.")
    else:
        st.success("😊 Good Air Quality!")