from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("\n" + "="*60)
print("QUICK DATA CHECK")
print("="*60)

# Get latest date from waiting_times
print("\n1. Latest date in WAITING_TIMES:")
try:
    wait_latest = supabase.table("waiting_times").select("work_date").order("work_date", desc=True).limit(1).execute()
    if wait_latest.data:
        latest_date = wait_latest.data[0]['work_date']
        print(f"   ✓ {latest_date}")
        
        # Now check if attendance has data for this date
        print(f"\n2. Checking ATTENDANCE for {latest_date}:")
        att_check = supabase.table("attendance").select("attendance, facility_name").eq("usage_date", latest_date).limit(5).execute()
        
        if att_check.data:
            print(f"   ✓ Found {len(att_check.data)} records!")
            total = sum(r['attendance'] for r in att_check.data)
            print(f"   ✓ Total visitors: {total}")
            print(f"   Sample records:")
            for r in att_check.data[:3]:
                print(f"      - {r.get('facility_name', 'N/A')}: {r['attendance']}")
        else:
            print(f"   ✗ NO DATA for {latest_date}")
            print(f"\n   Checking what dates ARE available in attendance:")
            att_dates = supabase.table("attendance").select("usage_date").order("usage_date", desc=True).limit(3).execute()
            if att_dates.data:
                print(f"   Available dates:")
                for d in att_dates.data:
                    print(f"      - {d['usage_date']}")
            else:
                print(f"   ✗ Attendance table is EMPTY!")
    else:
        print("   ✗ No data in waiting_times!")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*60)
