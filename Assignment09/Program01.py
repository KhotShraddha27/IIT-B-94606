import os
import time
import pandas as pd
import streamlit as st
from pandasql import sqldf
from langchain.chat_models import init_chat_model

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq",
    api_key=os.getenv("GROQ_API_KEY")
)

st.set_page_config(page_title="Multi-Agent App", layout="wide")
st.title("Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = None

if "sunbeam_df" not in st.session_state:
    st.session_state.sunbeam_df = None

if "csv_df" not in st.session_state:
    st.session_state.csv_df = None

agent = st.sidebar.selectbox(
    "Choose Agent",
    ["CSV Question Answering Agent", "Sunbeam Web Scraping Agent"]
)

st.session_state.selected_agent = agent  

if agent == "CSV Question Answering Agent":
    st.header("📊 CSV Question Answering Agent")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file:
        st.session_state.csv_df = pd.read_csv(uploaded_file)
        st.success("CSV loaded successfully")

    df = st.session_state.csv_df
    if df is not None:
        st.subheader("CSV Schema")
        st.write(df.dtypes)

        with st.form("csv_form"):
            question = st.text_input("Ask a question about this CSV")
            submit_csv = st.form_submit_button("Submit")

        if submit_csv and question:
            prompt = f"""
Table name is df

Table schema:
{df.dtypes}

Question:
{question}

Write only a SQLite SELECT query.
Do NOT use markdown or code blocks.
If not possible, return Error.
"""
            response = llm.invoke(prompt)
            sql_query = response.content.strip().replace("```sql", "").replace("```", "").strip()

            st.write("**Generated SQL:**")
            st.code(sql_query, language="sql")

            if sql_query != "Error":
                try:
                    result = sqldf(sql_query, {"df": df})
                    st.write("**Result:**")
                    st.dataframe(result)

                    explain_prompt = f"""
Explain this result in simple English.

Question:
{question}

Result:
{result}
"""
                    explanation = llm.invoke(explain_prompt).content
                    st.write("**Explanation:**")
                    st.write(explanation)

                    st.session_state.chat_history.append(("CSV Agent", question, explanation))

                except Exception as e:
                    st.error(f"SQL Error: {e}")
            else:
                st.error("Could not generate SQL")

elif agent == "Sunbeam Web Scraping Agent":
    st.header("🌐 Sunbeam Web Scraping Agent")

    if st.button("Fetch Internship & Batch Info") or st.session_state.sunbeam_df is not None:

        if st.session_state.sunbeam_df is None:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )

            data = []
            try:
                driver.get("https://www.sunbeaminfo.in/internship")
                time.sleep(3)
                rows = driver.find_elements(By.XPATH, "//table//tr[td]")

                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 3:
                        batch = cols[1].text.strip()
                        start = cols[2].text.strip()
                        if batch or start:
                            data.append({"Batch Name": batch, "Start Date": start})
            finally:
                driver.quit()

            st.session_state.sunbeam_df = pd.DataFrame(data)

        sunbeam_df = st.session_state.sunbeam_df
        st.dataframe(sunbeam_df)
        with st.form("sunbeam_form"):
            question = st.text_input("Ask a question about Sunbeam internships")
            submit_sunbeam = st.form_submit_button("Submit")

        if submit_sunbeam and question:
            explain_prompt = f"""
Answer the following question using this data.

Data:
{sunbeam_df}
Question:
{question}

Explain the answer in simple English.
"""
            explanation = llm.invoke(explain_prompt).content
            st.write("**Explanation:**")
            st.write(explanation)

            st.session_state.chat_history.append(("Sunbeam Agent", question, explanation))
st.sidebar.subheader("📝 Chat History")

with st.sidebar.expander("View Chat History", expanded=True):
    if st.session_state.chat_history:
        for agent_name, question, _ in st.session_state.chat_history:  # show only question
            st.markdown(f"**{agent_name}**")
            st.markdown(f"Q: {question}")
            st.markdown("---")
    else:
        st.info("No questions asked yet.")