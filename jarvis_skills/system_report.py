# Skill: system_report
# Description: Print a quick system status report
import psutil, datetime
cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()
disk = psutil.disk_usage("/")
print(f"System Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"CPU: {cpu}%  RAM: {ram.percent}%  Disk: {disk.percent}%")
print(f"RAM used: {ram.used//1024**3}GB / {ram.total//1024**3}GB")
