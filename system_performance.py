import psutil
import time
from datetime import datetime
import csv
import os

def collect_metrics():
    metrics = {}
    
    # I. CPU Metrics percent (system-wide)
    metrics['cpu_percent'] = psutil.cpu_percent(interval=1)  # Current CPU %
    
    # CPU load average (1min, 5min, 15min)
    try:
        load_avg = psutil.getloadavg()
        metrics['load_1min'] = load_avg[0]
        metrics['load_5min'] = load_avg[1]
        metrics['load_15min'] = load_avg[2]
    except:
        metrics['load_avg'] = 'N/A (non-Linux)'
    
    # II. Memory number of running processes
    memory = psutil.virtual_memory()
    metrics['memory_total'] = memory.total
    metrics['memory_used'] = memory.used
    metrics['memory_available'] = memory.available
    metrics['memory_percent'] = memory.percent  # Memory usage percent
    
    # III. Disk metrics percent (root partition)
    root_usage = psutil.disk_usage('/')
    metrics['disk_total'] = root_usage.total
    metrics['disk_used'] = root_usage.used
    metrics['disk_free'] = root_usage.free
    metrics['disk_percent'] = root_usage.percent  # Root disk %
    
    # IV. System Uptime
    uptime_seconds = time.time() - psutil.boot_time()  # System uptime
    metrics['uptime_seconds'] = uptime_seconds
    
    # System idle time (from cpu_times_percent)
    cpu_times_p = psutil.cpu_times_percent(interval=1)
    metrics['system_idle_percent'] = cpu_times_p.idle  # Recent idle %
    
    # V. Active Processes (total)
    metrics['total_processes'] = len(psutil.pids())  # Total processes
    
    # Number running vs sleeping processes
    running = 0
    sleeping = 0
    # List to store process info for Top 3 analysis
    process_list = []
    
    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info']):
        try:
            # Count running vs sleeping
            if proc.info['status'] == psutil.STATUS_RUNNING:
                running += 1
            elif proc.info['status'] == psutil.STATUS_SLEEPING:
                sleeping += 1
            
            # Store info for Top 3 Sorting
            process_list.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
            continue

    metrics['running_processes'] = running
    metrics['sleeping_processes'] = sleeping

    # Top 3 Processes by CPU and Memory
    metrics['top_3_cpu'] = sorted(process_list, key=lambda x: x['cpu_percent'], reverse=True)[:3]
    metrics['top_3_mem'] = sorted(process_list, key=lambda x: x['memory_info'].rss, reverse=True)[:3]
    
    return metrics

os.makedirs("logs", exist_ok=True) # create logs folder

csv_file = "logs/system_metrics.csv"  # store inside logs folder

# add headers in csv file
headers = [
    "Timestamp",
    "CPU_Percent",
    "Memory_Used(GB)", "Memory_Available(GB)", "Memory_Percent",
    "Disk_Used(GB)", "Disk_Free(GB)", "Disk_Percent", "Top_3_CPU_Processes", "Top_3_Memory_Processes"
]

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)


# Collect and print every 10 seconds
def start_system_monitoring():
    print("System Performance and Resource Monitoring (every 10s)\n" + "="*60)
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            metrics = collect_metrics()

            print(f"\n[{timestamp}]")
            print(f"CPU %: {metrics['cpu_percent']:.1f}%")
            print(f"Memory Used: {metrics['memory_percent']:.1f}%")
            print(f"Disk Used: {metrics['disk_percent']:.1f}%")
            print(f"System Uptime: {metrics['uptime_seconds']:.0f}s")

            # Formatted the Top 3 data into strings for the CSV
            top_cpu_str = ", ".join([f"{p['name']}({p['cpu_percent']}%)" for p in metrics['top_3_cpu']])
            top_mem_str = ", ".join([f"{p['name']}({p.get('memory_info').rss/1024**2:.1f}MB)" for p in metrics['top_3_mem']])

            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    timestamp,
                    metrics['cpu_percent'],
                    metrics['memory_used']/1024**3,
                    metrics['memory_available']/1024**3,
                    metrics['memory_percent'],
                    metrics['disk_used']/1024**3,
                    metrics['disk_free']/1024**3,
                    metrics['disk_percent'],
                    top_cpu_str,
                    top_mem_str
                ])

            time.sleep(10)

    except KeyboardInterrupt:
        print("\nSystem monitoring stopped.")

if __name__ == "__main__":
    start_system_monitoring()

