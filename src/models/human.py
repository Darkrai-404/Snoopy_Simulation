'''
human.py: models the human object.
'''

import random, math
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from ..utils.helper import flip_coords, distance


class Human:
    def __init__(self, name, relation, position):
        self.name = name
        self.relation = relation
        self.position = position
        self.whistle = False
        self.nearby_dog_barking = False


    ###################################################
    #                   Whistle                       #
    ###################################################
    def start_whistling(self):
        self.whistle = True

    def stop_whistling(self):
        self.whistle = False

    def is_whistling(self):
        return self.whistle


    def detect_surrounding(self, dogs):
        if self.relation == "Friend":
            nearby_dog = False
            for dog in dogs:
                distance_to_dog = distance(self.get_position(), dog.get_position())
                if distance_to_dog <= 30 and dog.is_bored(): # Human whistle 30 grid, dog hears 20 grid, dog plays 5 grid
                    self.start_whistling()
                    nearby_dog = True
                if not nearby_dog:
                    self.stop_whistling()

        if self.relation == "Stranger":
            for dog in dogs:
                distance_to_dog = distance(self.get_position(), dog.get_position())
                if distance_to_dog <= 20 and dog.is_barking():
                    self.nearby_dog_barking = True
                    # Run from dog
                    dog_position = dog.get_position()
                    current_position = self.get_position()

                    dx = 1 if dog_position[0] < current_position[0] else - 1
                    dy = 1 if dog_position[1] < current_position[1] else - 1

                    # Calculate new position to move to
                    new_position = (current_position[0] + dx, current_position[1] + dy)
                    self.set_position(new_position)
            if not dog.is_barking():
                self.nearby_dog_barking = False


    # Methods
    def move(self, dogs):
        dx = random.choice([-1, 0, 1])  
        dy = random.choice([-1, 0, 1])  

        # Update the position
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        # Ensure the new position is within the limits of the yard
        # Assuming LIMITS is a tuple containing the dimensions of the yard (e.g., (100, 100))
        LIMITS = (220, 190)
        new_x = max(0, min(new_x, LIMITS[0] - 1))
        new_y = max(0, min(new_y, LIMITS[1] - 1))

        self.position = (new_x, new_y)

        self.detect_surrounding(dogs)



    # Function which plots the humans on the simulation
    def plot_me(self, ax, LIMITS):
        fpos = flip_coords(self.position, LIMITS)
        # Draw the body (rectangle)
        body = pat.Rectangle((fpos[0]-0.5, fpos[1]-0.5), width=2, height=3, color='maroon')
        ax.add_patch(body)
        # Draw the head (circle)
        
        if(self.get_relation() == "Stranger"):
            head = pat.Circle((fpos[0]+0.63, fpos[1]-1.5), radius=1.5, color='blue')
        else:
            head = pat.Circle((fpos[0]+0.63, fpos[1]-1.5), radius=1.5, color='red')
        ax.add_patch(head)

        ax.text(fpos[0], fpos[1] + 6, f"{self.relation}: {self.name}", ha='center', fontsize=9, color='black') #annotations

        # Whistling
        if self.is_whistling():
            ax.text(fpos[0], fpos[1] - 4, "*whistle*", ha='center', fontsize = 9, color='Black', fontweight='bold')

        # Scared by barking
        if self.nearby_dog_barking:
            ax.text(fpos[0], fpos[1] - 4, "!!!", ha='center', fontsize = 9, color='Black', fontweight='bold')

    # Accessors
    def get_position(self):
        return self.position
    
    def get_name(self):
        return self.name
    
    def get_relation(self):
        return self.relation

    # Mutators
    def set_position(self, new_position):
        self.position = new_position