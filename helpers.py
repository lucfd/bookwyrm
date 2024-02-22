import requests
from bs4 import BeautifulSoup

def search_spell(spell_name):

    URL = "http://dnd5e.wikidot.com/spell:"+spell_name[0]
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="page-content")

    #print(soup.title.get_text())
    #print(results.prettify())
    #print(results.get_text())

    #print(results.get_text())
    #print(results.p)

    newR = soup.find_all('p')

    #print(newR[0]) # array of da guys

    for x in newR:
        print(x.get_text())

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