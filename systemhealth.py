import psutil
import logging

# Configure logging
logging.basicConfig(filename='system_health.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Thresholds
CPU_USAGE_THRESHOLD = 80  # in percentage
MEMORY_USAGE_THRESHOLD = 80  # in percentage
DISK_USAGE_THRESHOLD = 90  # in percentage

def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_USAGE_THRESHOLD:
        alert(f"High CPU usage detected: {cpu_usage}%")
    return cpu_usage

def check_memory_usage():
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    if memory_usage > MEMORY_USAGE_THRESHOLD:
        alert(f"High memory usage detected: {memory_usage}%")
    return memory_usage

def check_disk_usage():
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    if disk_usage > DISK_USAGE_THRESHOLD:
        alert(f"High disk usage detected: {disk_usage}%")
    return disk_usage

def check_running_processes():
    process_count = len(psutil.pids())
    # No predefined threshold for process count in this example
    # Customize as needed
    return process_count

def alert(message):
    print(message)
    logging.info(message)

def main():
    cpu_usage = check_cpu_usage()
    memory_usage = check_memory_usage()
    disk_usage = check_disk_usage()
    process_count = check_running_processes()

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")
    print(f"Disk Usage: {disk_usage}%")
    print(f"Running Processes: {process_count}")

if __name__ == "__main__":
    main()
