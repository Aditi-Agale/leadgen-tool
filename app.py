import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# --------------------------
# UI Layout
# --------------------------
st.set_page_config(page_title="LeadGen Enrichment Tool", layout="centered")
st.title("🚀 Lead Generation Enrichment Tool")

st.markdown("Enter a keyword to find companies or leads. We'll scrape basic info and simulate enrichment.")

# --------------------------
# Input Form
# --------------------------
keyword = st.text_input("🔍 Search Keyword (e.g., 'AI SaaS', 'CRM startups')")

if st.button("Generate Leads") and keyword:
    with st.spinner("Scraping and enriching leads..."):
        # --------------------------
        # Simulate Scraping (Replace this)
        # --------------------------
        dummy_data = [
            {"Company": "Alpha AI", "Website": "https://alpha.ai", "Email": "info@alpha.ai", "Score": 87},
            {"Company": "Beta CRM", "Website": "https://betacrm.com", "Email": "hello@betacrm.com", "Score": 76},
            {"Company": "Gamma Insights", "Website": "https://gammainsights.io", "Email": "contact@gammainsights.io", "Score": 90}
        ]
        df = pd.DataFrame(dummy_data)

        # --------------------------
        # Display Results
        # --------------------------
        st.success(f"Found {len(df)} leads for: '{keyword}'")
        st.dataframe(df, use_container_width=True)

        # --------------------------
        # Export CSV
        # --------------------------
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", data=csv, file_name="leads.csv", mime="text/csv")

elif keyword == "":
    st.info("Enter a keyword to start.")

# --------------------------
# Footer
# --------------------------
st.markdown("---")
st.caption("Built for Caprae Capital – AI-Readiness Challenge")
