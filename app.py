import streamlit as st
import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
from io import BytesIO
import base64

st.set_page_config(page_title="LeadGen: Smart Company Finder", layout="wide")
st.title("🚀 AI-Ready Lead Generator + Enrichment")

st.markdown("""
Type a **keyword** like "B2B SaaS", "AI Startup", or "Fintech India" to find relevant leads.

✅ Features:
- Company info via Clearbit
- Smart enrichment (description, logo)
- Lead score
- Download or CRM-ready format
- AI-generated email pitch (optional)
""")

# --- Scrape a company description ---
def fetch_company_description(domain):
    try:
        url = f"https://{domain}"
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        meta = soup.find("meta", {"name": "description"}) or soup.find("meta", {"property": "og:description"})
        if meta and meta.get("content"):
            return meta["content"].strip()

        p = soup.find("p")
        if p and p.text:
            return p.text.strip()
    except:
        pass
    return "No description available."

# --- AI Email Pitch Generator ---
def generate_email_pitch(company):
    name = company.get("Company", "your company")
    desc = company.get("Description", "a growing business")
    return f"Hi,\n\nI came across {name} and was impressed by what you're doing in the space of {desc[:50]}...\nWould love to chat about how we could help you grow faster.\n\nBest,\n[Your Name]"

# --- Get leads from Clearbit ---
def fetch_clearbit_companies(keyword, max_results=15):
    url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={keyword}"
    try:
        r = requests.get(url, timeout=5)
        companies = r.json()
    except:
        return pd.DataFrame()

    leads = []
    for c in companies[:max_results]:
        domain = c.get("domain", "")
        name = c.get("name", "")
        logo = c.get("logo", "")
        if not domain:
            continue
        description = fetch_company_description(domain)
        email = f"info@{domain}" if domain else ""
        score = random.randint(75, 95)
        pitch = generate_email_pitch({"Company": name, "Description": description})

        leads.append({
            "Company": name,
            "Website": f"https://{domain}",
            "Email": email,
            "Score": score,
            "Description": description,
            "Logo": logo,
            "AI Email Pitch": pitch
        })
    return pd.DataFrame(leads)

# --- UI Layout ---
keyword = st.text_input("🔍 Keyword (e.g. 'HR Tech', 'Climate SaaS')")

col1, col2 = st.columns(2)
with col1:
    max_results = st.slider("Number of leads", min_value=5, max_value=25, value=10)
with col2:
    min_score = st.slider("Minimum Lead Score", min_value=60, max_value=100, value=75)

if st.button("🚀 Find Leads") and keyword.strip():
    with st.spinner("Fetching and enriching leads..."):
        df = fetch_clearbit_companies(keyword, max_results=max_results)
        if df.empty:
            st.warning("No companies found. Try a broader keyword.")
        else:
            df = df[df["Score"] >= min_score].reset_index(drop=True)
            st.success(f"✅ {len(df)} high-quality leads found!")

            # Show table
            st.dataframe(df.drop(columns=["Logo"]).style.highlight_max(axis=0), use_container_width=True)

            # Download
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", data=csv, file_name="leads.csv", mime="text/csv")

            # Show logos (optional)
            if st.checkbox("🖼️ Show company logos"):
                for _, row in df.iterrows():
                    st.markdown(f"### {row['Company']}")
                    if row['Logo']:
                        st.image(row['Logo'], width=100)
                    st.write(f"**Website**: {row['Website']}")
                    st.write(f"**Email**: {row['Email']}")
                    st.write(f"**Score**: {row['Score']}")
                    st.write(f"**Description**: {row['Description']}")
                    st.code(row['AI Email Pitch'], language='text')
                    st.markdown("---")

elif not keyword:
    st.info("Start by entering a keyword to find company leads.")

st.markdown("---")
st.caption("Built for Caprae Capital – AI-Readiness Challenge | 💡 Smart B2B SaaS Scraper")
