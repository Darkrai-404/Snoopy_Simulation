'''
foodbowl.py: This class models the foodbowl which is dropped by the humans
'''

import matplotlib.patches as pat
import numpy as np

from ..utils.helper import flip_coords

# Class definition
class FoodBowl:
    def __init__(self, position, capacity=100):
        self.position = position
        self.capacity = capacity
        self.food_level = capacity

# Methods

    # Decreases the food level inside the foodbowl
    def decrease_food(self, amount):
        self.food_level -= amount
        if self.food_level < 0:
            self.food_level = 0

    # Function which plots the food bowl on the map
    def plot_me(self,ax):
        fpos = flip_coords(self.position, (220,190))
        gradient = ['#FF0000', '#FFFF00', '#00FF00']
        n_colours = len(gradient)
        colour_index = int(np.clip(self.food_level / 100 * n_colours, 0, n_colours - 1))
        colour = gradient[colour_index]

        # Plot larger black circle for outline
        patch_outline = pat.Circle(fpos, radius=1.8, color='black')
        ax.add_patch(patch_outline)

        patch = pat.Circle(fpos, radius=1.5, color=colour)
        ax.add_patch(patch)

        ax.text(fpos[0], fpos[1], r"$\bf{F}$", ha='center', va='center', fontsize=5, color='black')
    

    # Accessors
    def get_food_level(self):
        return self.food_level

    def get_position(self):
        return self.position
    
    def get_is_occupied(self):
        return self.isOccupied
    
    def is_empty(self):
        return self.food_level == 0

    