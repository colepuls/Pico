from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich import box
import threading, time
from skills.bibleverse import get_random_verse
from skills.get_current_time import get_time_skill, get_date_skill
from skills.weather import get_condition, get_current, get_high, get_low
from skills.system_report import get_cpu_temp, get_cpu_usage, get_ram_info
import thread_share

# False = dashboard, True = face
state = False # default to dash on boot
console = Console()

def switch_state():
    global state
    if state == False:
        state = True
        thread_share.dash_stop.set()
        console.clear()
        set_face_screen()
        return
    else:
        state = False
        console.clear()
        #set_dash_screen()
        thread_share.dash_stop.clear()
        thread_share.shared_dash = threading.Thread(target=set_dash_screen, daemon=True)
        thread_share.shared_dash.start()
        return
    

def update_data(data, get_data_func, interval):
    while True:
        data["value"] = get_data_func()
        time.sleep(interval)

def set_dash_screen():
    init_current_time = {}
    #update_data(init_current_time, get_time_skill, 5)
    thread_time = threading.Thread(target=update_data, args=(init_current_time, get_time_skill, 5), daemon=True)
    thread_time.start()

    while state is False and not thread_share.dash_stop.is_set():
        current_time = init_current_time["value"]
        table = Table()
        table.add_column("Time", style="cyan")
        table.add_row(current_time, style="green")
        console.print(table)
        if thread_share.dash_stop.wait(20):
            break
        console.clear()
    
    return


def set_face_screen():
    table = Table(title="Face")
    table.add_column("Component", style="red")
    table.add_column("Value", style="yellow")
    table.add_column("Component", style="red")
    table.add_column("Value", style="yellow")
    table.add_row("CPU", "45%")
    table.add_row("RAM", "3.2 GB")
    table.add_row("Temp", "62°C") 
    table.add_row("CPU", "45%")
    table.add_row("RAM", "3.2 GB")
    table.add_row("Temp", "62°C")
    table.add_row("CPU", "45%")
    table.add_row("RAM", "3.2 GB")
    table.add_row("Temp", "62°C")
    table.add_row("RAM", "3.2 GB")
    table.add_row("RAM", "3.2 GB")
    console.print(table)