import json
import csv

# Load JSON
with open('bandpass_export.json', 'r') as f:
    data = json.load(f)

# Export CSV
with open('bandpass_export.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for antenna, amplitudes in data.items():
        writer.writerow([antenna] + amplitudes)