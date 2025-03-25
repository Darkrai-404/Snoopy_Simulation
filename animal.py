'''
animal.py: Parent class for dog and squirrel
'''

# Class definition
class Animal():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Accessors
    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    # Mutators
    def set_name(self, new_name):
        self.name = new_name

    def set_age(self, new_age):
        self.age = new_age

