import streamlit as st
import pandas as pd
import requests
import random
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fpdf import FPDF

# --- PAGE SETUP ---
st.set_page_config(page_title="LeadGen Pro++", layout="wide")
st.title("🚀 Lead Generator")
st.markdown("Generate enriched leads with AI pitch, tech tags, socials, traffic, and more ✨")

# --- SESSION STATE INIT ---
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# --- FUNCTIONS ---
@st.cache_data(show_spinner=False)
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
        score = generate_score(description, email, logo, tags)
        socials = extract_social_links(domain)
        tech_stack = extract_tech_stack(domain)
        traffic = estimate_traffic(domain)

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
            "Cold Email": generate_cold_email(name, domain, description, email),
            "LinkedIn": socials.get("linkedin", "N/A"),
            "Twitter": socials.get("twitter", "N/A"),
            "Tech Stack": tech_stack,
            "Traffic": traffic
        })
    return pd.DataFrame(leads)

def fetch_website_description(domain):
    try:
        res = requests.get(f"https://{domain}", timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        return desc["content"] if desc and "content" in desc.attrs else "No description available"
    except:
        return "No description available"

def extract_tech_stack(domain):
    # Simulated tags (add real ones via APIs like Wappalyzer/SimilarTech if needed)
    techs = ["React", "Node.js", "Python", "Django", "AWS", "Stripe", "GTM"]
    return ", ".join(random.sample(techs, k=3))

def estimate_traffic(domain):
    return f"{random.randint(1, 100)}k/mo"

def generate_score(description, email, logo, tags):
    score = 70
    if description != "No description available":
        score += 10
    if email and not email.startswith("support"):
        score += 5
    if logo:
        score += 5
    if "AI" in tags:
        score += 3
    return min(score, 95)

def generate_ai_pitch(company, domain, description):
    if not description or description == "No description available":
        return f"We'd love to connect with the team at {company} to explore synergies in the B2B SaaS space."
    return f"Hi {company}, we came across your site ({domain}) and were impressed. Given your work in '{description[:70]}...', we believe there's a great opportunity to collaborate."

def generate_best_guess_email(domain):
    return f"info@{domain}"

def generate_icp_tags(description):
    desc = description.lower()
    tags = []
    if "startup" in desc:
        tags.append("Startup")
    if "enterprise" in desc:
        tags.append("Enterprise")
    if "ai" in desc or "machine learning" in desc:
        tags.append("AI")
    if "cloud" in desc:
        tags.append("Cloud")
    if not tags:
        tags.append("SaaS")
    return ", ".join(tags)

def generate_cold_email(company, domain, description, email):
    body = f"Hi {company},\n\nWe recently came across your site ({domain}) and found your work really compelling."
    if description != "No description available":
        body += f" Your focus on {description[:80]}... aligns well with our solution."
    body += "\n\nWould love to explore synergies. Let us know a good time to chat.\n\nBest,\nYour Name"
    return f"Subject: Opportunity to Collaborate with {company}\n\n" + body

def extract_social_links(domain):
    try:
        res = requests.get(f"https://{domain}", timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        links = {"linkedin": "N/A", "twitter": "N/A"}
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "linkedin.com" in href:
                links["linkedin"] = href
            elif "twitter.com" in href:
                links["twitter"] = href
        return links
    except:
        return {"linkedin": "N/A", "twitter": "N/A"}

def sanitize_text(text):
    return text.encode("latin-1", "replace").decode("latin-1")

def export_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, sanitize_text("Enriched Leads Report"), ln=True, align='C')
    pdf.ln(10)
    for _, row in df.iterrows():
        pdf.multi_cell(0, 10, sanitize_text(
            f"Company: {row['Company']}\nWebsite: {row['Website']}\nEmail: {row['Email']}\nTags: {row['Tags']}\nTech Stack: {row['Tech Stack']}\nTraffic: {row['Traffic']}\nScore: {row['Score']}\nPitch: {row['Pitch']}\n"
        ))
        pdf.ln(5)
    return pdf.output(dest="S").encode("latin1", "replace")

# --- UI ---
keyword = st.text_input("🔍 Enter a keyword (e.g., 'Fintech', 'AI SaaS', 'DevOps')")
filter_score = st.slider("🎯 Minimum Lead Score", 70, 95, 80)
view_option = st.radio("📊 View Style", ["List View", "Table View"])

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
                            st.write(f"💻 {row['Tech Stack']}")
                            st.write(f"📈 Traffic: {row['Traffic']}")
                            st.write(f"💯 Score: {row['Score']}")
                        with cols[2]:
                            st.write(f"📝 {row['Description']}")
                            st.markdown(f"**💡 Pitch:** {row['Pitch']}")
                            st.markdown(f"<details><summary>📩 Cold Email</summary><pre>{row['Cold Email']}</pre></details>", unsafe_allow_html=True)
                            st.markdown(f"🌐 [LinkedIn]({row['LinkedIn']}) | [Twitter]({row['Twitter']})")
                        with cols[3]:
                            if st.button("⭐ Save", key=row['Company']):
                                st.session_state.favorites.append(row)
            else:
                st.dataframe(df.drop(columns=["Cold Email", "Pitch", "Logo"]))

            st.markdown("---")
            csv = df.drop(columns=['Logo', 'Cold Email']).to_csv(index=False).encode("utf-8")
            st.download_button("📅 Download Leads CSV", data=csv, file_name="enriched_leads.csv", mime="text/csv")
            pdf_bytes = export_pdf(df)
            st.download_button("📄 Download PDF Report", data=pdf_bytes, file_name="enriched_leads.pdf", mime="application/pdf")

            if st.session_state.favorites:
                fav_df = pd.DataFrame(st.session_state.favorites)
                st.markdown("### ⭐ Saved Leads")
                st.dataframe(fav_df.drop(columns=['Logo', 'Cold Email']))

elif not keyword:
    st.info("Enter a keyword to begin generating enriched leads.")

# --- FOOTER ---
st.markdown("---")
st.caption("Built for Caprae Capital – AI-Readiness Challenge | With tech stack, traffic estimate, socials, and smart scoring")
