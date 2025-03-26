'''
toy.py: models the toy object
'''

import random
import matplotlib.pyplot as plt
import matplotlib.patches as pat

from ..utils.helper import flip_coords


# Class definition
class Toy:
    def __init__(self, name, position):
        self.name = name
        self.available = True
        self.position = position
        self.buried = False
        self.buried_by = None   # holds dog name
        self.held_by = None # holds dog name

    # Methods

    # Function which allows the toy interaction
    def interact(self, dog):
            dog.play_with_toy(self)
            self.available = False

    
    # Function which plots the toys on the map
    def plot_me(self, ax, LIMITS):
        fpos = flip_coords(self.position, LIMITS)
        color = 'purple' if not self.is_buried() else 'black'
        patch = pat.Rectangle((fpos[0]-0.5, fpos[1]-0.5), width=1, height=1, color=color)
        ax.add_patch(patch)
        ax.text(fpos[0], fpos[1] + 4, self.name, ha='center', fontsize=9, color=color)
        if self.is_buried():
            ax.text(fpos[0], fpos[1] - 4, "Buried!", ha='center', fontsize=9, color=color)

    # Accessors
    def get_name(self):
        return self.name

    def get_position(self):
        return self.position
    
    def is_available(self):
        return self.available
    
    def is_buried(self):
        return self.buried
    
    def get_buried_by(self):
        return self.buried_by
    
    def get_held_by(self):
        return self.held_by



    # Mutators
    def set_position(self, new_position):
        self.position = new_position

    def set_buried_by(self, dog_name):
        self.buried_by = dog_name

    def set_available(self, status):
        self.available = status

    def set_buried(self, status):
        self.buried = status

    def set_held_by(self, dog):
        self.held_by = dog