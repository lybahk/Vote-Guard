import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

def login():
    st.title("Login / Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials. Try again.")
        except requests.exceptions.RequestException:
            st.error("Server not responding. Make sure the backend is running.")

def vote_page():
    st.title("Vote for Your Candidates")
    
    if not st.session_state["logged_in"]:
        st.warning("Please log in first.")
        return

    try:
        response = requests.get(f"{BASE_URL}/candidates")
        if response.status_code == 200:
            candidates = response.json()["candidates"]
        else:
            st.error("Failed to fetch candidates.")
            return
    except requests.exceptions.RequestException:
        st.error("Server not responding.")
        return

    votes = {}
    for position, candidates_list in candidates.items():
        st.subheader(position)
        votes[position] = st.radio(f"Select your candidate for {position}", candidates_list)

    if st.button("Submit Vote"):
        data = {"username": st.session_state["username"], "votes": votes}
        try:
            response = requests.post(f"{BASE_URL}/vote", json=data)
            if response.status_code == 200:
                st.success("Vote submitted successfully!")
            else:
                st.error("Failed to submit vote.")
        except requests.exceptions.RequestException:
            st.error("Server not responding.")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.rerun()

if st.session_state["logged_in"]:
    vote_page()
else:
    login()
