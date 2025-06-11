# 🚀 LeadGen Pro++ — AI-Powered B2B Lead Generation App

**LeadGen Pro++** is an advanced Streamlit app designed for enriched B2B SaaS lead generation. It scrapes, scores, and enriches company data with AI-generated insights like pitches, cold emails, ICP tags, social media links, and more — all in a single, elegant interface.

---

## 🎯 Features

✅ Keyword-based company discovery via Clearbit  
✅ AI-generated cold emails and personalized pitches  
✅ Tech stack estimation (mocked, upgrade-ready)  
✅ Website traffic estimation (mocked, upgrade-ready)  
✅ Lead scoring algorithm with tag/context weighting  
✅ Social media extraction (LinkedIn, Twitter)  
✅ Tags like AI, SaaS, Cloud, Enterprise, etc.  
✅ Favorite leads saving across sessions  
✅ Export to PDF and CSV  
✅ Two views: list (cards) and table  
✅ Built entirely in Python with Streamlit  

---

## 📸 Demo Screenshots

| List View | Table View |
|-----------|------------|
| ![List View](assets/list-view.png) | ![Table View](assets/table-view.png) |

---

## 🛠️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/Aditi-Agale/leadgen-tool.git
cd leadgen-tool
pip install -r requirements.txt
```
Run the app locally:

```bash
streamlit run app.py
```
---
## 🔍 How It Works
1. User enters a keyword like "Fintech" or "AI SaaS".

2. App fetches matching companies using Clearbit’s autocomplete API.

3. For each company:

   - Description is scraped from the site.

   - Tags are assigned using NLP heuristics.

   - Email, logo, social links are guessed.

   - AI pitch and cold email are generated.

   - Tech stack and traffic are randomly estimated (upgradeable).

   - Score is computed based on relevance.

4. Leads can be viewed, filtered, saved, and downloaded (PDF/CSV).

---
## 📁 File Structure
```bash
leadgen-pro/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Dependencies
├── README.md              # This file
├── assets/                # Images for README
│   ├── list-view.png
│   └── table-view.png
```
📜 License

MIT License. Use it, build on it, make it yours.

