from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich import box

# False = dashboard, True = face
state = False # default to dash on boot
console = Console()

def switch_state():
    global state
    if state == False:
        state = True
        console.clear()
        set_face_screen()
        return
    else:
        state = False
        console.clear()
        set_dash_screen()
        return

def set_dash_screen():
    # place holders
    TIME_STR = "03:21 PM"
    DATE_STR = "Wed • Jan 07"

    WEATHER_NOW = "72°F"
    WEATHER_HI = "78°F"
    WEATHER_LO = "61°F"
    WEATHER_COND = "Partly cloudy"

    CPU_TEMP = "121.3°F"
    CPU_USAGE = "17.2%"
    UPTIME = "384 min"
    RAM_USED = "2.31 / 7.74 GB"
    RAM_FREE = "5.43 GB"
    RAM_PCT = "29.8%"

    VERSE_STR = 'Psalm 23:1 "The Lord is my shepherd; I shall not want."'


    # Layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="top", size=10),
        Layout(name="verse", size=6),
    )

    layout["top"].split_row(
        Layout(name="weather"),
        Layout(name="system"),
    )

    # Header
    header_grid = Table.grid(expand=True)
    header_grid.add_column(justify="left")
    header_grid.add_column(justify="right")

    title = Text("PICO", style="bold cyan")
    clock = Text(f"{DATE_STR}   {TIME_STR}", style="bold")

    header_grid.add_row(title, clock)

    layout["header"].update(
        Panel(
            header_grid,
            padding=(0, 1),
            box=box.ROUNDED,
            border_style="cyan",
        )
    )

    # Weather
    w = Table.grid(expand=True)
    w.add_column(justify="left")
    w.add_column(justify="right")

    w.add_row("Now", WEATHER_NOW)
    w.add_row("High", WEATHER_HI)
    w.add_row("Low", WEATHER_LO)
    w.add_row("Condition", WEATHER_COND)

    layout["weather"].update(
        Panel(
            w,
            title="Weather",
            padding=(0, 1),
            box=box.ROUNDED,
            border_style="blue",
        )
    )

    # System
    s = Table.grid(expand=True)
    s.add_column(justify="left")
    s.add_column(justify="right")

    s.add_row("CPU Temp", CPU_TEMP)
    s.add_row("CPU Usage", CPU_USAGE)
    s.add_row("Uptime", UPTIME)
    s.add_row("RAM Used", RAM_USED)
    s.add_row("RAM Free", RAM_FREE)
    s.add_row("RAM %", RAM_PCT)

    layout["system"].update(
        Panel(
            s,
            title="System",
            padding=(0, 1),
            box=box.ROUNDED,
            border_style="magenta",
        )
    )

    # Verse
    verse_text = Text(VERSE_STR)
    verse_text.justify = "left"

    layout["verse"].update(
        Panel(
            verse_text,
            title="Daily Verse (KJV)",
            padding=(0, 1),
            box=box.ROUNDED,
            border_style="green",
        )
    )

    console.print(layout)

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