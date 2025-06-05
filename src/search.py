from src.spell import Spell
from src import helpers
import argparse
import shlex
import re

def build_parser():
    parser = argparse.ArgumentParser(description="Filter spells based on flags.")
    parser.add_argument("-c",  "--class", nargs="+", help="Filter by spell class")
    parser.add_argument("-s", "--school", nargs="+", help="Filter by spell school")
    parser.add_argument("-l", "--level",  nargs="+", help="Filter by spell level")
    parser.add_argument("-cmp", "--component", nargs="+", help="Filter by spell components. Valid inputs are the letters v s m")
    parser.add_argument("-con", "--concentration", nargs="?", const=True, type=lambda input_str: input_str.lower() == "true", help="filter spells with concentration. -con false will exclude concentration spells.")   
    parser.add_argument("-r", "--ritual", nargs="?", const=True, type=lambda input_str: input_str.lower() == "true", help="filter spells with the ritual tag. -r false will exclude concentration spells.")

    return parser


def parse_query(user_input):

    parser = build_parser()
    args, unknown_args = parser.parse_known_args(shlex.split(user_input))
    return vars(args)


def filter_spells(list, search_filters, options=None): # generic filtering method

    filtered_spells = list

    class_filters = search_filters.get('class')
    school_filter = search_filters.get('school')
    component_filters = search_filters.get('component')
    concentration_filter = search_filters.get('concentration')
    level_filter = search_filters.get('level')
    ritual_filter = search_filters.get('ritual')

    if options:
        if not options.unearthed_arcana:
            filtered_spells = filter_ua(filtered_spells)
        optional_spells = options.optional_spells
    else:
        optional_spells = False

    if class_filters:
        for arg in class_filters:
            filtered_spells = filter_by_class(filtered_spells, arg, optional=optional_spells)

    if component_filters:
        for arg in component_filters:
            filtered_spells = filter_by_component(filtered_spells, arg) # TODO: ability to search for spells without a certain component

    if school_filter:
        filtered_spells = filter_by_school(filtered_spells, school_filter[0])

    if concentration_filter is not None: # concentration_filter is a bool
        filtered_spells = filter_by_concentration(filtered_spells, concentration_filter)

    if ritual_filter is not None: # ritual_filter is a bool
        filtered_spells = filter_by_ritual(filtered_spells, ritual_filter)

    if level_filter:
        filtered_spells = filter_by_level(filtered_spells, level_filter)

    return filtered_spells


def filter_by_class(spell_list, filter_class, optional=True): # returns list of spells belonging to a specified class

    if optional == True:
        filtered_spells = [spell for spell in spell_list if any(normalize_class_name(filter_class) == normalize_class_name(s) for s in spell.spell_lists)]
    else:
        filtered_spells = [spell for spell in spell_list if filter_class.lower() in [s.lower() for s in spell.spell_lists]]
    
    return filtered_spells


def filter_by_school(list, filter_school): #  returns list of spells of a specific school

    filtered_spells = [spell for spell in list if spell.school.lower() == filter_school.lower()]
    
    return filtered_spells


def filter_by_component(list, filter_component, has_component=True):

    filtered_spells = None

    if has_component:
        filtered_spells = [spell for spell in list if spell.has_component(filter_component.upper())]
    else:
        filtered_spells = [spell for spell in list if not spell.has_component(filter_component.upper())]

    return filtered_spells


def filter_by_concentration(list, is_concentration = True):

    filtered_spells = None

    if is_concentration == True:
        filtered_spells = [spell for spell in list if spell.is_concentration()]
    else:
        filtered_spells = [spell for spell in list if not spell.is_concentration()]
    
    return filtered_spells


def filter_by_level(list, levels):

    parsed_levels = parse_level_range(levels)

    filtered_spells = [spell for spell in list if spell.level_to_int() in parsed_levels]

    return filtered_spells


def filter_by_ritual(list, is_ritual = True):

    filtered_spells = None

    if is_ritual == True:
         filtered_spells = [spell for spell in list if spell.is_ritual()]
    else:
         filtered_spells = [spell for spell in list if not spell.is_ritual()]

    return filtered_spells


def filter_ua(list):

    filtered_spells = [spell for spell in list if "(UA)" not in spell.name]

    return filtered_spells


def filter_hb(list):

    filtered_spells = [spell for spell in list if "(HB)" not in spell.name]

    return filtered_spells


def parse_level_range(level_filter):
    
    levels = []

    for arg in level_filter:
        if arg.isdigit():
            levels.append(int(arg))
        elif arg == 'Cantrip':
            levels.append(0)

        ranges = re.match(r"\d+\.\.\d+", arg) # handling for range notation (0..3)

        try:
            if ranges is not None:
                nums = ranges.string.split('..')
                range_start = int(nums[0])
                range_end = int(nums[1])
                for x in range(range_start, range_end+1):
                    levels.append(int(x))
        except Exception as e:
            print(f"ERROR: {ranges} Invalid spell range.")

    return levels


def fetch_spell(list, name): # returns Spell object that matches a provided spell name
    
    spell_names = []

    try:
        for i, item in enumerate(list):
            spell_names.append(item.name)

        closest_spell = helpers.find_closest_spell(spell_names, name)

        for spell in list:
            if spell.name == closest_spell:
                return spell
    except:
        return None
    

def normalize_class_name(name):
    return re.sub(r"\s*\(.*?\)", "", name).strip().lower()

