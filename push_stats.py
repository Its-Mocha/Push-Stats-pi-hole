import requests
import json
import datetime
import os
from dotenv import load_dotenv

# --- CONFIG ---
load_dotenv()

PIHOLE_URL = os.getenv("PI_HOLE_IP")
APP_PASSWORD = os.getenv("PI_HOLE_PASSWORD")
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{os.getenv('JSONBIN_BIN_ID')}"
MASTER_KEY = os.getenv("JSONBIN_MASTER_KEY")

def sync_stats():
    # We define sid here so we can check it during logout
    sid = None 
    
    try:
        # 1. AUTHENTICATE
        auth_resp = requests.post(f"{PIHOLE_URL}/api/auth", json={"password": APP_PASSWORD})
        sid = auth_resp.json().get("session", {}).get("sid") 
        
        if not sid:
            print("❌ Auth Failed! Response:", auth_resp.text)
            return

        # 2. FETCH SUMMARY
        headers = {"X-FTL-SID": sid}
        stats_resp = requests.get(f"{PIHOLE_URL}/api/stats/summary", headers=headers)
        data = stats_resp.json()

        # 3. MAPPED PAYLOAD
        payload = {
            "dns_queries_today": data.get("queries", {}).get("total", 0),
            "ads_blocked_today": data.get("queries", {}).get("blocked", 0),
            "ads_percentage_today": round(data.get("queries", {}).get("percent_blocked", 0), 1),
            "domains_being_blocked": data.get("gravity", {}).get("domains_being_blocked", 0),
            "active_clients": data.get("clients", {}).get("active", 0),
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        }

      # 4. PUSH TO JSONBIN (Updated for better Auth compatibility)
        cloud_headers = {
            "Content-Type": "application/json",
            "X-Master-Key": MASTER_KEY,
            "X-Bin-Private": "true",
            "X-Bin-Versioning": "false"
        }
        
        # We'll use a session object to ensure the connection is stable
        session = requests.Session()
        req = session.put(JSONBIN_URL, json=payload, headers=cloud_headers)
        
        if req.status_code == 200:
            print("✅ Success! Data is in the cloud.")
            latest_update = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
         # 2. Your data payload
            data_to_cloud = {
                "status": "enabled",
                "last_updated": latest_update
            }
            print(f"Data pushed! Last Updated: {latest_update}")
        else:
            print(f"❌ Cloud Error ({req.status_code}): {req.text}")

    except Exception as e:
        print(f"❌ Script Error: {e}")

    finally:
        # 5. LOGOUT (Cleanup session regardless of success or failure)
        if sid:
            try:
                logout_resp = requests.delete(f"{PIHOLE_URL}/api/auth", headers={"X-FTL-SID": sid})
                if logout_resp.status_code == 204:
                    print("🧹 Session cleared from Pi-hole.")
            except:
                print("⚠️ Failed to close Pi-hole session.")

if __name__ == "__main__":
    sync_stats()