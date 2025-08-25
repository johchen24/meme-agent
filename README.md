# Meme Agent

A tiny Streamlit app that uses a browser-automation **agent** to create memes on **Imgflip**.
- **browser-use** runs the agent loop (plan → act → repeat)
- **Playwright** drives Chromium to click/type
- **LangChain model clients** (Claude / GPT-4o / DeepSeek chat) provide the LLM
- **Streamlit** provides the simple UI


> This app is **BYOK (Bring Your Own Key)**. You’ll paste your own API key for the model you choose.

---

## Setup

```bash
# 1) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2) Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# 3) Install the Chromium browser for Playwright (one-time)
python -m playwright install chromium --with-deps

