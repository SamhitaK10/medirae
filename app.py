import streamlit as st
import random
import json
import os
from datetime import datetime, timedelta

st.title("MediVault Lite")
st.subheader("Secure Scan Analysis for Doctors")

# Get username
username = st.text_input("Enter your username:", max_chars=20)
if not username:
    st.stop()
filename = f"scan_history_{username}.json"

# Load history
if os.path.exists(filename):
    with open(filename, "r") as f:
        scan_history = json.load(f)
else:
    scan_history = []

# Upload & analyze
st.header("Upload and Analyze a Scan")
scan_file = st.file_uploader("Upload scan file (image or PDF)")
note = st.text_input("Notes for this scan:")

if st.button("Analyze Scan") and scan_file:
    result = random.choice(["Normal", "Possible Pneumonia", "Abnormal Shadow"])
    confidence = random.randint(75, 95)
    pst_time = datetime.utcnow() - timedelta(hours=7)
    timestamp = pst_time.strftime("%Y-%m-%d %H:%M:%S")

    new_scan = {
        "file": scan_file.name,
        "result": result,
        "confidence": confidence,
        "note": note,
        "time": timestamp
    }

    scan_history.append(new_scan)
    with open(filename, "w") as f:
        json.dump(scan_history, f, indent=2)

    st.success(f"Scan '{scan_file.name}' uploaded and analyzed.")
    st.write(f"Result: {result} ({confidence}% confidence)")
    st.write(f"Note: {note}")
    st.write(f"Date: {timestamp}")

# View history
st.header("Scan History")
if scan_history:
    for scan in reversed(scan_history):
        st.write(f"**{scan['file']}** | {scan['result']} ({scan['confidence']}%)")
        st.write(f"Note: {scan['note']}")
        st.write(f"Date: {scan['time']}")
        st.markdown("---")
else:
    st.info("No scan history yet.")
