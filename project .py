from google.colab import files
uploaded = files.upload()

import pandas as pd
import concurrent.futures
import time
# Load CSV without header and set column names
df = pd.read_csv('students.csv', header=None)
df.columns = ['ID', 'Name', 'Age', 'Score'] # Set column names here
# Convert 'Score' column to numeric, handling errors
df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
# Initialize shared variables
high_scorers = []
failed_students = []
score_sum = 0
highest_score = 0
topper_name = ""
# Function to process each student record
def process_student(row):
global highest_score, topper_name
info = {}
score = row['Score'] # Now 'Score' column should exist
if score >= 80:
info['high'] = row
if score < 40:
info['fail'] = row
info['score'] = score
return info
# Start timing
start_time = time.time()
results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
results = list(executor.map(process_student, [row for _, row in df.iterrows()]))
total_score = 0
for res in results:
total_score += res['score']
if 'high' in res:
high_scorers.append(res['high'])
if 'fail' in res:
failed_students.append(res['fail'])
if res['score'] > highest_score:
highest_score = res['score']
topper_name = res.get('high', {}).get('Name', "Unknown")
# Display results
print("Students with score >= 80:")
print("-" * 40)
for student in high_scorers:
print(f"ID: {student['ID']} | Name: {student['Name']} | Age: {student['Age']} | Score:
{student['Score']}")
print("\nSummary")
print("-" * 40)
print(f"Total Students: {len(df)}")
print(f"High Scorers (>=80): {len(high_scorers)}")
print(f"Failed Students (<40): {len(failed_students)}")
print(f"Average Score: {total_score / len(df):.2f}")
print(f"Topper: {topper_name} with score {highest_score}")
print(f"\nExecution Time: {time.time() - start_time:.6f} seconds")
