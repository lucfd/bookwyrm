import requests
from bs4 import BeautifulSoup
from src.spell import Spell
import re
from difflib import get_close_matches
import json


SPELL_SCHOOLS = ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Transmutation"]
SPELL_LEVELS = ["Cantrip", "1st-Level", "2nd-Level", "3rd-Level", "4th-Level", "5th-Level", "6th-Level", "7th-Level", "8th-Level", "9th-Level"]

class UserPreferences:

    def __init__(self, unearthed_arcana=True, optional_spells=True, disabled_sourcebooks=[], theme="Lich"):
        self.unearthed_arcana = unearthed_arcana
        self.optional_spells = optional_spells
        self.disabled_sourcebooks = disabled_sourcebooks
        self.theme = theme

    def to_json(self):
        return {
            "unearthed_arcana": self.unearthed_arcana,
            "optional_spells": self.optional_spells,
            "disabled_sourcebooks": self.disabled_sourcebooks,
            "theme": self.theme
        }
    
    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)
    

# SCRAPING HELPERS

def scrape_spell_json(spell_name): # scrape spell's info, returns as json

    URL = "http://dnd5e.wikidot.com/spell:"+spell_name[0]
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="page-content")

    return parse_to_json(results, soup.title.get_text().split(' -')[0])


def scrape_spell(spell_name): # scrape spell's info, returns as Spell object

    spell_json = scrape_spell_json(spell_name)

    if(spell_json is None):
        return None

    new_spell = Spell.from_json(spell_json)

    return new_spell


def spellify_list(list): # converts list of spell dicts to list of Spell objects

    new_list = []

    for item in list:
        new_list.append(Spell.from_json(item))

    return new_list


def jsonify_list(list):

    new_list = []

    for item in list:
        new_list.append(item.to_json())

    return new_list

    
def parse_to_json(soup, name): # converts scraped html to json

    spell_name = name
    spell_school = None
    spell_level = None
    spell_duration = None
    spell_cast_time = None
    spell_cast_range = None
    spell_components = []
    spell_source = None
    spell_description = ""
    spell_upcast = None
    spell_lists = []
    is_ritual = False

    spell_html = soup.find_all(['p','ul'])

    # handling spell school and level
    emphasis = soup.find("em")
    emphasis_text = emphasis.get_text() if emphasis else ""
    emphasis_container = emphasis.find_parent("p") if emphasis else None

    spell_school = next(
        (school for school in SPELL_SCHOOLS if school.lower() in emphasis_text.lower()),
    None)
    spell_level = next(
        (level for level in SPELL_LEVELS if level.lower() in emphasis_text.lower()),
    None)

    if "ritual" in emphasis_text:
        is_ritual = True

    for x in spell_html:

        if x == emphasis_container: # prevents spell & school <p> tag from accidentally being appended to spell_description
            continue

        if(x.get_text().startswith('Source:')):
            spell_source = x.get_text().split(': ')[1]
        elif(x.get_text().startswith('Casting Time:')):
            pattern = r'Casting Time:\s*(.+?)\nRange:\s*(.+?)\nComponents:\s*(.+?)\nDuration:\s*(.+)'
            match = re.search(pattern, x.get_text())
            if match: # handling for legacy format (one <p> for four attributes)
                casting_time, spell_range, components, duration = match.groups()
                spell_cast_time = casting_time
                spell_cast_range = spell_range
                spell_components = components.split(', ')
                spell_duration = duration
            else: # handling for modern format (different <p> for each attribute)
                spell_cast_time = x.get_text().split(': ')[1]
        elif(x.get_text().startswith('Range:')):
            spell_cast_range = x.get_text().split(': ')[1]
        elif(x.get_text().startswith('Components:')):
            spell_components = x.get_text().split(': ')[1].split(', ')
        elif(x.get_text().startswith('Duration:')):
            spell_duration = x.get_text().split(': ')[1]
        elif(x.get_text().startswith('At Higher Levels.')):
            spell_upcast = x.get_text().split('At Higher Levels. ')[1]
        elif(x.get_text().startswith('Spell Lists.')):
            for class_name in x.get_text().split('Spell Lists. ')[1].split(', '):
                spell_lists.append(class_name)
        else:
            spell_description = spell_description + x.get_text() +"\n" # covers spells that break descriptions into multiple tags


    json_data = {
    "name": spell_name,
    "school": spell_school,
    "level": spell_level,
    "duration": spell_duration,
    "cast_time": spell_cast_time,
    "cast_range": spell_cast_range,
    "components": spell_components,
    "source": spell_source,
    "description": spell_description,
    "upcast": spell_upcast,
    "spell_lists": spell_lists,
    "ritual": is_ritual
}
    
    # prune bad data
    if None in (json_data.get("name"), json_data.get("school"), json_data.get("level")):
        return None

    
    return json_data


def reformat(string):

    new_string = string.replace(" (UA)","")
    new_string = new_string.replace(" (HB)","")
    new_string = new_string.replace(" ","-")
    new_string = new_string.replace("'","")
    new_string = new_string.replace("/","-")
    new_string = new_string.replace(":","")


    return(new_string)


def clean_list(spell_list): # removes invalid & duplicate items from a provided list

    # remove invalid items
    temp_list = [item for item in spell_list if isinstance(item, Spell)]

    seen_spells = []
    final_list = []
    # remove duplicates
    for spell in temp_list:
        if(spell.name not in seen_spells):
            seen_spells.append(spell.name)
            final_list.append(spell)

    return final_list


def find_closest_spell(spell_list, target, num_results = 1, similarity=0.6): # finds closest matching spell name in a list of strings

    try:
        matches = get_close_matches(target, spell_list, n=num_results, cutoff=similarity)
        return matches[0] if num_results==1 else matches
    except:
        return None
    

def get_sourcebooks(spell_list):

    unique_sourcebooks = set()

    for spell in spell_list:
        spell_sources = re.split(r'\s*/\s*', spell.source) # avoid edge cases such as reprinted blade cantrips "elemental evil/xanathar"
        for source in spell_sources:
            if "Unearthed Arcana" not in spell.source:
                unique_sourcebooks.add(source.strip())

    organized_sourcebooks = []
    for source in unique_sourcebooks:
        organized_sourcebooks.append(source)
    organized_sourcebooks.sort()

    return organized_sourcebooks


def initialize_preferences():
    try: 
        with open('prefs.json', 'r') as file:
            pref_json = json.load(file)
        return UserPreferences.from_json(pref_json)
    except FileNotFoundError:
        new_prefs = UserPreferences()
        return new_prefs
    except Exception as e:
        return None
    

def save_preferences(preferences):

    with open('prefs.json', 'w') as f:
        json.dump(preferences.to_json(), f, indent=4)
        f.close()