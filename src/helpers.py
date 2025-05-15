import requests
from bs4 import BeautifulSoup
from src.spell import Spell
import re
from difflib import get_close_matches


SPELL_SCHOOLS = ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Transmutation"]
SPELL_LEVELS = ["Cantrip", "1st-Level", "2nd-Level", "3rd-Level", "4th-Level", "5th-Level", "6th-Level", "7th-Level", "8th-Level", "9th-Level"]


# SCRAPING HELPERS

def scrape_spell_json(spell_name): # scrape spell's info, returns as json

    URL = "http://dnd5e.wikidot.com/spell:"+spell_name[0]
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    
    return parse_to_json(soup, soup.title.get_text().split(' -')[0])


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
    spell_description = None
    spell_upcast = None
    spell_lists = []

    spell_html = soup.find_all('p')

    for x in spell_html:

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
            spell_description = x.get_text()

    # handling spell school and level
    emphasis = soup.find("em")
    spell_school = next(
        (school for school in SPELL_SCHOOLS if emphasis.get_text() and school.lower() in emphasis.get_text().lower()),
    None)
    spell_level = next(
        (level for level in SPELL_LEVELS if emphasis.get_text() and level.lower() in emphasis.get_text().lower()),
    None)    

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
    "spell_lists": spell_lists
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


def clean_list(list):

    list[:] = [item for item in list if item is not None]
    return


def find_closest_spell(list, target): # finds closest matching spell name in a list of strings

    try:
        return get_close_matches(target, list, 1)[0]
    except:
        return None