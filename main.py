import os
import re
import time
from datetime import datetime

def update_file_dates(base_path: str):
    # Pattern to match filenames like: photo_1@26-10-2025_12-30-16_thumb.jpg
    pattern = re.compile(r'@(\d{2}-\d{2}-\d{4})_(\d{2}-\d{2}-\d{2})')

    for root, _, files in os.walk(base_path):
        for file in files:
            match = pattern.search(file)
            if not match:
                continue

            file_path = os.path.join(root, file)
            try:
                stat_info = os.stat(file_path)
                old_mod_time = datetime.fromtimestamp(stat_info.st_mtime)
                old_create_time = datetime.fromtimestamp(stat_info.st_ctime)
            except Exception as e:
                print(f"⚠️ Could not read timestamps for {file}: {e}")
                continue

            date_str, time_str = match.groups()
            try:
                new_dt = datetime.strptime(f"{date_str}_{time_str}", "%d-%m-%Y_%H-%M-%S")
            except ValueError:
                print(f"Skipping invalid date format in: {file}")
                continue

            # Convert datetime to timestamp
            new_timestamp = time.mktime(new_dt.timetuple())

            os.utime(file_path, (new_timestamp, new_timestamp))

            print(
                f"✅ {file}\n"
                f"   Old Created: {old_create_time}\n"
                f"   Old Modified: {old_mod_time}\n"
                f"   ➜ New Date: {new_dt}\n"
            )

if __name__ == "__main__":
    path = input("Enter the directory path to scan: ").strip()
    if not os.path.isdir(path):
        print("❌ Invalid path")
    else:
        update_file_dates(path)
