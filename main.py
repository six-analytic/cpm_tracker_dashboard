import streamlit as st
import pandas as pd
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
    st.markdown("""
        <style>
        .stApp {
            background-color: #111111;
            color: #FFFFFF;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #111111;
        }
        div[data-testid="stText"] {
            color: #111111;
        }
        </style>
    """, unsafe_allow_html=True)

# Title and subtitle
st.title("CPM Data Support Dashboard v0.1")
col1, col2 = st.columns(2)
with col1:
    st.text("- Provided by Six Analytic - for any questions, or to suggest new data sources, please contact us at sixanalytic@iiss.org")
    st.text("- You can use the AI Filter slider to see relevant entries. You can then follow the links, or use the download button to get the filtered dataset.")
with col2:
    st.text("- Known issue: Light mode is not working properly, please use dark mode for now")
    st.text("- Known issue 2: The system currently generates duplicate entries for the same event, as they are reported by different sources. We are working on fixing this.")

# Airtable configuration
AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
BASE_ID = st.secrets["AIRTABLE_BASE_ID"]
TABLE_ID = st.secrets["AIRTABLE_TABLE_ID"]

# Initialize Airtable client
api = Api(AIRTABLE_API_KEY) 
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
    
    # Ensure 'id' is the first column
    if 'id' in df.columns:
        # Reorder columns to put 'id' first
        cols = ['id'] + [col for col in df.columns if col != 'id']
        df = df[cols]
        # Sort by id in descending order (newest first)
        df = df.sort_values('id', ascending=False)
    
    # AI Filter toggle
    ai_filter = st.toggle('Activate AI Filter', value=False)
    
    # Filter data based on AI relevance if toggle is enabled
    if ai_filter:
        filtered_df = df[df['relevance_ai'] == "1"]
    else:
        filtered_df = df
    
    # Display last 25 entries with selected columns only
    st.subheader("Latest 25 Entries")
    columns_to_display = [
        'id',
        'op_name',
        'type',
        'details_text',
        'sponsor_actor',
        'target_actor',
        'source_html',
        'time_recorded_unix'
    ]
    
    # Ensure all requested columns exist in the DataFrame
    display_cols = [col for col in columns_to_display if col in filtered_df.columns]
    
    st.dataframe(
        filtered_df[display_cols].head(25),
        hide_index=True
    )
    
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
