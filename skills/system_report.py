from gpiozero import CPUTemperature
import psutil
import time
import os

os.chdir("/home/colecodes/projects/Pico/motor_files") # make auto .lgd files stored in specific folder

def get_cpu_temp():
    cpu = CPUTemperature()
    return f"CPU Temperature: {((cpu.temperature * 9/5) + 32):.2f}°F"

def get_cpu_usage():
    return f"CPU Usage: {(psutil.cpu_percent(interval=1)):.2f}%"

def get_uptime():
    return f"Uptime: {((time.time() - psutil.boot_time()) / 60):.0f} min"

def get_ram_info():
    vm = psutil.virtual_memory()

    total_mb = vm.total / (1024 ** 3)
    used_mb = vm.used / (1024 ** 3)
    available_mb = vm.available / (1024 ** 3)
    percent = vm.percent

    return f"RAM: {used_mb:.2f} GB / {total_mb:.2f} GB used\n     {available_mb:.2f} GB available\n     {percent:.1f}% used"

def get_system_report():
    return f"{get_cpu_temp()}\n\n{get_cpu_usage()}\n\n{get_uptime()}\n\n{get_ram_info()}"

# print(get_system_report())
