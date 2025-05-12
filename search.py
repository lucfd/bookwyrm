from spell import Spell
import helpers


def filter_spells(list, field, target): # generic filtering method

    filtered_spells = None

    if(field.lower()=="class"):
        filtered_spells = filter_by_class(list, target)
    elif(field.lower()=="school"):
        filtered_spells = filter_by_school(list, target)
    elif(field.lower()=="component"):
        filtered_spells = filter_by_component(list, target)

    return filtered_spells


def filter_by_class(list, filter_class): # returns list of spells belonging to a specified class

    filtered_spells = [spell for spell in list if filter_class.lower() in [s.lower() for s in spell.spell_lists]] # TODO: handling for Tasha's optional spell lists
    
    return filtered_spells


def filter_by_school(list, filter_school): #  returns list of spells of a specific school

    filtered_spells = [spell for spell in list if spell.school.lower()==filter_school.lower()]
    
    return filtered_spells


def filter_by_component(list, filter_component, has_component=True):

    filtered_spells = None

    if has_component:
        filtered_spells = [spell for spell in list if spell.has_component(filter_component.upper())]
    else:
        filtered_spells = [spell for spell in list if not spell.has_component(filter_component.upper())]

    return filtered_spells