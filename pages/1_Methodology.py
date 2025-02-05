import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Methodology - CPM Data Support Dashboard",
    page_icon="📚",
    layout="wide"
)

st.title("Methodology")

st.markdown("""

Last updated: 01/02/2025 

## About
- This dashboard is a work in progress. It is intended to be a tool for analysts to help them find and track Cyber Operations.
- We also hope that it will be useful platform for offering similar tools to the other IISS departments.

## Sources
- The automation platform collects all articles received from the RSS feeds from the following sources:
    - EuRepoC Archive Feed
    - Advanced Persisten Threats (SentinelOne)
    - State Sponsored Cyber Attack (SentinelOne)
    - BBC News (Cyber Attacks tag)
    - BleepingComputer
    - New York Times (Cyber Security tag)
    - Le Monde (Piratage tag)
    - HackerNews (Cyber Attack tag)
    - SecurityWeek (Nation-State archives)
    - CISA Current Activity feed
    - Les Echos (Cybersecurité tag)
    - Silicon UK (Nation-State Hacking tag)
    - The Record by Recorded Future (Nation-State tag)
    - WIRED (Cyberattakcs and Hacks tag)
    - NSCS News RSS feed

- We have the capability to add new sources, and to modify the existing sources to be more specific. 
- It should be noted that the tracking quality across sources varies as we are still building our capability of extracting RSS feeds and website monitoring.

## Data Extraction (AI Agent 1)

- As new articles are received by the automation platform, they are processed by AI Agent 1 following an API call.
- AI Agent 1 uses a GPT-4o agent to extract relevant information from the article.
- Please note that the AI Agent is tasked with finding Cyber Operations in all articles:
    - As such, it will often to "see" a Cyber Operation where there is none. If it fails to find anything, responses may be blank.
    - An AI filter is applied in the next step to counter this issue.
- A major known issue is that the AI agent is insufficient in extracting operation dates - we recommend manual checking.

## AI Filter (AI Agent 2)

- The AI filter is another OpenAI agent which reads the initial output, and populates the "AI Filter" column.
- The filter is not perfect, and sometimes misclassifies events.
- We are working on improving the filter, and will update the dashboard as we make progress.

## Data Updates

- The database is updated in real time as new articles are received by the automation platform.
- In future, we will add batch processing to reduce costs, which will be done on a daily basis.

## Future Improvements

- We are working on improving the AI filter to reduce the number of false positives.
- We are also working on adding more sources to the dashboard.
- We are also working on migrating the dashboard to a more scalable platform, especially for the database.
- We are working on adding a third AI agent, which will query the database to see whether the operation in question has already been reported.
- Upon completion of the above, we will implement the ability to look for individual operations, and start working on visualisation capabilities.

""")

# Add any additional methodology content here 