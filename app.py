import requests
import streamlit as st
import matplotlib.pyplot as plt

# Streamlit page config
st.set_page_config(page_title="Weather Dashboard", layout="centered")

st.title("🌤️ Weather Visualization Dashboard")

# Your OpenWeatherMap API Key
API_KEY = ""  # Add your API Key Here

# Text input for city
cities_input = st.text_input("Enter city name(s) separated by commas (e.g., Delhi,Mumbai):")

# Parse and clean city names
cities = [city.strip() for city in cities_input.split(",") if city.strip()]

if st.button("Get Weather Data"):
    if not API_KEY:
        st.error("Please enter a valid OpenWeatherMap API Key.")
    elif not cities:
        st.warning("Please enter at least one city name.")
    else:
        temperatures = []
        humidities = []
        valid_cities = []
        failed_cities = []

        with st.spinner("Fetching data..."):
            for city in cities:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    valid_cities.append(city)
                    temperatures.append(data['main']['temp'])
                    humidities.append(data['main']['humidity'])
                else:
                    failed_cities.append(city)

        # Show error if all cities failed
        if not valid_cities:
            st.error("❌ Could not fetch weather data for any of the cities.")
        else:
            # Show warnings if some cities failed
            if failed_cities:
                st.warning(f"⚠️ Failed to fetch data for: {', '.join(failed_cities)}")

            # Display temperature chart
            st.subheader("🌡️ Temperature Comparison (°C)")
            fig1, ax1 = plt.subplots()
            ax1.bar(valid_cities, temperatures, color='orange')
            ax1.set_ylabel("Temperature (°C)")
            ax1.set_title("Temperature by City")
            st.pyplot(fig1)

            # Display humidity chart
            st.subheader("💧 Humidity Comparison (%)")
            fig2, ax2 = plt.subplots()
            ax2.bar(valid_cities, humidities, color='skyblue')
            ax2.set_ylabel("Humidity (%)")
            ax2.set_title("Humidity by City")
            st.pyplot(fig2)

            # Display data table
            st.subheader("📋 Weather Data Table")
            weather_data = {
                "City": valid_cities,
                "Temperature (°C)": temperatures,
                "Humidity (%)": humidities
            }
            st.dataframe(weather_data)
