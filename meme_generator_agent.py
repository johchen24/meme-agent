import re
import asyncio
import streamlit as st
from browser_use import Agent
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


async def generate_meme(query: str, model: str, api_key: str) -> str | None:
    if model == "Claude":
        llm = ChatAnthropic(
            model="claude-3-7-sonnet-20250219",
            api_key=api_key,
            temperature=0.3
    )
    elif model == "Deepseek":
        # DeepSeek API is OpenAI-compatible
        llm = ChatOpenAI(
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",      # V3.1-backed chat model
            api_key=api_key,
            temperature=0.3
        )
    else:  # "OpenAI"
        llm = ChatOpenAI(
            model="gpt-4o",
            api_key=api_key,
            temperature=0.3
        )

    # --- vision toggle logic ---
    if model == "Deepseek":
        # DeepSeek chat API doesn't accept images; avoid agent vision mode to prevent errors.
        use_vision = False
        st.info("DeepSeek chat does not support image inputs; running without vision.")
    else:
        use_vision = True
    
    task_description = f"""
    You are a expert, precise meme-making browser agent.
    Your ONLY goal: generate a meme on Imgflip that matches the user's idea and return the final meme page URL.

    Rules:
    - Follow steps IN ORDER. If something fails, retry up to 2 times, then try a different template.
    - Be literal and specific. Do not open extra tabs or unrelated pages.
    - Never ask for login or upload. Stay on public meme templates.

    Steps:
    1) Open https://imgflip.com/memetemplates
    2) Find the search box for templates. Search for EXACTLY ONE MAIN ACTION VERB extracted from this idea: "{query}"
    - Examples of verbs: laugh, cry, panic, flex, betray, grind, wait.
    - If you can’t find a verb, pick a common neutral template (e.g., “Distracted Boyfriend”).
    3) Pick ONE template that metaphorically fits the idea. Click its “Add Caption” button.
    4) In the caption page:
    - Write a concise **Top Text** that sets up context for "{query}".
    - Write a concise **Bottom Text** that delivers a punchline or outcome for "{query}".
    - Keep it readable and not too long; prefer 6–10 words per line.
    - It's not a requirement to use both top and bottom text (or whatever is available). Prioritize accuracy to the user's idea, humor, creativity, and interpretability.
    5) Check the live preview. If the joke is confusing, edit the texts once to improve clarity.
    6) Click the button that generates the meme (usually “Generate”).
    7) After it loads, copy the FINAL meme page URL. It should look like:
    https://imgflip.com/i/<MEME_ID>

    Output:
    - Return ONLY the final meme page URL as plain text on its own line.
    - Do NOT include any other commentary.
    """

    agent = Agent(
        task=task_description,
        llm=llm,
        use_vision=use_vision,
        max_actions_per_step=5,
        max_failures=25
    )

    history = await agent.run()
    final_result = history.final_result() # this should be the precise URL
    
    final_text = (final_result or "").strip().strip("<>")  # handle None + angle brackets

    # 1) Prefer the page URL we asked for in the prompt
    m = re.search(r'https?://(?:www\.)?imgflip\.com/i/([A-Za-z0-9]+)(?=[^\w]|$)', final_text)
    if m:
        meme_id = m.group(1)
        return f"https://i.imgflip.com/{meme_id}.jpg"

    # 2) Fallback: accept a direct image URL if that’s what we got
    m2 = re.search(r'https?://i\.imgflip\.com/([A-Za-z0-9]+)\.(?:jpg|png|gif)(?:\?\S+)?', final_text)
    if m2:
        return m2.group(0)

    return None

    
def main():
    st.title("Meme Generator Agent with Browser Use - Small Project for learning by Johnnie Chen 🐀")
    st.info("This browser agent automates browser use and generates memes on Imgflip. Pick a model, enter your API key, and describe your meme idea.")
    
    with st.sidebar:
        st.subheader("⚙️ Model Configuration")
        
        # pick a model
        model = st.selectbox(
            "Choose an AI model",
            ["Claude", "Deepseek", "OpenAI"],
            
        )

if __name__ == "__main__":
    main()