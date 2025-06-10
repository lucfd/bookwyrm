import requests
from bs4 import BeautifulSoup
from src import helpers
from difflib import get_close_matches
import json
from src.spell import Spell
from rich.progress import track
from pathlib import Path
import os

def update_spells_txt(): # scrapes a list of all spell names, saves them to spells.txt

    spell_names = scrape_spell_names()
    save_spell_names(spell_names)


def scrape_spell_names(): # scrapes wikidot for a list of all spell names
    
    URL = "http://dnd5e.wikidot.com/spells"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="page-content")


    td_tags = results.find_all('td')

    spell_list = []
    
    for td_tag in track(td_tags, description="Building spell index...", total=len(td_tags)):
    
        anchor_tags = td_tag.find_all('a')

        for spell_name in anchor_tags:
            spell_list.append(spell_name.get_text())

    return spell_list


def save_spell_names(spell_list): # save a list of spell names to spells.txt

    with open('spells.txt', 'w') as f:

        for spell in spell_list:
            f.write(spell)
            f.write('\n')

        f.close()


def initialize_spells(backup=True): # loads spell data into memory. backup=False will scrape wikidot, True pulls from spells.json

    spell_list = []
    # attempt to load spells from spells.json backup
    if(backup):
        try: 
            with open('spells.json', 'r') as file:
                spell_list = json.load(file)
                return helpers.spellify_list(spell_list)

        except FileNotFoundError:
            print("Failed to load spells.json - file could not be found.")
        except Exception as e:
            print("Failed to load spells.json")
            print(f"Error: {e}")

    # check if spells.txt exists (important for first-time users)
    file_path = Path('spells.txt')
    if not file_path.is_file():
        try:
            update_spells_txt()
        except Exception as e:
            print("Failed to build spell index.")
            print(f"Error: {e}")

            return None
        
    # scrape spell information, parse to json, return list of spell jsons
    try:
        with open('spells.txt', 'r') as f:

            spells = f.read()
            
        data_into_list = spells.split("\n")
        data_into_list.remove('')
        
        for i, item in enumerate(data_into_list):
            data_into_list[i] = helpers.reformat(item)
        
        json_list = []

        for i, new_spell_info in track(enumerate(data_into_list), description="Scraping spells from the web...", total=len(data_into_list)):
            scraped_spell = helpers.scrape_spell(match_spell(helpers.reformat(new_spell_info)))
            json_list.append(scraped_spell)

        # remove bad data from list
        json_list = helpers.clean_list(json_list)

        return json_list
    
    except Exception as e:
        print("Failed to load data from the web.")
        print(f"Error: {e}")

    return None


def save_spells(spell_list): # save all spells to json

    with open('spells.json', 'w') as f:
        json.dump(spell_list, f, indent=4)
        f.close()
        
    
def match_spell(user_input): # searches spells.txt for input string, returns closest match

    spells = []

    with open('spells.txt', 'r') as f:

         spells = f.read()

    data_into_list = spells.split("\n")
    data_into_list.remove('')
    
    for i, item in enumerate(data_into_list):
        data_into_list[i] = helpers.reformat(item)
        
    return get_close_matches(user_input, data_into_list, 1)


def find_new_spells(return_old=False): # returns a list of scraped spell names not found in spells.txt
    new_spell_names = scrape_spell_names()

    with open('spells.txt', 'r') as f:
            old_spells = f.read().splitlines()
            new_spells = [spell_name for spell_name in new_spell_names if spell_name not in old_spells]

    if return_old: # return both old and new spells
        return [old_spells, new_spells]
    else:
        return new_spells
    

def delete_library(spell_names="spells.txt", spell_data="spells.json"):

    if os.path.exists(spell_names):
        try:
            os.remove(spell_names)
            print(f"Successfully deleted {spell_names}")
        except:
            print(f"Failed to delete {spell_names}")
    
    if os.path.exists(spell_data):
        try:
            os.remove(spell_data)
            print(f"Successfully deleted {spell_data}")
        except:
            print(f"Failed to delete {spell_data}")  