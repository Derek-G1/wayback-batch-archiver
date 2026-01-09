import os
import requests
import time
import csv
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load API keys from the .env file
load_dotenv()

def log_to_csv(original_url, archive_url, status):
    """Saves the result to a local file named archive_history.csv"""
    file_exists = os.path.isfile("archive_history.csv")
    with open("archive_history.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Original URL", "Wayback Link", "Status"])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, original_url, archive_url, status])

def wait_for_completion(job_id, access_key, secret_key, original_url, max_tries=12):
    """Polls the status for 2 minutes and logs the result."""
    status_url = f"https://web.archive.org/save/status/{job_id}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"LOW {access_key}:{secret_key}"
    }

    print(f"⏳ Waiting for archival (Max: 2 mins)...")
    
    tries = 0
    while tries < max_tries:
        try:
            response = requests.get(status_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                
                if status == "success":
                    ts = data.get("timestamp")
                    final_url = f"https://web.archive.org/web/{ts}/{original_url}"
                    print(f"\n\n✨ SUCCESS! Permanent Link: {final_url}")
                    log_to_csv(original_url, final_url, "Success")
                    return True
                elif status == "error":
                    msg = data.get("message")
                    print(f"\n\n❌ Archival failed: {msg}")
                    log_to_csv(original_url, "N/A", f"Error: {msg}")
                    return False
                else:
                    for _ in range(10):
                        print(".", end="", flush=True)
                        time.sleep(1)
            tries += 1
        except Exception:
            return False

    print(f"\n⏰ Timeout. Check manually: {status_url}")
    log_to_csv(original_url, status_url, "Timeout/Pending")
    return False

def save_site_today(target_url, access_key, secret_key):
    """Triggers archival and handles the result."""
    save_endpoint = "https://web.archive.org/save/"
    headers = {
        "Accept": "application/json",
        "Authorization": f"LOW {access_key}:{secret_key}"
    }
    payload = {'url': target_url, 'capture_all': '1', 'capture_screenshot': '1', 'force_get': '1'}

    print(f"\n🚀 Initializing capture for: {target_url}")
    
    try:
        response = requests.post(save_endpoint, data=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            job_id = data.get("job_id") or response.headers.get("X-Archive-Wayback-Job-ID")
            
            if job_id:
                print(f"✅ Capture submitted! Job ID: {job_id}")
                wait_for_completion(job_id, access_key, secret_key, target_url)
            else:
                history = f"https://web.archive.org/web/*/{target_url}"
                print(f"✅ Accepted (cached). History: {history}")
                log_to_csv(target_url, history, "Accepted (No ID)")
        else:
            print(f"⚠️ API Error: {response.status_code}")
            log_to_csv(target_url, "N/A", f"API Error {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    try:
        ACCESS = os.getenv("WAYBACK_ACCESS_KEY")
        SECRET = os.getenv("WAYBACK_SECRET_KEY")

        # =========================================================
        # 📝 HOW TO EDIT YOUR LIST OF SITES:
        # 1. Each URL must be inside double quotes " "
        # 2. Add a comma , after every URL except the very last one.
        # 3. To archive just ONE site, keep only one line (no comma needed).
        # =========================================================
        sites_to_archive = [
            "https://example.com",
        ]
        # =========================================================

        if ACCESS and SECRET:
            for site in sites_to_archive:
                save_site_today(site, ACCESS, SECRET)
            print("\n🏁 All tasks complete. History saved to 'archive_history.csv'")
        else:
            print("❌ ERROR: API keys not found in .env! Check your file.")

    except KeyboardInterrupt:
        print("\n\n🛑 Script stopped by user.")
        sys.exit(0)