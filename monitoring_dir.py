import time
import csv
from pathlib import Path



MONITORED_DIR = "watched_folder"
LOG_FILE = "directory_logs.csv"

previous_state = {}

def get_metadata(path):
    stats = path.stat()
    return {
        "type": "Directory" if path.is_dir() else "File",
        "size": stats.st_size,
        "permissions": oct(stats.st_mode),
        "owner": stats.st_uid,
        "group": stats.st_gid,
        "atime": stats.st_atime,
        "mtime": stats.st_mtime,
        "ctime": stats.st_ctime
    }

def scan_directory():
    state = {}
    for item in Path(MONITORED_DIR).iterdir():
        state[item.name] = get_metadata(item)
    return state

def monitor_directory():
    global previous_state
    current_state = scan_directory()
    timestamp = time.ctime()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        for name in current_state:
            if name not in previous_state:
                writer.writerow([timestamp, "CREATED", name, current_state[name]])

        for name in previous_state:
            if name not in current_state:
                writer.writerow([timestamp, "DELETED", name])

        for name in current_state:
            if name in previous_state and current_state[name] != previous_state[name]:
                writer.writerow([
                    timestamp, "MODIFIED", name,
                    previous_state[name],
                    current_state[name]
                ])

    previous_state = current_state

while True:
    monitor_directory()
    time.sleep(5)
