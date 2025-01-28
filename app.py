import streamlit as st
import pandas as pd
import plotly.express as px
from pyairtable import Api
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(page_title="CPM Data Support Dashboard v0.1", layout="wide")

# Add theme toggle at the top
theme = st.toggle('Dark Mode', value=True)
if theme:
    # Dark mode
    st.markdown("""
        <style>
        .stApp {
            background-color: #111111;
            color: #FFFFFF;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    # Light mode
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #111111;
        }
        </style>
    """, unsafe_allow_html=True)

# Title and subtitle
st.title("CPM Data Support Dashboard v0.1")
st.text("Provided by Six Analytic - for any questions, please contact us at sixanalytic@iiss.org")
st.text("Warning: Light mode is not working properly, please use dark mode for now")


# Airtable configuration
AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
BASE_ID = st.secrets["AIRTABLE_BASE_ID"]
TABLE_ID = st.secrets["AIRTABLE_TABLE_ID"]

# Initialize Airtable client
api = Api(AIRTABLE_API_KEY) # TODO: store this in safer place in production

table = api.table(BASE_ID, TABLE_ID)

# Function to fetch and process data
@st.cache_data(ttl=300)  # Cache the data for 5 minutes
def get_airtable_data():
    records = table.all()
    # Convert Airtable records to pandas DataFrame
    df = pd.DataFrame([record['fields'] for record in records])
    return df

# Load the data
try:
    df = get_airtable_data()
    
    # Add title for the map
    st.subheader("Map of State Sponsors")
    
    # Create world map using Plotly
    fig = px.choropleth(
        df,
        locations='sponsor_actor',  # Column containing country names
        locationmode='country names',  # Tells Plotly to expect country names
        hover_name='op_name',  # Shows the title when hovering over a country
        hover_data=['report_date', 'source_html'],  # Additional data to show in hover tooltip
        color_discrete_sequence=['#1f77b4'],  # Single color for all countries with data
        projection='natural earth'
    )
    
    # Customize the map appearance
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="LightGray",
        showframe=False
    )
    # Display the map
    st.plotly_chart(fig, use_container_width=True)
    
    # AI Filter toggle
    ai_filter = st.toggle('Activate AI Filter', value=False)
    
    # Filter data based on AI relevance if toggle is enabled
    if ai_filter:
        filtered_df = df[df['relevance_ai'] == "1"] # TODO: change this to 1 and make sure this field is stored as a number
    else:
        filtered_df = df
    
    # Display last 20 entries
    st.subheader("Latest 25 Entries")
    st.dataframe(filtered_df.tail(25))
    
    # Download button
    if st.button('Download Data as CSV'):
        # Convert DataFrame to CSV
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Click to Download",
            data=csv,
            file_name="cpm_newstracker_data.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
