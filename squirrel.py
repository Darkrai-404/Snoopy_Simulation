'''
squirrel.py: models the squirrel object. Extends from the animal parent class.
'''

import random, math
from animal import Animal
import matplotlib.pyplot as plt
import matplotlib.patches as pat

def distance(point1, point2):
    return math.sqrt(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))

# Flips the map coordinates
def flip_coords(position, LIMITS):
    return((position[1],position[0]))

# Class definition. Extends from the animal class
class Squirrel(Animal):
    def __init__(self,name, position):
        super().__init__(name, age=None) # age is not required for squirrels
        self.position = position
        self.nearby_dog_barking = False

    # Methods

    # Function which allows the squirrels to move
    def move(self, dogs):     # Squirrels will move faster than the Dogs
        valid_moves = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]
        
        # Choose a random valid move
        dx, dy = random.choice(valid_moves)

        # Update the position
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # Ensure the new position is within the limits of the yard
        # Assuming LIMITS is a tuple containing the dimensions of the yard (e.g., (220, 190))
        LIMITS = (220, 190)
        new_x = max(0, min(new_x, LIMITS[0] - 1))
        new_y = max(0, min(new_y, LIMITS[1] - 1))

        self.position = (new_x, new_y) 

        self.detect_surrounding(dogs)       

    def detect_surrounding(self, dogs):
        for dog in dogs:
            distance_to_dog = distance(self.get_position(), dog.get_position())
            if distance_to_dog <= 20 and dog.is_barking():
                self.nearby_dog_barking = True
                # Run from dog
                dog_position = dog.get_position()
                current_position = self.get_position()

                dx = 2 if dog_position[0] < current_position[0] else - 2
                dy = 2 if dog_position[1] < current_position[1] else - 2

                # Calculate new position to move to
                new_position = (current_position[0] + dx, current_position[1] + dy)
                self.set_position(new_position)
        if not dog.is_barking():
            self.nearby_dog_barking = False


    # Function which plots the squirrels on the map
    def plot_me(self, ax, LIMITS):
        fpos = flip_coords(self.position, LIMITS)
        patch = pat.Circle(fpos, radius=0.9, color='black')
        ax.add_patch(patch)

        # Scared by barking
        if self.nearby_dog_barking:
            ax.text(fpos[0], fpos[1] - 4, "!!!", ha='center', fontsize = 9, color='Black', fontweight='bold')

    # Accessor
    def get_position(self):
        return self.position
    
    # Mutator
    def set_position(self, new_position):
        self.position = new_position