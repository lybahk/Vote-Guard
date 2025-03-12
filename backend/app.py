import streamlit as st
import requests

st.title("Blockchain Voting System")

positions = ["President", "Vice President", "Secretary"]
candidates = {
    "President": ["Alice", "Bob"],
    "Vice President": ["Charlie", "David"],
    "Secretary": ["Eve", "Frank"]
}

position = st.selectbox("Select Position", positions)
if position:
    candidate = st.radio("Choose your candidate:", candidates[position])

    if st.button("Submit Vote"):
        response = requests.post("http://127.0.0.1:5000/submit_vote", json={"position": position, "candidate": candidate})
        if response.status_code == 200:
            st.success("Vote submitted successfully!")
        else:
            st.error("Error submitting vote.")

# Display Results
st.subheader("Election Results")
if st.button("Show Results"):
    response = requests.get("http://127.0.0.1:5000/get_results")
    if response.status_code == 200:
        results = response.json()
        st.json(results)
    else:
        st.error("Error fetching results.")
