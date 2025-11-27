from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("=" * 60)
print("Checking data availability in tables...")
print("=" * 60)

# Check waiting_times
print("\n1. WAITING_TIMES table:")
wait_dates = supabase.table("waiting_times").select("work_date").order("work_date", desc=True).limit(5).execute()
if wait_dates.data:
    print(f"   Latest 5 dates: {[d['work_date'] for d in wait_dates.data]}")
    print(f"   Total records: {len(wait_dates.data)}")
else:
    print("   ❌ No data found!")

# Check attendance
print("\n2. ATTENDANCE table:")
att_dates = supabase.table("attendance").select("usage_date, attendance").order("usage_date", desc=True).limit(5).execute()
if att_dates.data:
    print(f"   Latest 5 dates:")
    for d in att_dates.data:
        print(f"      - {d['usage_date']}: {d['attendance']} visitors")
else:
    print("   ❌ No data found!")

# Check facilities
print("\n3. FACILITIES table:")
fac_count = supabase.table("facilities").select("facility_id").execute()
print(f"   Total facilities: {len(fac_count.data) if fac_count.data else 0}")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)

if wait_dates.data and att_dates.data:
    latest_wait = wait_dates.data[0]['work_date']
    latest_att = att_dates.data[0]['usage_date']
    
    if latest_wait == latest_att:
        print(f"✅ Data is aligned! Both tables have data for: {latest_wait}")
    else:
        print(f"⚠️ Data mismatch!")
        print(f"   - waiting_times latest: {latest_wait}")
        print(f"   - attendance latest: {latest_att}")
        print(f"\n   Solution: Upload attendance data for {latest_wait}")
