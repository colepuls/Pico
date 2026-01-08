from pathlib import Path
import psutil
import time
import os

os.chdir("/home/colecodes/projects/Pico/motor_files") # make auto .lgd files stored in specific folder

def get_cpu_temp():
    temp_milli = int(Path("/sys/class/thermal/thermal_zone0/temp").read_text().strip())
    temp_c = temp_milli / 1000
    temp_f = (temp_c * 9/5) + 32
    return f"{temp_f:.2f}"

def get_cpu_usage():
    return f"{(psutil.cpu_percent(interval=0.1)):.2f}"

def get_uptime():
    return f"Uptime: {((time.time() - psutil.boot_time()) / 60):.0f} min"

def get_ram_info():
    vm = psutil.virtual_memory()

    total_mb = vm.total / (1024 ** 3)
    used_mb = vm.used / (1024 ** 3)
    available_mb = vm.available / (1024 ** 3)
    percent = vm.percent

    return f"{used_mb:.2f}"

def get_system_report():
    return f"{get_cpu_temp()}\n\n{get_cpu_usage()}\n\n{get_uptime()}\n\n{get_ram_info()}"

if __name__ == '__main__':
    print(get_system_report())


