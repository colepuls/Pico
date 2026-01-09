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
    init_time = {"value": None}
    thread_time = threading.Thread(target=update_data, args=(init_time, get_time_skill, 5), daemon=True)
    thread_time.start()

    init_current_temp = {"value": None}
    thread_current_temp = threading.Thread(target=update_data, args=(init_current_temp, get_current, 1800), daemon=True)
    thread_current_temp.start()

    init_cpu_temp = {"value": None}
    thread_cpu_temp = threading.Thread(target=update_data, args=(init_cpu_temp, get_cpu_temp, 300), daemon=True)
    thread_cpu_temp.start()

    while state is False and not thread_share.dash_stop.is_set():
        current_time = init_time["value"]
        current_temp = str(init_current_temp["value"])
        current_cpu_temp = init_cpu_temp["value"]
        table = Table(title="Dashboard")
        table.add_column("Skill", style="cyan")
        table.add_row("Time", current_time)
        table.add_row("Weather", current_temp)
        table.add_row("CPU Temp", current_cpu_temp)
        console.print(table)
        if thread_share.dash_stop.wait(10):
            break
        console.clear()
    
    return


def set_face_screen():
    face = """
                 ________________
                |                |
                |      o  o      |
                |                |
                |       ^^       |
                |                |
                |     ________   |
                |    |        |  |
                |    |_____^__|  |
                |                |
                 ----------------
    """

    console.print(face, style="green")