import requests
from bs4 import BeautifulSoup
from spell import Spell

SPELL_SCHOOLS = ["Abjuration", "Conjuration", "Divination", "Enchantment", "Evocation", "Illusion", "Necromancy", "Transmutation"]
SPELL_LEVELS = ["Cantrip", "1st-Level", "2nd-Level", "3rd-Level", "4th-Level", "5th-Level", "6th-Level", "7th-Level", "8th-Level", "9th-Level"]

def search_spell(spell_name):

    URL = "http://dnd5e.wikidot.com/spell:"+spell_name[0]
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    
    parse_to_json(soup, soup.title.get_text().split(' -')[0])
    
   # for x in newR:
   #     print(x.get_text())

    
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

        print("$ "+x.get_text())

        if(x.get_text().startswith('Source:')):
            print('Source...')
            spell_source = x.get_text().split(': ')[1]
        elif(x.get_text().startswith('Casting Time:')):
            print('Casting Time...')
            spell_cast_time = x.get_text().split(': ')[1]
        elif(x.get_text().startswith('Range:')):
            print('Range...')
            spell_cast_range = x.get_text().split(': ')[1]
        elif(x.get_text().startswith('Components:')):
            print('Components...')
            temp_components = x.get_text()
            print(temp_components)
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


    big_list = []
    for x in spell_html:

        for y in x.get_text().split('\n'):
            big_list.append(y)

    print(big_list)
    #print(spell_components)
        #print(x.get_text())
  #  print(soup[1].get_text())
    #print(spell_lists)
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
    print("-------------")
    spell = Spell.from_json(json_data)
    spell.output() # Output: Fireball
    print("$$$$$$$$$$$$$$$$")

#print(soup.title.get_text())
#print(soup.title.get_text())

def reformat(string):

    new_string = string.replace(" (UA)","")
    new_string = new_string.replace(" (HB)","")
    new_string = new_string.replace(" ","-")
    new_string = new_string.replace("'","")
    new_string = new_string.replace("/","-")
    new_string = new_string.replace(":","")


    return(new_string)    