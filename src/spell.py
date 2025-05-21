class Spell:

    def __init__(self, name, school, level, duration, cast_time, cast_range, components, source, description, upcast, spell_lists, ritual):
        self.name = name
        self.school = school
        self.level = level
        self.duration = duration
        self.cast_time = cast_time
        self.cast_range = cast_range
        self.components = components
        self.source = source
        self.description = description
        self.upcast = upcast
        self.spell_lists = spell_lists
        self.ritual = ritual

    def output(self):
        print(f"Name: {self.name}")
        print(f"School: {self.school}")
        print(f"Level: {self.level}")
        print(f"Duration: {self.duration}")
        print(f"Cast Time: {self.cast_time}")
        print(f"Range: {self.cast_range}")
        print(f"Components: {self.components}")
        print(f"Source: {self.source}")
        print(f"Description: {self.description}")
        print(f"Upcast: {self.upcast}")
        print(f"Spell Lists: {self.spell_lists}")       

    def to_json(self):
        return {
            "name": self.name,
            "school": self.school,
            "level": self.level,
            "duration": self.duration,
            "cast_time": self.cast_time,
            "cast_range": self.cast_range,
            "components": self.components,
            "source": self.source,
            "description": self.description,
            "upcast": self.upcast,
            "spell_lists": self.spell_lists,
            "ritual": self.ritual
        }
    
    def get_component(self, component_type): # returns the component matching the type provided ("V", "S", "M"). returns None if not found
        return(next((component for component in self.components if component.startswith(component_type)), None))  

    def has_component(self, component_type): # returns True if spell has specified component type, False otherwise
        
        if self.get_component(component_type) is None:
            return False
        else:
            return True
        
    def is_concentration(self):
        
        if 'Concentration' in self.duration:
            return True
        else:
            return False
        
    def level_to_int(self):
        
        if self.level == 'Cantrip':
            return 0
        elif self.level[0].isnumeric():
            return int(self.level[0])

    def is_ritual(self):
        return self.ritual

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

