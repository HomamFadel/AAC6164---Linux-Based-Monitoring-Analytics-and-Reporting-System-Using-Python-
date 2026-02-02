import threading
import time
import sys
import os

from monitoring_dir import start_directory_monitoring
from system_performance import start_system_monitoring

# Visualization is OPTIONAL
try:
    import visualization
except ImportError:
    visualization = None


def main():
    print("=" * 50)
    print("LINUX MONITORING SYSTEM - GROUP PROJECT")
    print("System Status: RUNNING")
    print("Press Ctrl+C to stop and generate report")
    print("=" * 50)

    os.makedirs("logs", exist_ok=True)
    os.makedirs("watched_folder", exist_ok=True)

    t1 = threading.Thread(target=start_directory_monitoring, daemon=True)
    t2 = threading.Thread(target=start_system_monitoring, daemon=True)

    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[STOP SIGNAL] Processing analytics for Student C...")

        if visualization:
            try:
                dir_stats = visualization.analyze_directory_data()
                sys_stats = visualization.analyze_system_performance()
                visualization.generate_report(dir_stats, sys_stats)
                print("Report created successfully.")
            except Exception as e:
                print(f"Analysis failed: {e}")
        else:
            print("Visualization module missing — skipping Student C stage.")

        print("System Shutdown Complete.")
        sys.exit(0)


if __name__ == "__main__":
    main()
