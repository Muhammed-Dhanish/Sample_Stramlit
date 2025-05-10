import streamlit as st
import pandas as pd
import requests
import time
import altair as alt


# Set the page title and layout
st.set_page_config(page_title="Live CSR Dashboard", layout="wide")
st.title("🚀 CSR Live Order Dashboard")

# Refresh interval
# REFRESH_INTERVAL = 60  # seconds

# API configuration
API_URL = "https://alaneesqatar.qa/backend/api/reports_api/agents_product_count_current_month"  
API_KEY = "0v5kc3947icqvh131svlkgjhz4m9"

payload = {"key": API_KEY}
headers = {"Content-Type": "application/x-www-form-urlencoded"}

# Function to fetch data from the API
# @st.cache_data(ttl=REFRESH_INTERVAL) # cache with timeout to automatically refresh
def fetch_data():
    try:
        response = requests.post(API_URL, data=payload, headers=headers)
        # st.write(f"API Response Status Code: {response.status_code}")

        data = response.json()

        #only proceed if the response is valid
        if data["status_code"] == 100 and "data" in data:
            df = pd.DataFrame(data["data"])
            
            # Data Table
            st.subheader("📊 Raw Data")
            st.dataframe(df)

            # Bar Chart
            st.subheader("📈 Order Status")
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X("name:N", title="Name"),
                y=alt.Y("count:Q", title="Total Orders"),
                color=alt.Color("count:Q", scale=alt.Scale(scheme='purpleblue'), legend=None),
                tooltip=["name", "count"]
            ).properties(
                width=700,
                height=400
            )
            st.altair_chart(chart, use_container_width=True)
            
        else:
            st.error("❌ Error: Invalid response from API")  
    except Exception as e:
         st.error(f"❌ Error fetching or displaying data:\n\n{e}")

# Refresh button
if st.button("Refresh Data"):
    fetch_data()
