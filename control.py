import requests
from bs4 import BeautifulSoup
import helpers
import cacher
import search
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich import box

def display_spell(spell):
    spell.output()


def main(): # CLI parsing logic goes here, make new file for filtering. rename control.py to main.py

    console = Console()

    ascii_header = """
    BBBBB   OOOOO   OOOOO  K   K   W   W   Y   Y  RRRRR   M   M
    B   B  O     O O     O K  K    W W W    Y Y   R    R  MM MM
    BBBBB  O     O O     O KKK     WW WW     Y    RRRRR   M M M
    B   B  O     O O     O K  K    W W W     Y    R   R   M   M
    BBBBB   OOOOO   OOOOO  K   K   W   W     Y    R    R  M   M
    """

    console.print(Panel(ascii_header, style="bold yellow on purple4", box=box.ROUNDED))


    spells = cacher.initialize_spells()

    if(spells == None):
        print("Aborting program.")
        return

    user_input = input("Enter field name: ")
    user_input2 = input("Enter target: ")

    filtered_spells = search.filter_spells(spells, user_input, user_input2)

    [print(spell.name) for spell in filtered_spells]

if __name__ == "__main__":
    main()