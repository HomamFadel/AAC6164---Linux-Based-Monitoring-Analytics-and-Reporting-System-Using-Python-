import pandas as pd
import matplotlib.pyplot as plt
import os

# Paths based on Student A and B's output
DIR_LOGS = "logs/directory_logs.csv"
SYS_LOGS = "logs/system_metrics.csv"
REPORT_FILE = "final_summary_report.txt"

def analyze_directory_data():
    """Analyzes file system events from Student A's logs."""
    if not os.path.exists(DIR_LOGS):
        return {"total": 0, "breakdown": {}, "top_file": "None"}
    try:
        # on_bad_lines='skip' handles the tokenizing error from extra commas
        df = pd.read_csv(DIR_LOGS, names=["Timestamp", "Event", "Filename", "Details"], 
                        header=None, on_bad_lines='skip', engine='python')
        
        total_events = len(df)
        event_counts = df['Event'].value_counts().to_dict() if not df.empty else {}
        most_active_file = df['Filename'].mode()[0] if not df.empty else "N/A"
        
        return {"total": total_events, "breakdown": event_counts, "top_file": most_active_file}
    except Exception:
        return {"total": 0, "breakdown": {}, "top_file": "Error"}

def analyze_system_performance():
    """Analyzes CPU/RAM from Student B's metrics and generates histograms."""
    if not os.path.exists(SYS_LOGS):
        return {"avg_cpu": 0, "avg_mem": 0, "peak_cpu": 0}
    try:
        df = pd.read_csv(SYS_LOGS)
        
        stats = {
            "avg_cpu": df['CPU_Percent'].mean(),
            "avg_mem": df['Memory_Percent'].mean(),
            "peak_cpu": df['CPU_Percent'].max()
        }

        # --- STUDENT C VISUALIZATION: HISTOGRAMS ---
        plt.figure(figsize=(12, 6))
        
        # Subplot 1: CPU Distribution
        plt.subplot(1, 2, 1)
        plt.hist(df['CPU_Percent'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
        plt.axvline(stats['avg_cpu'], color='red', linestyle='dashed', linewidth=2, label=f"Avg: {stats['avg_cpu']:.1f}%")
        plt.title('CPU Usage Frequency')
        plt.xlabel('CPU Usage (%)')
        plt.ylabel('Frequency')
        plt.legend()

        # Subplot 2: Memory Distribution
        plt.subplot(1, 2, 2)
        plt.hist(df['Memory_Percent'], bins=15, color='salmon', edgecolor='black', alpha=0.7)
        plt.axvline(stats['avg_mem'], color='blue', linestyle='dashed', linewidth=2, label=f"Avg: {stats['avg_mem']:.1f}%")
        plt.title('Memory Usage Frequency')
        plt.xlabel('Memory Usage (%)')
        plt.ylabel('Frequency')
        plt.legend()

        plt.tight_layout()
        plt.savefig('performance_histogram.png')
        plt.close()
        
        return stats
    except Exception as e:
        print(f"Visualization Error: {e}")
        return {"avg_cpu": 0, "avg_mem": 0, "peak_cpu": 0}

def generate_report(dir_stats, sys_stats):
    """Writes the final analysis to a text file."""
    with open(REPORT_FILE, "w") as f:
        f.write("="*50 + "\n")
        f.write("      LINUX MONITORING FINAL REPORT (STUDENT C)\n")
        f.write("="*50 + "\n\n")
        
        f.write("[SECTION 1: DIRECTORY ACTIVITY]\n")
        f.write(f"- Total File Events: {dir_stats['total']}\n")
        for event, count in dir_stats['breakdown'].items():
            f.write(f"  * {event}: {count}\n")
        f.write(f"- Most Active File: {dir_stats['top_file']}\n\n")
        
        f.write("[SECTION 2: SYSTEM PERFORMANCE]\n")
        f.write(f"- Average CPU Usage: {sys_stats['avg_cpu']:.2f}%\n")
        f.write(f"- Average RAM Usage: {sys_stats['avg_mem']:.2f}%\n")
        f.write(f"- Highest CPU Peak: {sys_stats['peak_cpu']:.2f}%\n\n")
        
        f.write("[SECTION 3: VISUALIZATION]\n")
        f.write("- Histogram Chart Saved: performance_histogram.png\n")
        f.write("\nAnalysis Complete.")
