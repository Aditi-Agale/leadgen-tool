import streamlit as st
import pandas as pd
import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

# --- PAGE SETUP ---
st.set_page_config(page_title="LeadGen Pro+", layout="wide")
st.title("🚀 LeadGen Pro+ - B2B SaaS Lead Generator")
st.markdown("Generate enriched leads with AI pitch, company info, tags, and email templates ✨")

# --- SESSION STATE INIT ---
if "favorites" not in st.session_state:
    st.session_state.favorites = []

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

        description = fetch_website_description(domain)
        tags = generate_icp_tags(description)
        email = generate_best_guess_email(domain)
        score = generate_score(description, email, logo)

        leads.append({
            "Rank": idx + 1,
            "Company": name,
            "Website": f"https://{domain}",
            "Email": email,
            "Description": description,
            "Score": score,
            "Logo": logo,
            "Tags": tags,
            "Pitch": generate_ai_pitch(name, domain, description),
            "Cold Email": generate_cold_email(name, domain, description, email)
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

def generate_score(description, email, logo):
    score = 70
    if description and description != "No description available":
        score += 10
    if email and not email.startswith("support"):
        score += 5
    if logo:
        score += 5
    return min(score, 95)

def generate_ai_pitch(company, domain, description):
    if not description or description == "No description available":
        return f"We'd love to connect with the team at {company} to explore synergies in the B2B SaaS space."
    return f"Hi {company}, we came across your website ({domain}) and were impressed. Given your work in '{description[:70]}...', we believe there's a great opportunity to collaborate."

def generate_best_guess_email(domain):
    return f"info@{domain}"

def generate_icp_tags(description):
    desc = description.lower()
    if "startup" in desc:
        return "Startup"
    elif "enterprise" in desc:
        return "Enterprise"
    elif "ai" in desc or "machine learning" in desc:
        return "AI / ML"
    elif "cloud" in desc:
        return "Cloud SaaS"
    else:
        return "General SaaS"

def generate_cold_email(company, domain, description, email):
    intro = f"Subject: Opportunity to Collaborate with {company}\n\n"
    body = f"Hi {company},\n\nWe recently came across your site ({domain}) and found your work really compelling."
    if description and description != "No description available":
        body += f" Your focus on {description[:80]}... aligns well with our solution."
    closing = f"\n\nWould love to explore synergies. Let us know a good time to chat.\n\nBest,\nYour Name"
    return intro + body + closing

# --- UI INPUT ---
keyword = st.text_input("🔍 Enter a keyword (e.g., 'Fintech', 'AI SaaS', 'DevOps')")
filter_score = st.slider("🎯 Minimum Lead Score", 70, 95, 80)
view_option = st.radio("View Style", ["List View", "Table View"])

# --- BUTTON ---
if st.button("🚀 Generate Leads") and keyword.strip():
    with st.spinner("Fetching and enriching leads..."):
        df = fetch_clearbit_companies(keyword)
        df = df[df['Score'] >= filter_score].reset_index(drop=True)

        if df.empty:
            st.warning("No enriched leads found. Try a broader or more relevant keyword.")
        else:
            st.success(f"✅ Found {len(df)} enriched leads.")

            if view_option == "List View":
                for _, row in df.iterrows():
                    with st.container():
                        cols = st.columns([1, 3, 6, 1])
                        with cols[0]:
                            if row["Logo"]:
                                st.image(row["Logo"], width=64)
                        with cols[1]:
                            st.subheader(row["Company"])
                            st.write(f"🔗 [{row['Website']}]({row['Website']})")
                            st.write(f"📧 {row['Email']}")
                            st.write(f"🏷️ {row['Tags']}")
                            st.write(f"💯 Score: {row['Score']}")
                        with cols[2]:
                            st.write(f"📝 {row['Description']}")
                            st.markdown(f"**💡 Pitch:** {row['Pitch']}")
                            st.markdown(f"<details><summary>📩 Cold Email</summary><pre>{row['Cold Email']}</pre></details>", unsafe_allow_html=True)
                        with cols[3]:
                            if st.button("⭐ Save", key=row['Company']):
                                st.session_state.favorites.append(row)
            else:
                st.dataframe(df.drop(columns=["Cold Email", "Pitch", "Logo"]))

            st.markdown("---")
            csv = df.drop(columns=['Logo', 'Cold Email']).to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Leads CSV", data=csv, file_name="enriched_leads.csv", mime="text/csv")

            if st.session_state.favorites:
                fav_df = pd.DataFrame(st.session_state.favorites)
                st.markdown("### ⭐ Saved Leads")
                st.dataframe(fav_df.drop(columns=['Logo', 'Cold Email']))

elif not keyword:
    st.info("Enter a keyword to begin generating enriched leads.")

# --- FOOTER ---
st.markdown("---")
st.caption("Built for Caprae Capital – AI-Readiness Challenge | Enhanced with ICP tags, cold emails, and UX improvements")
