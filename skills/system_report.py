from pathlib import Path
import psutil


def get_cpu_temp():
    temp_milli = int(Path("/sys/class/thermal/thermal_zone0/temp").read_text().strip())
    temp_c = temp_milli / 1000
    temp_f = (temp_c * 9/5) + 32
    return f"CPU temp is {temp_f:.1f} degrees"


def get_cpu_usage():
    return f"CPU usage {(psutil.cpu_percent(interval=0.1)):.1f} percent"


def get_ram_info():
    vm = psutil.virtual_memory()
    used_mb = vm.used / (1024 ** 3)
    return f"{used_mb:.2f} GB of RAM used"


def run_system_report():
    return f"{get_ram_info()}\n{get_cpu_temp()}\n{get_cpu_usage()}"


