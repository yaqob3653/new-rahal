import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd

# Clear ALL caches
st.cache_data.clear()
st.cache_resource.clear()

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("\n" + "="*60)
print("TESTING DATA FETCH (Same logic as dashboard)")
print("="*60)

# 1. Get latest date from waiting_times
wait_latest = supabase.table("waiting_times").select("work_date").order("work_date", desc=True).limit(1).execute()

if wait_latest.data:
    wait_date = wait_latest.data[0]['work_date']
    print(f"\n✓ Latest waiting_times date: {wait_date}")
    
    # Get Wait Times for this date
    wait_response = supabase.table("waiting_times").select("wait_time_max, entity_description_short").eq("work_date", wait_date).limit(1000).execute()
    wait_data = pd.DataFrame(wait_response.data)
    print(f"  - Records found: {len(wait_data)}")
    if not wait_data.empty:
        print(f"  - Avg wait time: {int(wait_data['wait_time_max'].mean())} min")
else:
    print("\n✗ No data in waiting_times")
    wait_date = None
    wait_data = pd.DataFrame()

# 2. Get latest date from attendance
att_latest = supabase.table("attendance").select("usage_date").order("usage_date", desc=True).limit(1).execute()

if att_latest.data:
    att_date = att_latest.data[0]['usage_date']
    print(f"\n✓ Latest attendance date: {att_date}")
    
    # Get Attendance for this date
    att_response = supabase.table("attendance").select("attendance").eq("usage_date", att_date).execute()
    attendance_data = pd.DataFrame(att_response.data)
    print(f"  - Records found: {len(attendance_data)}")
    if not attendance_data.empty:
        total = int(attendance_data['attendance'].sum())
        print(f"  - Total visitors: {total:,}")
else:
    print("\n✗ No data in attendance")
    att_date = None
    attendance_data = pd.DataFrame()

# 3. Get facilities
fac_response = supabase.table("facilities").select("facility_id").execute()
facilities_count = len(fac_response.data) if fac_response.data else 0
print(f"\n✓ Total facilities: {facilities_count}")

# 4. Calculate System Health
if not wait_data.empty and facilities_count > 0:
    active_facilities = wait_data['entity_description_short'].nunique()
    system_health = min(100.0, (active_facilities / facilities_count) * 100)
    print(f"✓ System Health: {system_health:.1f}%")
    print(f"  - Active facilities: {active_facilities}/{facilities_count}")
else:
    print("✗ Cannot calculate system health")

print("\n" + "="*60)
print("EXPECTED DASHBOARD VALUES:")
print("="*60)
if not attendance_data.empty:
    print(f"Total Visitors: {int(attendance_data['attendance'].sum()):,}")
else:
    print("Total Visitors: 0")
    
if not wait_data.empty:
    print(f"Avg Wait Time: {int(wait_data['wait_time_max'].mean())} min")
else:
    print("Avg Wait Time: 0")
    
print(f"System Health: {system_health:.1f}%" if not wait_data.empty and facilities_count > 0 else "System Health: 0.0%")
print("="*60)
