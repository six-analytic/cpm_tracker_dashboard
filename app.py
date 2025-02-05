import streamlit as st
import pandas as pd
from pyairtable import Api
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(page_title="CPM Data Support Dashboard v0.2", layout="wide")

# Title and subtitle
st.title("CPM Data Support Dashboard v0.2")

st.markdown("""
The tool captures the latest cyber operations from sources selected by the CPFC team and updates whenever new content is detected.

This is the first step in automating the monitoring of key websites (largely specialised media, cyber threat intelligence organisations) the team has identified as a valuable source and filters select pieces of information that the team wants to capture as a first step in the data collection process. 
For more information on the methodology, please refer to the Methodology page.

You can use the **AI Filter slider** to see relevant items, or use the **download button** (located at the bottom of the page) to download the filtered dataset as a CSV file.
Note that downloaded datasets have more columsn that are not shown on this page.
""") 




# Airtable configuration
AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
BASE_ID = st.secrets["BASE_ID"]  # Ensure your secrets.toml uses this key if different
TABLE_ID = st.secrets["TABLE_ID"]  # Ensure your secrets.toml uses this key if different

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
        cols = ['id'] + [col for col in df.columns if col != 'id']
        df = df[cols]
        df = df.sort_values('id', ascending=False)
    
    # AI Filter toggle
    ai_filter = st.toggle('AI Filter', value=True)
    st.markdown("The AI filter is enabled by default. You can deactivate it to see all the data being collected.")
    
    # Filter data based on AI relevance if toggle is enabled
    if ai_filter:
        filtered_df = df[df['relevance_ai'] == "1"]
    else:
        filtered_df = df
    
    # Display last 25 entries with selected columns only
    st.subheader("Latest 25 Entries in the Database")
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
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Ready - Click to Download",
            data=csv,
            file_name="cpm_newstracker_data.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
