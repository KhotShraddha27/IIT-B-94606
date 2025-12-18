import streamlit as st
import pandas as pd
from pandasql import sqldf
import os
from langchain.chat_models import init_chat_model

# ✅ Correct Groq initialization
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq",
    api_key=os.getenv("GROQ_API_KEY")
)

st.set_page_config(page_title="CSV SQL Assistant", layout="wide")
st.title("📊 CSV SQL Assistant with LLM")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Preview of Data")
    st.dataframe(df.head())

    st.subheader("🧾 CSV Schema")
    st.write(df.dtypes)

    user_question = st.text_input("Ask a question about this CSV data:")

    if st.button("Run Query") and user_question:

        sql_prompt = f"""
        Table Name: df
        Table Schema: {df.dtypes}
        Question: {user_question}
        Instruction:
        Write a SQL query for the above question.
        Generate SQL query only in plain text.
        If not possible, output 'Error'.
        """

        sql_response = llm.invoke(sql_prompt)
        sql_query = sql_response.content.strip()

        st.subheader("🧠 Generated SQL")
        st.code(sql_query, language="sql")

        if sql_query.lower() != "error":
            try:
                result = sqldf(sql_query, {"df": df})

                st.subheader("📈 Query Result")
                st.dataframe(result)

                explain_prompt = f"""
                SQL Query:
                {sql_query}

                Result:
                {result.to_string(index=False)}

                Explain the result in simple English.
                """

                explanation = llm.invoke(explain_prompt)

                st.subheader("🗣️ Explanation")
                st.write(explanation.content)

            except Exception as e:
                st.error(f"Execution Error: {e}")
        else:
            st.error("LLM could not generate a valid SQL query.")
