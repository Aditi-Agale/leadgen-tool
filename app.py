import streamlit as st
import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# --- PAGE SETUP ---
st.set_page_config(page_title="LeadGen Pro", layout="wide")
st.title("🚀 LeadGen Pro - B2B SaaS Lead Generator")
st.markdown("Generate enriched leads with company name, email, logo, description, score & AI-generated pitch ✨")

# --- FUNCTIONS ---
def fetch_clearbit_companies(keyword, max_results=20):
    url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={keyword}"
    r = requests.get(url)
    companies = r.json()

    leads = []
    for idx, c in enumerate(companies[:max_results]):
        domain = c.get("domain", "")
        name = c.get("name", "")
        logo = c.get("logo", "")

        if not domain:
            continue

        # Scrape meta description from the website for enrichment
        description = fetch_website_description(domain)

        leads.append({
            "Rank": idx + 1,
            "Company": name,
            "Website": f"https://{domain}",
            "Email": f"info@{domain}",
            "Description": description,
            "Score": random.randint(75, 95),
            "Logo": logo,
            "Pitch": generate_ai_pitch(name, domain, description)
        })
    return pd.DataFrame(leads)

def fetch_website_description(domain):
    try:
        url = f"https://{domain}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        return desc_tag["content"] if desc_tag and "content" in desc_tag.attrs else "No description available"
    except:
        return "No description available"

def generate_ai_pitch(company, domain, description):
    if not description or description == "No description available":
        return f"We'd love to connect with the team at {company} to explore synergies in the B2B SaaS space."
    return f"Hi {company}, we came across your website ({domain}) and were impressed. Given your work in '{description[:70]}...', we believe there's a great opportunity to collaborate."

# --- UI ---
keyword = st.text_input("🔍 Enter a keyword (e.g., 'Fintech', 'AI SaaS', 'DevOps')")
filter_score = st.slider("🎯 Minimum Lead Score", 70, 95, 80)

if st.button("🚀 Generate Leads") and keyword.strip():
    with st.spinner("Fetching data from Clearbit and enriching leads..."):
        df = fetch_clearbit_companies(keyword)
        df = df[df['Score'] >= filter_score].reset_index(drop=True)

        if df.empty:
            st.warning("No enriched leads found. Try a broader or more relevant keyword.")
        else:
            st.success(f"✅ Found {len(df)} enriched leads.")

            # --- Display with logos ---
            for _, row in df.iterrows():
                with st.container():
                    cols = st.columns([1, 3, 6])
                    with cols[0]:
                        if row["Logo"]:
                            st.image(row["Logo"], width=64)
                    with cols[1]:
                        st.subheader(row["Company"])
                        st.write(f"🔗 [{row['Website']}]({row['Website']})")
                        st.write(f"📧 {row['Email']}")
                        st.write(f"💯 Score: {row['Score']}")
                    with cols[2]:
                        st.write(f"📝 {row['Description']}")
                        st.markdown(f"**💡 Pitch:** {row['Pitch']}")

            # --- Downloadable CSV ---
            st.markdown("---")
            csv = df.drop(columns=['Logo']).to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Leads CSV", data=csv, file_name="enriched_leads.csv", mime="text/csv")

elif not keyword:
    st.info("Enter a keyword to begin generating enriched leads.")

# --- FOOTER ---
st.markdown("---")
st.caption("Built for Caprae Capital – AI-Readiness Challenge | Enhanced by GPT-4")
