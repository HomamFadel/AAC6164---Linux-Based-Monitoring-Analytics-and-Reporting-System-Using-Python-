import threading
from monitoring_dir import start_directory_monitoring
from system_performance import start_system_monitoring

print("Linux Monitoring System Started")
print("=" * 40)

directory_thread = threading.Thread(target=start_directory_monitoring)
system_thread = threading.Thread(target=start_system_monitoring)

directory_thread.start()
system_thread.start()

directory_thread.join()
system_thread.join()
