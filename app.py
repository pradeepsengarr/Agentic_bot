# Exploring the Agentic bot

import streamlit as st
import requests
import re
import os

# APIs that used
TOGETHER_API_KEY = "tgp_v1_ZytvDbMu9PMwIlnBZEfYSq9nzJAYwS0MecjY9Kt7RxE"
SERPER_API_KEY = "75f06519187851ad63486c3012b34c5e0e6501f1"

# General Structure
def generate_startup_ideas(prompt):
    url = "https://api.together.xyz/v1/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "prompt": f"""
Suggest 3 unique startup ideas based on this interest: \"{prompt}\".
Each idea should be short, clear, and numbered like this:
1. [Idea Title]: [One-sentence description]
2. ...
""",
        "max_tokens": 300,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" not in result:
        return []

    raw_text = result["choices"][0].get("text", "").strip()
    ideas = re.findall(r"\d+\.\s*(.*?):\s*(.*)", raw_text)
    return [f"{i+1}. {title.strip()}: {desc.strip()}" for i, (title, desc) in enumerate(ideas)]

# For URL
def market_research(query):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    data = {"q": query}
    res = requests.post(url, headers=headers, json=data)
    results = res.json()
    return [r["title"] + " - " + r["link"] for r in results.get("organic", [])[:5]]

# UI
st.set_page_config(page_title="Startup Co-Founder Agent", layout="centered")
st.title("🚀 Startup Co-Founder Agent")
st.write("Get startup ideas + instant market research with free AI tools!")

user_prompt = st.text_input("What are you interested in building a startup around?", "AI for education")

if st.button("Generate Startup Ideas"):
    if not TOGETHER_API_KEY or not SERPER_API_KEY:
        st.error("API keys are not set. Please configure them in your Hugging Face Space secrets.")
    else:
        with st.spinner("Generating ideas and researching..."):
            ideas = generate_startup_ideas(user_prompt)
            if not ideas:
                st.error("No startup ideas generated. Check API keys or try again.")
            else:
                st.subheader("💡 Startup Ideas")
                for idea in ideas:
                    st.markdown(f"- {idea}")

                st.subheader("🔍 Market Research")
                for idea in ideas:
                    title = idea.split(":")[0].strip()
                    st.markdown(f"**📌 {title}**")
                    results = market_research(title)
                    for r in results:
                        st.markdown(f"- {r}")
