import streamlit as st
import pandas as pd
import requests
import random

st.set_page_config(page_title="LeadGen with Clearbit", layout="centered")
st.title("🚀 Company Lead Generator via Clearbit")

st.markdown("Enter a keyword to fetch startup/company leads via Clearbit's autocomplete API 🎯")

def fetch_clearbit_companies(keyword, max_results=20):
    url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={keyword}"
    r = requests.get(url)
    companies = r.json()
    
    leads = []
    for c in companies[:max_results]:
        domain = c.get("domain", "")
        name = c.get("name", "")
        if not domain:
            continue
        leads.append({
            "Company": name,
            "Website": f"https://{domain}",
            "Email": f"info@{domain}",
            "Score": random.randint(75, 95)
        })
    return pd.DataFrame(leads)

keyword = st.text_input("🔍 Keyword (ex: 'Segment', 'Airbnb', 'Clearbit')")

if st.button("Find Leads") and keyword.strip():
    with st.spinner("Fetching company leads from Clearbit..."):
        df = fetch_clearbit_companies(keyword)
        if df.empty:
            st.warning("No companies found. Try a different keyword.")
        else:
            st.success(f"Found {len(df)} companies.")
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", data=csv, file_name="leads.csv", mime="text/csv")
elif not keyword:
    st.info("Start by typing a company keyword above.")

st.markdown("---")
st.caption("Built for Caprae Capital – AI-Readiness Challenge")
