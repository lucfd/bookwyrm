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
from rich.prompt import Prompt, Confirm
from rich.theme import Theme

global selected_theme

def load_theme(name=""):

    # Lich theme (cmd friendly colours)
    theme_lich = Theme({
        "big.header": "bold chartreuse1 on black",
        
        "highlight": "bold yellow", # used for prompts and in-text highlighting
        "error": "orange_red1",
        "success": "sea_green2",
        "neutral": "cyan2",

        # menu tables
        "menu.title": "yellow1",
        "table.header": "yellow1",
        "table.border": "green",
        "col1": "bold cyan",
        "col2": "sea_green2",
        "col3": "chartreuse1",


        # spell table
        "spell.table.header": "bold turquoise2",
        "row1": "white on black",
        "row2":"chartreuse1 on grey11", 
    })

    theme_beholder = Theme({
        "big.header": "bold gold1",
        
        "highlight": "bold yellow",
        "error": "orange_red1",
        "success": "sea_green2",
        "neutral": "cyan2",

        # menu tables
        "menu.title": "chartreuse1",
        "table.header": "orchid",
        "table.border": "pale_turquoise1",
        "col1": "bold cyan",
        "col2": "sea_green2",
        "col3": "gold1",


        # spell table
        "spell.table.header": "bold chartreuse1",
        "row1": "hot_pink on black",
        "row2":"cyan on grey11", 
    })

    theme_illithid = Theme({
        "big.header": "bold yellow on purple4",
        
        "highlight": "bold medium_purple1",
        "error": "orange_red1",
        "success": "sea_green2",
        "neutral": "cyan2",

        # menu tables
        "menu.title": "thistle1",
        "table.header": "orchid",
        "table.border": "medium_purple3",
        "col1": "bold cyan",
        "col2": "medium_purple3",
        "col3": "blue3",


        # spell table
        "spell.table.header": "bold magenta",
        "row1": "blue_violet on grey30",
        "row2":"blue_violet on grey42",
    })

    theme_dragon = Theme({
        "big.header": "bold yellow on dark_red",
        
        "highlight": "bold yellow",
        "error": "orange_red1",
        "success": "sea_green2",
        "neutral": "cyan2",

        # menu tables
        "menu.title": "yellow1",
        "table.header": "gold1",
        "table.border": "dark_red",
        "col1": "bold orange_red1",
        "col2": "orange3",
        "col3": "gold1",


        # spell table
        "spell.table.header": "bold gold1 on red3",
        "row1": "gold1 on dark_red",
        "row2":"bold gold1 on dark_orange3",
    })

    if name == "Beholder":
        return theme_beholder
    elif name == "Illithid":
        return theme_illithid
    elif name == "Dragon":
        return theme_dragon
    else:
        return theme_lich # Lich is default theme


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
        
    console = Console(theme=selected_theme)

    if len(spells) == 0:
        console.print(('[error]No spells found. Double-check your search criteria.[/]'))
        return

    spell_table = Table(title="", show_header=True, header_style="spell.table.header", row_styles=["row1", "row2"])
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

    console = Console(theme=selected_theme)
    menu_table = Table(show_header=True, header_style="menu.title", border_style="table.border")
    menu_table.add_column("Option", style="col3", justify="center")
    menu_table.add_column("Description", style="col3", justify="left")

    menu_table.add_row("1", "Display spell info")
    menu_table.add_row("2", "Spell search")
    menu_table.add_row("3", "Check for compendium updates")
    menu_table.add_row("4", "Options")
    menu_table.add_row("q", "Quit")

    console.print(menu_table)

    selected_option = Prompt.ask("[bold yellow]Please select an option[/]", choices=["1", "2", "3", "4", "q"])

    return selected_option


def display_help_menu():
    
    console = Console(theme=selected_theme)
    table = Table(border_style="table.border")

    table.add_column("[table.header]Argument[/]", style="col1")
    table.add_column("[table.header]Description[/]", style="col2")
    table.add_column("[table.header]Example[/]", style="bold")

    table.add_row("-c, --class", 
                "Filters for spells that belong to specified classes.", 
                "[highlight]-c Bard Wizard[/] filters for spells available to both Bards and Wizards.")


    table.add_row("-s, --school", 
                "Filter by spell school.", 
                "[highlight]-s Abjuration[/] filters for Abjuration spells.")

    table.add_row("-l, --level", 
                "Filter by spell level.", 
                "[highlight]-l 3 [/]filters for level 3 spells. [highlight]-l 0..5[/] includes spells from cantrips to level 5.")

    table.add_row("-cmp, --component", 
                "Filter by spell components.", 
                "[highlight]-cmp v s m [/]will filter for spells with all three components.")

    table.add_row("-con, --concentration", 
                "Filter spells with concentration.", 
                "[highlight]-con[/] filters for concentration spells. [highlight]-con false[/] excludes them.")
    
    table.add_row("-r, --ritual", 
                "Filter for spells with the ritual tag.", 
                "[highlight]-r[/] filters for ritual spells. [highlight]-r false[/] excludes them.")

    console.print(table)


def sourcebook_table(sourcebooks, prefs):
    
    console = Console(theme=selected_theme)
    table = Table(border_style="table.border")

    table.add_column("[table.header]Option[/]", style="col1")
    table.add_column("[table.header]Source[/]", style="col2")
    table.add_column("[table.header]Status[/]", style="col3")

    for i, source in enumerate(sourcebooks):

        if source in prefs.disabled_sourcebooks:
            source_status = "DISABLED"
        else:
            source_status = "ENABLED"

        table.add_row(str(i+1), source, f"[{'green' if source_status == 'ENABLED' else 'red'}]{source_status}[/]")

    console.print(table)
    console.print('[highlight]q to quit[/]')


def manage_sources(spells, prefs):

    sourcebooks = helpers.get_sourcebooks(spells)

    while(True):
        sourcebook_table(sourcebooks, prefs)
        user_input = input()

        if user_input.lower() == 'q':
            return
        elif user_input.isnumeric() and int(user_input) <= len(sourcebooks):
            print(sourcebooks[int(user_input)-1])

            if sourcebooks[int(user_input)-1] in prefs.disabled_sourcebooks:
                prefs.disabled_sourcebooks.remove(sourcebooks[int(user_input)-1])
            else:
                prefs.disabled_sourcebooks.append(sourcebooks[int(user_input)-1])


def theme_menu(prefs):
    global selected_theme
    console = Console(theme=selected_theme)
    table = Table(border_style="table.border")

    table.add_column("[table.header]Option[/]", style="col1", justify="center")
    table.add_column("[table.header]Theme[/]", style="col2")
    table.add_column("[table.header]Description[/]", style="col3")

    style_list = []
    style_list.append(("Lich", "Black and green. CMD-friendly!"))
    style_list.append(("Dragon", "Red, orange and gold."))
    style_list.append(("Illithid", "Blue, pink and purple."))
    style_list.append(("Beholder", "Lots of bright neon colours!"))

    for i, style in enumerate(style_list):
        table.add_row(str(i+1), style[0], style[1])

    console.print(table)
    console.print(f"Your current theme is [highlight]{prefs.theme}[/]")

    user_input = Prompt.ask("[bold yellow]Please select an option[/]", choices=[str(num) for num in range(1, i+2)] + ["q"])

    if user_input == 'q':
        return
    else:
        prefs.theme = style_list[int(user_input)-1][0]
        selected_theme = load_theme(prefs.theme)


def option_table(spells, prefs):
    console = Console(theme=selected_theme)
    table = Table(border_style="table.border")

    table.add_column("[table.header]Option[/]", style="col1")
    table.add_column("[table.header]Description[/]", style="col2")
    table.add_column("[table.header]Status[/]", style="bold")

    if prefs.unearthed_arcana:
        ua_status = 'ENABLED'
    else:
        ua_status = 'DISABLED'
 
    table.add_row("Unearthed Arcana", 
                "Include official WOTC playtest material.", 
                f"[{'green' if prefs.unearthed_arcana else 'red'}]{ua_status}[/]")

    if prefs.optional_spells:
        optional_status = 'ENABLED'
    else:
        optional_status = 'DISABLED'  

    table.add_row("Optional spells", 
                "Include TCoE's expanded spell lists in search results.", 
                    f"[{'green' if prefs.optional_spells else 'red'}]{optional_status}[/]")
    
    num_sourcebooks = len(helpers.get_sourcebooks(spells))
    num_disabled_sourcebooks = len(prefs.disabled_sourcebooks)

    table.add_row("Manage sourcebooks", 
                "Choose which sources are included in search results.", 
                f"[bold yellow]{str(num_sourcebooks-num_disabled_sourcebooks)}/{str(num_sourcebooks)}[/]")
    
    table.add_row("Modify theme", 
                "Change the colours of the user interface.", 
                "")

    table.add_row("Delete library", 
                "Delete local files, resetting your library.", 
                "")
    
    console.print(table)


def display_options_menu(spells, prefs):
    
    while(True):

        option_table(spells, prefs)
        selected_option = Prompt.ask("[bold yellow]Please select an option[/]", choices=["1", "2", "3", "4", "q"])

        if selected_option == '1': # toggle UA
            prefs.unearthed_arcana = not prefs.unearthed_arcana

        elif selected_option == '2': # toggle optional spells
            prefs.optional_spells = not prefs.optional_spells

        elif selected_option == '3': 
            manage_sources(spells, prefs)

        elif selected_option == '4': 
            theme_menu(prefs)

        elif selected_option == '5': 
            confirm_deletion = Confirm.ask("[bold dark_orange3]Are you sure? This cannot be undone.[/]")
            if confirm_deletion:
                sm.delete_library()

        elif selected_option == 'q':
            helpers.save_preferences(prefs)
            return


def update_library(): # add missing spells to spells.txt, then returns re-initialized list of spells
    console = Console(theme=selected_theme)
    console.print("[neutral]Searching for new spells...[/]")

    try:
        old_spells, new_spells = sm.find_new_spells(return_old=True)
    except FileNotFoundError:
        console.print("[error]Failed to read spells.txt[/]")
        return None
    except Exception:
        console.print("[error]Failed to check for updates.[/]")
        return None
    
    if not new_spells:
        console.print("[neutral]No new spells found.[/]")
    else:
        console.print(f"[neutral]Found the following new spells: [/]\n[sky_blue1]"+", ".join(new_spells)+"[/]")
        update_input = Prompt.ask("[bold yellow]Would you like to update your library?[/] [bold magenta][Y/N][/]")

        if update_input.lower() in ['y', 'yes']:
            try:
                sm.save_spell_names(old_spells+new_spells)
                updated_spells = sm.initialize_spells()
                console.print('[success]Spell library updated successfully.[/]')
                return updated_spells
            except:
                console.print('[error]Failed to download new spells.[/]')
        else:
            console.print('[neutral]Spell library will not be updated.[/]')

    return None


def main():

    global selected_theme
    prefs =  helpers.initialize_preferences()
    selected_theme = load_theme(prefs.theme)
    console = Console(theme=selected_theme)

    ascii_header = """
    BBBBB   OOOOO   OOOOO  K   K   W   W   Y   Y  RRRRR   M   M
    B   B  O     O O     O K  K    W W W    Y Y   R    R  MM MM
    BBBBB  O     O O     O KKK     WW WW     Y    RRRRR   M M M
    B   B  O     O O     O K  K    W W W     Y    R   R   M   M
    BBBBB   OOOOO   OOOOO  K   K   W   W     Y    R    R  M   M
    """

    console.print(Panel(ascii_header, style="big.header", box=box.ROUNDED))


    spells = sm.initialize_spells()

    if(spells == None):
        console.print("[error]Failed to initialize spells. Aborting program.[/]")
        return

    # save spells to json if there is no backup
    file_path = Path('spells.json')
    if not file_path.is_file():
        sm.save_spells(helpers.jsonify_list(spells))
        console.print("[success]spells.json successfully created.[/]")

    # main control loop
    while(True): 
         
        user_input = display_menu()
        # display spell information
        if user_input == '1':
            target_spell = Prompt.ask("[bold yellow]Enter spell name[/]")
            try:
                display_spell(search.fetch_spell(spells, target_spell))
            except:
                console.print("[error]Couldn\'t find that spell.[/]")
        # spell search
        elif user_input == '2':
            display_help_menu()
            args = search.parse_query(Prompt.ask("[bold yellow]Enter your search query[/]"))
            filtered_spells = search.filter_spells(spells, args, options=prefs)
            display_spell_table(filtered_spells)
        # check for updates
        elif user_input == '3':
            new_spells = update_library()
            
            if new_spells:
                spells = new_spells
        # options menu
        elif user_input == '4':
            display_options_menu(spells, prefs)
           # console = Console(theme=selected_theme)
            
        # terminate program
        elif user_input == 'q':
            console.print("[success]Exiting program.[/]")
            return


if __name__ == "__main__":
    main()