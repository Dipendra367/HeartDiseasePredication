import os

filename = "cleaned_npl2019.csv"

if os.path.exists(filename):
    print(f"✅ File '{filename}' exists.")
else:
    print(f"❌ File '{filename}' does NOT exist.")
