
"""
Terminal UI:
- Face -> Dashboard toggle ("Pico, change screen")
- Face:
    * Basic eyes that idle blink animation
    * Pico awake -> Eyes open, idling blink
    * Pico asleep -> Eyes closed
    * Mouth with movement while speaking
- Dashboard:
    * Date and time
    * System usage
    * Weather
    * Daily Bible verse
"""
import time
from rich import print
from rich.console import Console
from rich.table import Table


# State 1 ex
console2 = Console()
table2 = Table()
table2.add_column("Component", style="red")
table2.add_column("Value", style="yellow")
table2.add_column("Component", style="red")
table2.add_column("Value", style="yellow")
table2.add_row("CPU", "45%")
table2.add_row("RAM", "3.2 GB")
table2.add_row("Temp", "62°C")
table2.add_row("CPU", "45%")
table2.add_row("RAM", "3.2 GB")
table2.add_row("Temp", "62°C")
table2.add_row("CPU", "45%")
table2.add_row("RAM", "3.2 GB")
table2.add_row("Temp", "62°C")
table2.add_row("RAM", "3.2 GB")
table2.add_row("Temp", "62°C")
console2.print(table2)

# Switch state ex
time.sleep(5)
console2.clear(table2)

# State 2
console = Console()
table = Table()
table.add_column("Component", style="green")
table.add_column("Value", style="cyan")
table.add_column("Component", style="green")
table.add_column("Value", style="cyan")
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
table.add_row("Temp", "62°C")
console.print(table)

time.sleep(5)
