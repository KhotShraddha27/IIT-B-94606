import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="CSV Management App", layout="wide")

USERS_FILE = "users.csv"
HISTORY_FILE = "userfiles.csv"

# ---------------- FILE INITIALIZATION ----------------
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["userid", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["userid", "csv_filename", "upload_datetime"]).to_csv(
        HISTORY_FILE, index=False
    )

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- SIDEBAR MENU ----------------
def sidebar_menu():
    if st.session_state.user is None:
        return st.sidebar.radio("Menu", ["Home", "Login", "Register"])
    else:
        return st.sidebar.radio(
            "Menu", ["Explore CSV", "See History", "Logout"]
        )

# ---------------- HOME ----------------
def home():
    st.title("🏠 Home")
    st.write("Welcome to the CSV Management Application")
    st.info("Please login or register to continue")

# ---------------- REGISTER ----------------
def register():
    st.title("📝 Register")

    userid = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if userid.strip() == "" or password.strip() == "":
            st.error("User ID and Password cannot be empty")
            return

        users = pd.read_csv(USERS_FILE)

        users["userid"] = users["userid"].astype(str).str.strip()

        if userid.strip() in users["userid"].values:
            st.error("User already exists")
        else:
            users.loc[len(users)] = [userid.strip(), password.strip()]
            users.to_csv(USERS_FILE, index=False)
            st.success("Registration successful. Please login.")

# ---------------- LOGIN ----------------
def login():
    st.title("🔐 Login")

    userid = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = pd.read_csv(USERS_FILE)

        # 🔧 IMPORTANT FIX (spaces + datatype)
        users["userid"] = users["userid"].astype(str).str.strip()
        users["password"] = users["password"].astype(str).str.strip()

        userid = userid.strip()
        password = password.strip()

        valid = users[
            (users["userid"] == userid) &
            (users["password"] == password)
        ]

        if not valid.empty:
            st.session_state.user = userid
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- EXPLORE CSV ----------------
def explore_csv():
    st.title("📊 Explore CSV")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        history = pd.read_csv(HISTORY_FILE)
        history.loc[len(history)] = [
            st.session_state.user,
            uploaded_file.name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        history.to_csv(HISTORY_FILE, index=False)

        st.success("CSV uploaded and history saved")

# ---------------- SEE HISTORY ----------------
def see_history():
    st.title("🕒 Upload History")

    history = pd.read_csv(HISTORY_FILE)
    history["userid"] = history["userid"].astype(str).str.strip()

    user_history = history[history["userid"] == st.session_state.user]

    if user_history.empty:
        st.info("No uploads yet")
    else:
        st.dataframe(user_history)

# ---------------- LOGOUT ----------------
def logout():
    st.session_state.user = None
    st.success("Logged out successfully")
    st.rerun()

# ---------------- APP FLOW ----------------
choice = sidebar_menu()

if st.session_state.user is None:
    if choice == "Home":
        home()
    elif choice == "Login":
        login()
    elif choice == "Register":
        register()
else:
    if choice == "Explore CSV":
        explore_csv()
    elif choice == "See History":
        see_history()
    elif choice == "Logout":
        logout()