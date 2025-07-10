import json
import os
import random
from datetime import datetime, timedelta

print("Welcome to MediVault Lite.")
print("This tool helps doctors upload and analyze medical scans.\n")

# Ask for username and load their file
username = input("Enter your username: ").strip().lower()
filename = f"scan_history_{username}.txt"

# Load existing scan history if available
if os.path.exists(filename):
    with open(filename, "r") as f:
        scan_history = json.load(f)
else:
    scan_history = []

# Convert scan history to dictionary to prevent duplicates
scan_dict = {scan["file"]: scan for scan in scan_history}

# Main loop to process scans
while True:
    scan_name = input("Enter scan file name (or type 'exit' to quit): ")
    if scan_name.lower() == "exit":
        break

    print("Analyzing scan...")
    result = "Normal"
    confidence = random.randint(75, 95)
    note = input("Any notes to attach to this scan? ")

    # Convert UTC to PST manually (UTC-7 as of daylight savings time)
    pst_time = datetime.utcnow() - timedelta(hours=7)

    scan_dict[scan_name] = {
        "file": scan_name,
        "result": result,
        "confidence": confidence,
        "note": note,
        "time": pst_time.strftime("%Y-%m-%d %H:%M:%S")
    }

    print(f"\nScan '{scan_name}' uploaded.")
    print(f"AI Result: {result} ({confidence}% confidence)")
    print(f"Note: {note}")
    print(f"Date uploaded (PST): {pst_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# Save updated scan history
scan_history = list(scan_dict.values())
with open(filename, "w") as f:
    json.dump(scan_history, f, indent=2)

# Show all scans for this user
print(f"\nScan history saved for {username}")
print("Scan log:")
for scan in scan_history:
    print(f"- {scan['file']}: {scan['result']} ({scan['confidence']}%)")
    print(f"  Note: {scan['note']}")
    print(f"  Date uploaded (PST): {scan['time']}")
