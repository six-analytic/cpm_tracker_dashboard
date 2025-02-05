import streamlit as st

# Configure the page
st.set_page_config(
    page_title="About - CPM Data Support Dashboard",
    page_icon="ℹ️",
    layout="wide"
)

st.title("About")

st.markdown("""
## About the Dashboard

The CPM Data Support Dashboard is designed to help analysts monitor and track cyber operations from multiple sources. This tool consolidates data from Airtable and provides filtering and download capabilities for further analysis.

For more details or support, please contact our team at [sixanalytic@iiss.org](mailto:sixanalytic@iiss.org).

### Key Features
- **Data Aggregation:** Collects data from various sources into one unified view.
- **AI Filtering:** Utilizes an AI filter (enabled by default) to display relevant entries.
- **Data Exploration:** A clean table view that allows you to quickly browse the latest records.
- **Data Export:** Easily download the filtered dataset as a CSV file for further analysis.

### Known Issues
- The system currently generates duplicate entries for the same event, as they are reported by different sources. We are working on fixing this.
- Not all sources are being tracked with the same quality. We are investigating whether this is a RSS, AI, or data pipeline issue.


### Changelog
- v0.2 (5 Feb 2025): Modified the AI filter to be enabled by default. Style changes to improve readability, fixed a bug with the theme. Added the "About" page.
- v0.1 (1 Feb 2025): Initial release

""") 