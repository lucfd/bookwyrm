class Spell:

    def __init__(self, name, school, level, duration, cast_time, cast_range, description):
        self.name = name
        self.school = school
        self.level = level
        self.duration = duration
        self.cast_time = cast_time
        self.cast_range = cast_range
        self.components = []
        self.source = None
        self.description = description
        self.upcast = None
        self.spell_lists = []

    # getters
    def getName(self):
        return self.name
    
    def getSchool(self):
        return self.school
    
    def getRange(self):
        return self.cast_range