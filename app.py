import streamlit as st
import random
import json
import os
from datetime import datetime, timedelta

st.title("Medirae")
st.subheader("Secure Scan Analysis for Doctors")

# --- USER LOGIN ---
username = st.text_input("Enter your username:", max_chars=20)
password = st.text_input("Enter password:", type="password")

if not username or password != "testpass":
    st.warning("Enter username and correct password to continue. (Hint: password is 'testpass')")
    st.stop()

filename = f"scan_history_{username}.json"

# --- DEMO DATA ---
if username.lower() == "demo" and not os.path.exists(filename):
    sample_scan = {
        "file": "sample_chest_xray.jpg",
        "result": "Abnormal",
        "confidence": 87,
        "note": "Cough and fever for 3 days",
        "time": (datetime.utcnow() - timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(filename, "w") as f:
        json.dump([sample_scan], f, indent=2)

# --- LOAD HISTORY ---
if os.path.exists(filename):
    with open(filename, "r") as f:
        scan_history = json.load(f)
else:
    scan_history = []

# --- UPLOAD & ANALYZE ---
st.header("Upload and Analyze a Scan")
scan_file = st.file_uploader("Upload scan file (image or PDF)")
note = st.text_input("Notes for this scan:")

if st.button("Analyze Scan") and scan_file:
    result = random.choice(["Normal", "Abnormal", "Abnormal Shadow"])
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
    st.write(f"Result: **{result}** ({confidence}% confidence)")
    st.write(f"Note: {note}")
    st.write(f"Date: {timestamp}")

    # --- DOWNLOAD REPORT ---
    report = f"""Scan Report for {scan_file.name}
Result: {result} ({confidence}% confidence)
Note: {note}
Date: {timestamp}
"""
    st.download_button("Download Report", report, file_name="scan_report.txt")

# --- SCAN HISTORY ---
st.header("Scan History")
if scan_history:
    for scan in reversed(scan_history):
        st.write(f"**{scan['file']}** | {scan['result']} ({scan['confidence']}%)")
        st.write(f"Note: {scan['note']}")
        st.write(f"Date: {scan['time']}")
        st.markdown("---")
else:
    st.info("No scan history yet.")
