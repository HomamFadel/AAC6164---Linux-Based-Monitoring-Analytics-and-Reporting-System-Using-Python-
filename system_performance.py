import psutil
import time
from datetime import datetime

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
    for proc in psutil.process_iter(['pid', 'status']):
        if proc.info['status'] == psutil.STATUS_RUNNING:
            running += 1
        elif proc.info['status'] == psutil.STATUS_SLEEPING:
            sleeping += 1
    metrics['running_processes'] = running
    metrics['sleeping_processes'] = sleeping
    
    return metrics

# Collect and print every 10 seconds
print("System Performance and Resource Monitoring (every 10s)\n" + "="*60)
try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        metrics = collect_metrics()
        
        print(f"\n[{timestamp}]")
        print(f"CPU %: {metrics['cpu_percent']:.1f}%")
        print(f"Load Average (1/5/15min): {metrics['load_1min']:.2f}, {metrics['load_5min']:.2f}, {metrics['load_15min']:.2f}")
        print(f"Memory: Used {metrics['memory_used']/1024**3:.1f}GB ({metrics['memory_percent']:.1f}%), Avail {metrics['memory_available']/1024**3:.1f}GB")
        print(f"Disk /: Used {metrics['disk_used']/1024**3:.1f}GB ({metrics['disk_percent']:.1f}%)")
        print(f"Uptime: {metrics['uptime_seconds']/3600:.1f} hours")
        print(f"Idle % (recent): {metrics['system_idle_percent']:.1f}%")
        print(f"Processes: Total {metrics['total_processes']}, Running {metrics['running_processes']}, Sleeping {metrics['sleeping_processes']}")
        
        time.sleep(10)  # Every 10 seconds
except KeyboardInterrupt:
    print("\nMonitoring stopped.")
