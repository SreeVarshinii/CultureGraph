# CultureGraph – Co-Founder Compatibility Checker

🌐 **Live App**: [https://culturegraph.streamlit.app/](https://culturegraph.streamlit.app/) 

CultureGraph is a Streamlit application that helps you **evaluate potential co-founder compatibility** by combining:

1. **Cultural taste signals** (music, film, brands, books, travel, podcasts, etc.)  
2. **Scenario-based questions** that probe working style, values, and decision-making  
3. **Three independent scoring pipelines**
   - **Qloo** entity similarity (taste-graph comparison)
   - **NLP similarity** using TF-IDF + cosine similarity over short free-text answers
   - **LLM (Gemini)** reasoning score with an explanation

The app captures a profile, resolves tastes to Qloo entity IDs, computes similarity against existing profiles, and produces a ranked list of matches with JSON/CSV logs for auditing.

---

## Table of Contents

- [Features](#features)  
- [Architecture](#architecture)  
- [Repository Structure](#repository-structure)  
- [Requirements](#requirements)  
- [Quick Start (Local)](#quick-start-local)  
- [Configuration & Secrets](#configuration--secrets)  
- [Running the App](#running-the-app)  
- [What Gets Saved](#what-gets-saved)  
- [Scoring & Logs](#scoring--logs)  
- [Deploy to Streamlit Cloud](#deploy-to-streamlit-cloud)  
- [Common Issues & Fixes](#common-issues--fixes)  
- [Extending the App](#extending-the-app)  
- [Contributing](#contributing)  
- [License](#license)

---

## Features

- **Rich profile intake**: Music, film, brands, travel, books, podcasts, games, etc.  
- **Scenario questions**: 27 curated questions to reveal working style and values.  
- **Entity resolution**: Converts user tastes into Qloo entity IDs for graph comparisons.  
- **Three scoring tracks**:
  - **Taste compatibility** via Qloo compare endpoint
  - **NLP similarity** (TF-IDF cosine) for free-text answers
  - **Gemini LLM** score + reasoning
- **Batch compare**: Compare the current profile to all existing profiles in `logs/master_entity_log.csv`.
- **Persistent logs**:  
  - Profile JSONs in `/profile`  
  - Per-run CSV in `/logs`  
  - A master log CSV you can grow over time  
- **“Best match” surfaced**: Row with the highest mean score is shown, and the matched person’s name/email/role are loaded from their JSON.

---

## Architecture

```

Streamlit UI (app.py)
├─ Collects demographic + cultural + scenario answers
├─ Resolves tastes → Qloo entity IDs (api\_utils.py)
├─ Analyzes tastes by category (analysis.py)
├─ Computes compatibility (compatibility.py)
│     ├─ Qloo taste score
│     ├─ NLP text similarity score
│     └─ Gemini score + explanation
├─ Persists JSON/CSV logs (create\_compatibility\_log.py)
└─ Displays best match + matched profile details

```

---

## Repository Structure

```

.
├── app.py                        # Streamlit entrypoint
├── api\_utils.py                  # Qloo searching, master CSV update, helpers
├── analysis.py                   # Taste/category analysis
├── compatibility.py              # Core scoring: Qloo, NLP, Gemini (+ helpers)
├── create\_compatibility\_log.py   # Batch compare & CSV logging
├── form\_Questions.py             # Category definitions + scenario questions
├── config.py                     # Reads API keys & builds headers
├── .streamlit/secrets.toml       # (local dev) secrets – Do not commit to public repos
├── logs/                         # Per-run and master logs
├── profile/                      # Saved profile JSONs
├── requirements.txt              # Python dependencies
└── README.md

````

---

## Requirements

- **Python 3.9+** (3.10–3.12 recommended)
- A **virtual environment** (`venv` or `conda`)
- **Qloo Hackathon API key** (or Qloo key for your account)
- **Gemini API key** (Google Generative AI)

Install dependencies:

```bash
pip install -r requirements.txt
````

> If you add scikit-learn or other libs, be sure your `requirements.txt` includes them:
>
> ```
> streamlit
> requests
> matplotlib
> numpy
> scikit-learn
> google-generativeai==0.8.5
> ```

---

## Quick Start (Local)

```bash
# 1) Clone and enter repo
git clone https://github.com/<your-username>/culturegraph.git
cd culturegraph

# 2) Create & activate venv
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Add your API keys (see next section)

# 5) Run the app
streamlit run app.py
```

---

## Configuration & Secrets

### Option A — Use **Streamlit Secrets**

Create `.streamlit/secrets.toml` (for local dev) and add:

```toml
API_KEY = "YOUR_QLOO_OR_TASTE_API_KEY"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Then, **in `config.py`**:

```python
import streamlit as st

API_KEY = st.secrets["API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

SEARCH_URL = "https://hackathon.api.qloo.com/search"
COMPARE_URL = "https://hackathon.api.qloo.com/v2/insights/compare"

HEADERS = {
    "accept": "application/json",
    "X-Api-Key": API_KEY
}
```

> On **Streamlit Cloud**, do **not** commit secrets. Set them in:
> **Manage App → Settings → Secrets**.

### Option B — Use environment variables

```bash
export API_KEY="..."
export GEMINI_API_KEY="..."
```

And read them in `config.py` with `os.getenv`.

---

## Running the App

```bash
streamlit run app.py
```

The UI walks you through:

1. Personal details
2. Cultural preferences (music/film/brands/books/travel/podcasts/TV/games)
3. Scenario-based questions (27 items with sensible defaults)

On **Submit**, the app:

* Resolves tastes → Qloo entity IDs
* Computes **taste compatibility** (Qloo), **NLP similarity**, and **Gemini score**
* Saves a profile JSON under `/profile`
* Writes a per-run CSV under `/logs`
* Updates the **master log** CSV (for future batch comparisons)
* Ranks matches and surfaces the **best match**
* Loads the best match’s JSON and shows their **first\_name / email / post**

---

## What Gets Saved

### Profile JSON (example)

`/profile/VM-jane-20250801T103000.json`

```json
{
  "first_name": "Jane",
  "email": "jane@startup.com",
  "post": "CTO",
  "form_data": { ...all UI inputs... },
  "taste_analysis": { ...derived tags by category... },
  "UUID": ["urn:entity:artist:...", "..."],
  "NLP": [
    "I listen first and then decide.",
    "I prefer async with weekly syncs.",
    "... (27 answers total) ..."
  ]
}
```

### Master log CSV

`/logs/master_entity_log.csv` grows with every submitted profile and includes:

* `filename` (without `.json`)
* `full_entity_ids` (list of UUIDs)
* `scenario_answers` (list of 27 answers)

---

## Scoring & Logs

* **Taste score**: Weighted average over Qloo tags (popularity-weighted).
* **NLP score**: Mean cosine similarity of per-question TF-IDF vectors.
* **Gemini score**: LLM evaluates both answer sets and returns `[0..1]` + reasoning.
* **mean**: Aggregate you define (e.g., average of the three above) to rank matches.

> The function `batch_compatibility_check(...)` writes these to the CSV so the UI can highlight the best match and pull their JSON to show **name/email/role**.

---

## Deploy to Streamlit Cloud

1. Push your repo to GitHub.
2. Go to **[https://streamlit.io/cloud](https://streamlit.io/cloud) → New app**.
3. Select your repo, branch (`main`), and main file (`app.py`).
4. In **Settings → Secrets**, add:

```toml
API_KEY="..."
GEMINI_API_KEY="..."
```

5. Click **Deploy**. The app will auto-redeploy on every push.

---

## Common Issues & Fixes

**`ModuleNotFoundError: scikit-learn`**
→ Add `scikit-learn` to `requirements.txt`, push, redeploy.

**`KeyError: st.secrets["API_KEY"]`**
→ You haven’t set secrets in Streamlit Cloud. Add keys under **Manage app → Settings → Secrets**.

**`google.generativeai has no attribute GenerativeModel`**
→ Your `google-generativeai` version is too old.
`pip install --upgrade google-generativeai==0.8.5`

**Protobuf / grpc version conflicts**
→ Upgrade `pip` and reinstall:
`python -m pip install --upgrade pip`
`pip install --upgrade google-generativeai`

**File not found when loading matched JSON**
→ Remember to append `.json` when loading a profile file:
`f"profile/{match['filename']}.json"`

---

## Extending the App

* **Add or edit scenario questions**: `form_Questions.py`
* **Add categories or inputs**: extend `categories` in `form_Questions.py` and render logic in `app.py`
* **Adjust weights / mean**: edit how `mean` is computed in your logging function
* **Swap LLM**: `compatibility.py → get_gemini_score` is the shim for model prompts & parsing

---

## Contributing

1. Create a new branch: `git checkout -b feature/my-change`
2. Make your changes & add tests if applicable
3. Commit: `git commit -m "Add X / Fix Y"`
4. Push: `git push origin feature/my-change`
5. Open a Pull Request to `main`


### Questions?

Open an issue or reach out. If you share a failing log/stack trace (minus secrets), we’ll help you fix it quickly.

```

---
