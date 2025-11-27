import os
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Supabase credentials missing.")
    exit()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("--- Checking 'attendance' table ---")
try:
    res = supabase.table("attendance").select("*").limit(5).execute()
    print(f"Count: {len(res.data)}")
    if res.data:
        print(pd.DataFrame(res.data).head())
    else:
        print("Table is empty.")
except Exception as e:
    print(f"Error: {e}")

print("\n--- Checking 'waiting_times' table ---")
try:
    res = supabase.table("waiting_times").select("*").limit(5).execute()
    print(f"Count: {len(res.data)}")
    if res.data:
        print(pd.DataFrame(res.data).head())
    else:
        print("Table is empty.")
except Exception as e:
    print(f"Error: {e}")

print("\n--- Checking 'facilities' table ---")
try:
    res = supabase.table("facilities").select("*").limit(5).execute()
    print(f"Count: {len(res.data)}")
    if res.data:
        print(pd.DataFrame(res.data).head())
    else:
        print("Table is empty.")
except Exception as e:
    print(f"Error: {e}")
