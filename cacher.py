import requests
from bs4 import BeautifulSoup
import helpers
from difflib import get_close_matches
import spell


def display_spell(spell_name):

    print("spell name: ",spell_name)

    helpers.search_spell(helpers.reformat(spell_name))

def cache_spells(): # saves a list of all spell names to spells.txt

    spell_names = scrape_spell_names()
    save_spells(spell_names)


def scrape_spell_names(): # scrapes wikidot for a list of all spell names
    
    URL = "http://dnd5e.wikidot.com/spells"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="page-content")


    td_tags = soup.find_all('td')

    #print(newR[0]) # array of da guys
    spell_list = []
    
    for td_tag in td_tags:
    
        anchor_tags = td_tag.find_all('a')

        for spell_name in anchor_tags:
            spell_list.append(spell_name.get_text())
       # print(x.get_text())
        # print("-------------------")
    return spell_list


def save_spells(list): # save a list of all spell names

    with open('spells.txt', 'w') as f:

        for spell in list:
            f.write(spell)
            f.write('\n')


        f.close()
        
        
def read_cache():

    spells = []

    with open('spells.txt', 'r') as f:

         spells = f.read()
         
    #print(spells)
    data_into_list = spells.split("\n")
    data_into_list.remove('')
    #print(data_into_list)
    
    for i, item in enumerate(data_into_list):
    
        data_into_list[i] = helpers.reformat(item)
        #item = helpers.reformat(item)
    
    user_input = input("Enter spell name: ")
    print('matched words:',get_close_matches(user_input, data_into_list, 1))
    
    
def cache_search(user_input):

    spells = []

    with open('spells.txt', 'r') as f:

         spells = f.read()
         
    #print(spells)
    data_into_list = spells.split("\n")
    data_into_list.remove('')
    #print(data_into_list)
    
    for i, item in enumerate(data_into_list):
    
        data_into_list[i] = helpers.reformat(item)
        #item = helpers.reformat(item)
        
    return get_close_matches(user_input, data_into_list, 1)
    
    
    
def main():

    print("Caching...")

    cache_spells()
    read_cache()

	
if __name__ == "__main__":
    main() 