'''
dog.py: implements the dog object. Extends from the animal parent class.

'''

import math, random
from src.models.animal import *
from src.models.toy import *
from src.models.foodbowl import *
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np

# Import utils
from ..utils.helper import flip_coords, distance

# # Flips the map coordinates.
# def flip_coords(position, LIMITS):
#     return((position[1],position[0]))

# # Python formula to find distance between two points
# # REF: https://www.w3resource.com/python-exercises/python-basic-exercise-40.php
# def distance(point1, point2):
#     return math.sqrt(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))

# Class definition. Extends from animal class.
class Dog(Animal):
    def __init__(self, name, age, colour, position):
        super().__init__(name, age)

        # colour implementation
        csplit = colour.split("/")
        self.colour1 = csplit[0]
        if len(csplit) == 2:
            self.colour2 = csplit[1]
        else:
            self.colour2 = csplit[0]

        self.energy = 80    # initial energy 
        self.position = position
        self.holding_toy = None     # A toy object 
        self.inactive_steps = 0     # Used to calculate boredom
        self.barking = False
        self.dog_hears_whistle = False

        # Energy Management
        self.max_energy = 100
        self.energy_decay_rate = 0.001 # energy decay during time step

        # Data Collection
        self.buried_toys = 0
        self.dropped_toys = 0
        self.interactions_with_toys = 0
        self.toys_interacted_with = []  # List to hold toy names
        self.dug_up_toy_via_smell = 0
        self.food_intake_winter = 0
        self.food_intake_summer = 0



    '''
    Class Methods
    '''

    ################################################################
    #                    For Toy Interaction                       #
    ################################################################

    # Locates the nearest toy object to the dog object
    def find_nearest_toy(self, toys):
        if not isinstance(toys, list):  ## converting to list to bypass non-iterable error
            toys = [toys]

        nearest_toy = None
        min_distance = float('inf')

        detection_range = 10    # Implements the smell sense for dogs. Dogs can smell toys within 10 grids

        for toy in toys:
            if toy.is_available:     # Not held by any dog
                dist = distance(self.get_position(), toy.get_position()) 
                if not toy.is_buried():   # Normal dog sight function to pick up toy
                    if dist < min_distance:
                        min_distance = dist
                        nearest_toy = toy
                elif toy.get_buried_by() == self.get_name():     # Dog which buried the toy can directly dig out toy
                    if dist < min_distance:
                        min_distance = dist
                        nearest_toy = toy
                elif dist <= detection_range:       # Dogs which did not bury the toy will need to be in a range to smell toy's presence
                    if dist < min_distance:
                        print(f"{self.get_name()} got the scent of toy and other dog's presence")
                        min_distance = dist
                        nearest_toy = toy
        return nearest_toy
    

    # The dog moves towards the nearest toy
    def move_towards_toy(self, toy):
        nearest_toy = self.find_nearest_toy(toy)

        if nearest_toy:         # Function makes dog move 1 step towards the toy in each timestep
            current_position = self.get_position()
            toy_position = nearest_toy.get_position()

            # Movement direction calculation for x,y coodinates
            dx = 1 if toy_position[0] > current_position[0] else -1
            dy = 1 if toy_position[1] > current_position[1] else -1

            # Calculate new position to move to
            new_position = (current_position[0] + dx, current_position[1] + dy)

            # Update the dog's position
            self.set_position(new_position)

    # The first function to be called from the main simulation loop for toy activity
    def interact_with_toy(self, toys):     
        interaction_range = 2
        if self.is_bored():
            if not self.has_toy():
                nearest_toy = self.find_nearest_toy(toys)
                if nearest_toy:
                    if nearest_toy.is_available():
                        if distance(nearest_toy.get_position(), self.get_position()) < interaction_range:     # Dog can interact if within 2 grids
                            if nearest_toy.is_buried():
                                self.dig_up_toy(nearest_toy, toys)
                            else:
                                self.pick_up_toy(nearest_toy, toys)
                        else:
                            self.move_towards_toy(nearest_toy)
                    else:
                        # Find another available toy
                        available_toys = [toy for toy in toys if toy.is_available()]
                        if available_toys:
                            nearest_available_toy = self.find_nearest_toy(available_toys)
                            self.move_towards_toy(nearest_available_toy)
            else:
                print(f"{self.get_name()} already has a toy: {self.holding_toy.get_name()}, interacting with said toy")
                self.holding_toy.interact(self)     # interact function in toy class

    # Function to allow dog to play with toy
    def play_with_toy(self, toy):
        energy_cost = 10
        print(f"{self.get_name()} is playing with the toy {toy.name}!")
        self.set_energy(self.get_energy() - energy_cost)
        self.energy = max(0, self.energy) # prevent energy from reaching below 0
        self.reset_boredom()     # reset boredom counter

        # Data collection
        self.interactions_with_toys +=1
        self.toys_interacted_with.append(toy.get_name())
        
    # Function to allow dog to pick up toy from the ground
    def pick_up_toy(self, toy, toys):
        print(f"{self.get_name()} picked up the toy {toy.name}!")
        self.reset_boredom()
        toy.set_available(False)
        toy.set_buried(False)
        self.holding_toy = toy


        # toys = All the toys on the map
        # toy = the toy that our dog is about to pick up
        # index = toys[index] = toy <-- this means the index of our toy in the toys collection

        toy_index = toys.index(toy)
        toys.pop(toy_index)  # pop the toy from the list
        toy.interact(self)  # defined in the toy class

        
    # Function to allow dog to drop toy on the ground
    def drop_toy(self, toys):
        if self.holding_toy:
            self.reset_boredom()     # reset boredom counter
            print(f"{self.get_name()} is dropping the toy {self.holding_toy.name}!")
            self.holding_toy.set_position(self.get_position())
            self.holding_toy.set_available(True)
            toys.append(self.holding_toy)       # add the toy back to the list
            self.holding_toy = None
            self.reset_boredom()     # reset counter again to avoid runtime logic error

            # Data Collection
            self.dropped_toys += 1
            
            # toys = All the toys on the map
            # toy = the toy that our dog is about to pick up
            # index = toys[index] = toy <-- this means the index of our toy in the toys collection


    # Function to allow the dog to bury the toy object            
    def bury_toy(self, toys):
        if self.has_toy():
            energy_cost = 5
            buried_toy = self.holding_toy
            buried_toy.set_buried_by(self.name)  # to keep track of current "owner"
            self.holding_toy.set_buried(True)
            print(f"{self.get_name()} buried the toy {self.holding_toy.name}! Ignore the next drop statement")
            self.drop_toy(toys)     # drop mechanism used to implement bury functionality
            self.set_energy(self.get_energy() - energy_cost)
            # Data collection
            self.buried_toys += 1
            self.dropped_toys -=1

        else:
            print(f"{self.get_name} is trying to bury a toy it doesn't hold")

    # Function to allow the dog to dig up a buried toy
    def dig_up_toy(self, toy, toys):
        dig_energy_cost = 5

        # Data collection
        if self.get_name() != toy.get_buried_by():
            self.dug_up_toy_via_smell += 1

        self.pick_up_toy(toy, toys) # pickup mechanism used to implement dig function
        print(f"{self.get_name()} dug up the toy {self.holding_toy.name}!")
        self.set_energy(self.get_energy() - dig_energy_cost)



    ###############################################################
    #                    FOR FOOD INTERACTION                     #
    ###############################################################

    # Function to allow dog to find nearest foodbowl
    def find_nearest_foodbowl(self, foodbowls):
        if not isinstance(foodbowls, list): # convert to list to bypass non-iterable error
            foodbowls = [foodbowls]

        min_distance = float('inf')
        nearest_bowl = None
    
        for bowl in foodbowls:
            if not bowl.is_empty() and bowl is not None:    
                distance_to_bowl = distance(bowl.get_position(), self.get_position())  # Initialize distance_to_bowl
                if distance_to_bowl < min_distance:
                    min_distance = distance_to_bowl
                    nearest_bowl = bowl    
        return nearest_bowl
    

    # Function to allow dog to interact with foodbowl
    # Primary food interaction method to be called from the main simulation loop
    def interact_with_food(self, foodbowl, season):     #first
        nearest_bowl = self.find_nearest_foodbowl(foodbowl)
        eating_range = 3
        # If the distance to the nearest bowl is less than 3, the dog eats from it
        if distance(nearest_bowl.get_position(), self.get_position()) < eating_range and not nearest_bowl.is_empty():
            
            # Mechanism which allows dog to keep eating until it reaches 50 energy units or till the maximum food level
            available_food = nearest_bowl.get_food_level()
            desired_energy = 50
            how_much_to_eat = desired_energy - self.get_energy()

            if available_food >= how_much_to_eat:
                print(f"{self.get_name()} is able to satisfy hunger")
                self.eat(how_much_to_eat, season)
                nearest_bowl.decrease_food(how_much_to_eat)
                print(f"{self.get_name()} ate {how_much_to_eat:.2f} units of food from the bowl")

            else:
                # Eat whatever foodlevel the bowl has
                print(f"{self.get_name()} is able to PARTIALLY satisfy hunger")
                self.eat(available_food, season)
                nearest_bowl.decrease_food(available_food)
                print(f"{self.get_name()} ate {available_food:.2f} units of food from the bowl")

            self.reset_boredom()     # reset boredom level
        else:
            # Move towards the nearest bowl
            self.move_towards_foodbowl(nearest_bowl)



    # Function which allows the dog to move towards the foodbowl
    def move_towards_foodbowl(self, foodbowl):
        nearest_bowl = self.find_nearest_foodbowl(foodbowl)
        if nearest_bowl:
            current_position = self.get_position()
            bowl_position = nearest_bowl.get_position()

            # Calculate the movement direction
            # -2 is used to simulate the running action
            dx = 2 if bowl_position[0] > current_position[0] else -2
            dy = 2 if bowl_position[1] > current_position[1] else -2

            # Calculate the new position
            new_position = (current_position[0] + dx, current_position[1] + dy)

            # Set the new dog position
            self.set_position(new_position)


    # Function which allows the dog to eat
    def eat(self, amount, season):
        if season == "Winter":
            self.food_intake_winter += amount
        if season == "Summer":
            self.food_intake_summer += amount
        self.energy += amount
        self.energy = min(100, self.energy) # limit energy to 100




    ##########################################################
    #                      Barking                           #
    ##########################################################

    # Check if dog is barking
    def is_barking(self):
        return self.barking
    
    # Dog starts barking
    def start_barking(self):
        self.barking = True


    # Dog stops barking
    def stop_barking(self):
        self.barking = False
   

    # Function which allows the dog to bark
    def bark(self):
        energy_cost = 0.02
        # print("Woof! Woof!")
        self.set_energy(self.get_energy() - energy_cost)
        self.reset_boredom()
        self.start_barking()

    # Detecting surroundings
    def detect_surrounding(self, humans, squirrels, should_stop_listening):
        
        if(should_stop_listening):
            self.dog_hears_whistle = False

        else:
            # Detects humans nearby
            stranger_nearby = False  # flag to track if any strangers are nearby
            squirrels_nearby = False    # flag to track if any squirrels are nearby

            for human in humans:
                distance_to_human = distance(self.get_position(), human.get_position())


                if self.is_bored() and distance_to_human <=20 and human.is_whistling():
                    # Dog hears human whistling
                    self.dog_hears_whistle = True
                    
                    # Move towards human
                    # Calc movement direction
                    current_position = self.get_position()
                    human_position = human.get_position()
                    dx = 1 if human_position[0] > current_position[0] else -1
                    dy = 1 if human_position[1] > current_position[1] else -1

                    new_position = (current_position[0] + dx, current_position[1] + dy)
                    self.set_position(new_position)
                if not self.is_bored() and not human.is_whistling():
                    self.dog_hears_whistle = False
                
                if distance_to_human <= 5 and human.get_relation() == "Friend":
                    if self.is_bored():
                        self.reset_boredom()
                        print(f"{self.get_name()} played with {human.get_relation()}: {human.get_name()}")
                        self.set_energy(self.get_energy() - 10)
                if distance_to_human <= 20 and human.get_relation() == "Stranger":
                    self.bark()
                    stranger_nearby = True 

            for squirrel in squirrels:
                distance_to_squirrel = distance(self.get_position(), squirrel.get_position())
                if distance_to_squirrel <= 10:
                    self.bark()
                    squirrels_nearby = True

            if not stranger_nearby and not squirrels_nearby:  # If no strangers are nearby, stop barking
                self.stop_barking()



    #############################################################
    #                       Other Methods                       #
    #############################################################

    # Function which allows the dog to move
    def move(self, season, humans, squirrels):

        energy_cost = 0.001
        valid_moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

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
        
        # Update the position
        self.position = (new_x, new_y)

        self.set_energy(self.get_energy() - energy_cost)

        # Increment inactive_steps if the dog doesn't interact with anything
        self.inactive_steps += 1

        self.update_energy(season)   # Energy decay

        self.detect_surrounding(humans, squirrels, False) # Detect Humans and Squirrels Normally




    # Function which plots the dog on the map
    def plot_me(self ,ax, LIMITS):
        fpos = flip_coords(self.position, LIMITS)
        patch = pat.Circle(fpos, radius=1, color=self.colour1)
        ax.add_patch(patch)
        patch = pat.Ellipse((fpos[0]-0.9, fpos[1]-0.3), height=1.5, width=0.3, color=self.colour2)
        ax.add_patch(patch)
        patch = pat.Ellipse((fpos[0]+0.9, fpos[1]-0.3), height=1.5, width=0.3, color=self.colour2)
        ax.add_patch(patch)
        #annotations
        ax.text(fpos[0], fpos[1] + 4, r"$\bf{" + self.name + "}$", ha='center', fontsize=9, color=self.colour2)
    
        # Add indicator if the dog is bored
        if self.is_bored():
            ax.text(fpos[0], fpos[1] + 8, "Bored!", ha='center', fontsize=9, color='red')

        # Barking indicator
        if self.is_barking():
            ax.text(fpos[0], fpos[1] - 4, "Woof! Woof!", ha='center', fontsize = 9, color='red', fontweight='bold')

        # Hearing the whistle
        if self.dog_hears_whistle:
            ax.text(fpos[0], fpos[1] - 4, "!!!", ha='center', fontsize = 9, color='red', fontweight='bold')

    # Resets the boredom status    
    def reset_boredom(self):
        self.inactive_steps = 0

    # Accessors
    def get_colour(self):
        return self.colour

    def get_energy(self):
        return self.energy
    
    def get_position(self):
        return self.position
    
    def get_has_toy(self):
        return self.holding_toy
    
    def has_toy(self):
        return self.holding_toy is not None

    def is_bored(self):
        # Dog is bored if it hasn't done anything for specific number of time steps
        return self.inactive_steps >= 80
    
    def is_hungry(self):
        return self.energy <= 30


    # Mutators
    def set_colour(self, new_colour):
        self.colour = new_colour

    def set_energy(self, new_energy):
        self.energy = new_energy

    def set_position(self, new_position):
        self.position = new_position


    def update_energy(self, season):
        if season == "Winter":
            self.energy -= 3 * self.energy_decay_rate
        else:
            self.energy -= self.energy_decay_rate

        self.energy = max(0, min(self.energy, self.max_energy))

    