import requests
from bs4 import BeautifulSoup
import helpers
import cacher


def display_spell(spell_name):

    print("spell name: ",spell_name)

    helpers.search_spell(cacher.cache_search(helpers.reformat(spell_name)))


def main():

    user_input = input("Enter spell name: ")

    display_spell(user_input)


if __name__ == "__main__":
    main()