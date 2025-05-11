import requests
from bs4 import BeautifulSoup
import helpers
import cacher


def display_spell(spell):
    spell.output()


def filter_by_class(list, filter_class):

    filtered_spells = [spell for spell in list if filter_class in [s.lower() for s in spell.spell_lists]]

    [print(spell.name) for spell in filtered_spells]
    
    return filtered_spells


def filter_by_school(list, filter_class):

    filtered_spells = [spell for spell in list if filter_class in [s.lower() for s in spell.spell_lists]]

    [print(spell.name) for spell in filtered_spells]
    return filtered_spells


def main():

    print('------Bookwyrm------')

    spells = cacher.initialize_spells()

    if(spells == None):
        print("Aborting program.")
        return




    user_input = input("Enter spell name: ")

    filter_by_class(spells, user_input)


if __name__ == "__main__":
    main()