import requests
from bs4 import BeautifulSoup
from src import helpers
from src import spell_manager as sm
from src import search
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

def display_spell(spell):
        console = Console()
        spell_info = Text()
        
        spell_info.append(f"School: ", style="bold cyan")
        spell_info.append(f"{spell.school}\n", style="cyan")

        spell_info.append(f"Level: ", style="bold yellow")
        spell_info.append(f"{spell.level}\n", style="yellow")

        spell_info.append(f"Duration: ", style="bold green")
        spell_info.append(f"{spell.duration}\n", style="green")

        spell_info.append(f"Cast Time: ", style="bold magenta")
        spell_info.append(f"{spell.cast_time}", style="magenta")
        
        if spell.is_ritual():
            spell_info.append(f" (ritual)", style="italic magenta")
        spell_info.append("\n")

        spell_info.append(f"Range: ", style="bold blue")
        spell_info.append(f"{spell.cast_range}\n", style="blue")

        spell_info.append(f"Components: ", style="bold red")
        for spell_component in spell.components:
            spell_info.append(f"{spell_component}", style="red")
        spell_info.append(f"\n", style="red")

        spell_info.append(f"Source: ", style="bold white")
        spell_info.append(f"{spell.source}\n\n", style="white")

        spell_info.append(f"Description:\n", style="bold orange1 underline")
        spell_info.append(f"{spell.description}\n\n", style="white")

        spell_info.append(f"Upcast:\n", style="bold orange1 underline")
        spell_info.append(f"{spell.upcast}\n\n", style="white")

        spell_info.append(f"Spell Lists:\n", style="bold orange1 underline")
        try:
            for index, class_name in enumerate(spell.spell_lists):
                spell_info.append(f"{class_name}", style="white")
                if index != len(spell.spell_lists) - 1:
                    spell_info.append(f", ")
        except:
                spell_info.append(f"{spell.spell_lists}\n", style="white")

        console.print(Panel(spell_info, title=f"[bold magenta]{spell.name}[/bold magenta]", border_style="magenta"))


def display_spell_table(spells):
        
    console = Console()

    if len(spells) == 0:
        console.print(('[orange_red1]No spells found. Double-check your search criteria.[/]'))
        return

    spell_table = Table(title="", show_header=True, header_style="bold magenta", row_styles=["blue_violet on grey30","blue_violet on grey42"])
    spell_table.add_column("Name", style="cyan", justify="center")
    spell_table.add_column("School", style="green", justify="center")
    spell_table.add_column("Level", style="cyan", justify="center")
    spell_table.add_column("Range", style="green", justify="center")
    spell_table.add_column("Duration", style="orchid", justify="center")
    spell_table.add_column("Components", style="green", justify="center")

    for spell in spells:
        spell_table.add_row(spell.name, spell.school, spell.level.split('-')[0], spell.cast_range, spell.duration, ", ".join(spell.components).split('(')[0])

    console.print(spell_table)

def display_menu():

    console = Console()
    menu_table = Table(show_header=True, header_style="bold magenta")
    menu_table.add_column("Option", style="gold1", justify="center")
    menu_table.add_column("Description", style="gold1", justify="left")

    menu_table.add_row("1", "Display spell info")
    menu_table.add_row("2", "Spell search")
    menu_table.add_row("3", "Check for compendium updates")
    menu_table.add_row("4", "Options")
    menu_table.add_row("5", "Quit")

    console.print(menu_table)

    selected_option = Prompt.ask("[bold yellow]Please select an option[/]", choices=["1", "2", "3", "4", "5"])

    return selected_option


def display_help_menu():
    
    console = Console()
    table = Table(border_style="green")

    table.add_column("[orchid]Argument[/]", style="bold cyan")
    table.add_column("[orchid]Description[/]", style="sea_green2")
    table.add_column("[orchid]Example[/]", style="bold")

    table.add_row("-c, --class", 
                "Filters for spells that belong to specified classes.", 
                "[bold yellow]-c Bard Wizard[/] filters for spells available to both Bards and Wizards.")


    table.add_row("-s, --school", 
                "Filter by spell school.", 
                "[bold yellow]-s Abjuration[/] filters for Abjuration spells.")

    table.add_row("-l, --level", 
                "Filter by spell level.", 
                "[bold yellow]-l 3 [/]filters for level 3 spells. [bold yellow]-l 0..5[/] includes spells from cantrips to level 5.")

    table.add_row("-cmp, --component", 
                "Filter by spell components.", 
                "[bold yellow]-cmp v s m [/]will filter for spells with all three components.")

    table.add_row("-con, --concentration", 
                "Filter spells with concentration.", 
                "[bold yellow]-con[/] filters for concentration spells. [bold yellow]-con false[/] excludes them.")
    
    table.add_row("-r, --ritual", 
                "Filter for spells with the ritual tag.", 
                "[bold yellow]-r[/] filters for ritual spells. [bold yellow]-r false[/] excludes them.")

    console.print(table)


def display_options_menu(): #TODO
    
    console = Console()
    console.print("[cyan2]STUB: Options menu[/]")


def update_library(): # add missing spells to spells.txt, then returns re-initialized list of spells
    console = Console()
    console.print("[cyan2]Searching for new spells...[/]")

    try:
        old_spells, new_spells = sm.find_new_spells(return_old=True)
    except FileNotFoundError:
        console.print("[cyan2]Failed to read spells.txt[/]")
        return None
    except Exception:
        console.print("[cyan2]Failed to check for updates.[/]")
        return None
    
    if not new_spells:
        console.print("[cyan2]No new spells found.[/]")
    else:
        console.print(f"[cyan2]Found the following new spells: [/]\n[sky_blue1]"+", ".join(new_spells)+"[/]")
        update_input = Prompt.ask("[bold yellow]Would you like to update your library?[/] [bold magenta][Y/N][/]")

        if update_input.lower() in ['y', 'yes']:
            try:
                sm.save_spell_names(old_spells+new_spells)
                updated_spells = sm.initialize_spells()
                console.print('[sea_green2]Spell library updated successfully.[/]')
                return updated_spells
            except:
                console.print('[orange_red1]Failed to download new spells.[/]')
        else:
            console.print('[cyan2]Spell library will not be updated.[/]')

    return None


def main():

    console = Console()

    ascii_header = """
    BBBBB   OOOOO   OOOOO  K   K   W   W   Y   Y  RRRRR   M   M
    B   B  O     O O     O K  K    W W W    Y Y   R    R  MM MM
    BBBBB  O     O O     O KKK     WW WW     Y    RRRRR   M M M
    B   B  O     O O     O K  K    W W W     Y    R   R   M   M
    BBBBB   OOOOO   OOOOO  K   K   W   W     Y    R    R  M   M
    """

    console.print(Panel(ascii_header, style="bold yellow on purple4", box=box.ROUNDED))


    spells = sm.initialize_spells()

    if(spells == None):
        console.print("[orange_red1] Failed to initialize spells. Aborting program.[/]")
        return

    # save spells to json if there is no backup
    file_path = Path('spells.json')
    if not file_path.is_file():
        sm.save_spells(helpers.jsonify_list(spells))
        console.print("[bold chartreuse1]spells.json successfully created.[/]")

    # main control loop
    while(True): 
         
        user_input = display_menu()
        # display spell information
        if user_input == '1':
            target_spell = Prompt.ask("[bold yellow]Enter spell name[/]")
            try:
                display_spell(search.fetch_spell(spells, target_spell))
            except:
                console.print("[orange_red1]Couldn\'t find that spell.[/]")
        # spell search
        elif user_input == '2':
            display_help_menu()
            args = search.parse_query(Prompt.ask("[bold yellow]Enter your search query[/]"))
            filtered_spells = search.filter_spells(spells, args)
            display_spell_table(filtered_spells)
        # check for updates
        elif user_input == '3':
            new_spells = update_library()
            
            if new_spells:
                spells = new_spells
        # options menu
        elif user_input == '4':
            display_options_menu()
        # terminate program
        elif user_input == '5':
            console.print("[orange_red1]Exiting program.[/]")
            return


if __name__ == "__main__":
    main()