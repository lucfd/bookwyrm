import requests
from bs4 import BeautifulSoup
import helpers
from difflib import get_close_matches


def display_spell(spell_name):

    print("spell name: ",spell_name)

    helpers.search_spell(helpers.reformat(spell_name))


def cache_spells():
    
    URL = "http://dnd5e.wikidot.com/spells"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="page-content")

    #print(soup.title.get_text())
    #print(results.prettify())
    #print(results.get_text())

    #print(results.get_text())
    #print(results.p)

    newR = soup.find_all('td')

    #print(newR[0]) # array of da guys
    spell_list = []
    
    for x in newR:
    
        spell_name = x.find_all('a')

        for y in spell_name:
            
            #print(y.get_text())
            spell_list.append(y.get_text())
       # print(x.get_text())
        # print("-------------------")
		
    with open('spells.txt', 'w') as f:
    
        for z in spell_list:
            f.write(z)
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