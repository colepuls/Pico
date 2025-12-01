from gpiozero import CPUTemperature
import psutil
import time

def get_cpu_temp():
    cpu = CPUTemperature()
    return f"CPU Temperature: {((cpu.temperature * 9/5) + 32):.2f} °F"

def get_cpu_usage():
    return f"CPU Usage: {(psutil.cpu_percent(interval=1)):.2f}"

def get_uptime():
    return f"Uptime: {((time.time() - psutil.boot_time()) / 60):.0f} minutes"

if __name__ == '__main__':
    cpu_temp = get_cpu_temp()
    print(cpu_temp)

    cpu_usage = get_cpu_usage()
    print(cpu_usage)

    uptime = get_uptime()
    print(uptime)

