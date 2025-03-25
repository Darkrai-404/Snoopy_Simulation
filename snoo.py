'''
snoo.py: The main file which houses the simulation loop.
The skeleton of this code was received as a part of practical test 3 in FoP Semester 1 2024
'''
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv, time, math
from dog import *
from squirrel import *
from human import *
from foodbowl import *

def collect_dog_data(dog_animals, timestep):
    dog_data = []   # Stores data for every dog
    for dog in dog_animals:
        percentage_buried = (dog.buried_toys / dog.interactions_with_toys) * 100 if dog.interactions_with_toys > 0 else 0
        percentage_dropped = (dog.dropped_toys / dog.interactions_with_toys) * 100 if dog.interactions_with_toys > 0 else 0
        intake_winter = dog.food_intake_winter
        intake_summer = dog.food_intake_summer

        dog_info = {
            "Name": dog.get_name(),
            "Timestep": timestep,
            "Toys_Interacted_With": ", ".join(dog.toys_interacted_with),
            "Times_Buried_Toy": dog.buried_toys,
            "Times_Dropped_Toy": dog.dropped_toys,
            "Percentage_Toy_Buried": f"{percentage_buried:.2f}",
            "Percentage_Toy_Dropped": f"{percentage_dropped:.2f}",
            "Dug_Up_Toy_Via_Smell": dog.dug_up_toy_via_smell,
            "Food_Intake_Winter" : f"{intake_winter:.2f}",
            "Food_Intake_Summer" : f"{intake_summer:.2f}"
        }
        dog_data.append(dog_info)
    return dog_data



def build_yard2(dims, season):
    plan = np.zeros(dims)
    # Slicing = [Y coordinates, X coordinates]

    # Season check
    if season == "Summer":
        grass_color = 5
    elif season == "Winter":
        grass_color = 10
    else:
        grass_color = 5  
    
    # Grass
    plan[:210, :] = grass_color
    
    # Fences
    plan[0, :] = 0 # top fence
    plan[:, 0] = 0  # left fence
    plan[:, -1] = 0 # right fence
    plan[150,:] = 1 # back yard / front yard fence
    plan[200,:] = 1 # bottom fence

    # Gate in the bottom fence
    plan[195:205, 85:105] = 2

    # House
    plan[60:160, 40:150] = 7
    
    # Path
    plan[210:220, :] = 10
    
    return plan
   

def plot_yard(ax, p):
    ax.imshow(p, cmap='nipy_spectral') # data as image


def take_dog_input():
    # Doc: https://dev.to/tlylt/filter-map-and-manipulating-csv-data-in-python-fnn
    # Doc: https://docs.python.org/3/library/csv.html 
    valid_file = False 
    dogs = []  # Empty list to store dogs
    while not valid_file:
        try:
            dogfile = input("Please input your dog csv (eg. dogs.csv): ")
            with open(dogfile, 'r', newline='') as dogs_csv:  
                reader = csv.DictReader(dogs_csv)
                for row in reader:
                    dogs.append({
                        "name": row["name"],
                        "age": int(row["age"]),
                        "colour": row["colour"],
                        "position": tuple(map(int, row["position"].split(',')))
                    })
            valid_file = True  
        
        except FileNotFoundError:
            print("\nFile is not found. Please check file name and format")
            print("File input example: <filename>.csv\n")

    return dogs


def take_squirrel_input():
    # Doc: https://dev.to/tlylt/filter-map-and-manipulating-csv-data-in-python-fnn
    # Doc: https://docs.python.org/3/library/csv.html 
    valid_file = False 
    squirrels = []  # Empty list to store squirrels
    while not valid_file:
        try:
            squirrel_file = input("Please input your squirrel csv (eg. squirrels.csv): ")
            with open(squirrel_file, 'r', newline='') as squirrels_csv:  
                reader = csv.DictReader(squirrels_csv)
                for row in reader:
                    squirrels.append({
                        "name": row["name"],
                        "position": tuple(map(int, row["position"].split(',')))
                    })
            valid_file = True  
        
        except FileNotFoundError:
            print("\nFile is not found. Please check file name and format")
            print("File input example: <filename>.csv\n")

    return squirrels

def take_human_input():
    # Doc: https://dev.to/tlylt/filter-map-and-manipulating-csv-data-in-python-fnn
    # Doc: https://docs.python.org/3/library/csv.html 
    valid_file = False 
    humans = []  # Empty list to store humans
    while not valid_file:
        try:
            human_file = input("Please input your human csv (eg. humans.csv): ")
            with open(human_file, 'r', newline='') as humans_csv:  
                reader = csv.DictReader(humans_csv)
                for row in reader:
                    humans.append({
                        "name": row["name"],
                        "relation": row["relation"],
                        "position": tuple(map(int, row["position"].split(',')))
                    })
            valid_file = True  
        
        except FileNotFoundError:
            print("\nFile is not found. Please check file name and format")
            print("File input example: <filename>.csv\n")

    return humans

def menu():
    with open("image.txt", "r") as file:
        art = file.read()
        print(art)

  
def take_foodbowl_input():
    # Doc: https://realpython.com/lessons/reading-csvs-pythons-csv-module/
    # Doc: https://docs.python.org/3/library/csv.html
    valid_file = False 
    food_bowls = []
    while not valid_file:
        try:
            food_bowl_file = input("Please input your food bowl csv (eg. foodbowls.csv): ")
            with open(food_bowl_file, 'r', newline='') as food_bowl_csv:
                reader = csv.DictReader(food_bowl_csv)
                for row in reader:
                    food_bowls.append(tuple(map(int, row["position"].split(','))))
            valid_file = True
        except FileNotFoundError:
            print("\nFile is not found. Please check file name and format")
            print("File input example: <filename>.csv\n")

    return food_bowls

def take_toy_input():
    # Doc: https://dev.to/tlylt/filter-map-and-manipulating-csv-data-in-python-fnn
    # Doc: https://docs.python.org/3/library/csv.html 
    valid_file = False 
    toys = []  # Empty list to store dogs
    while not valid_file:
        try:
            toy_file = input("Please input your toy csv (eg. toys.csv): ")
            with open(toy_file, 'r', newline='') as toys_csv:  
                reader = csv.DictReader(toys_csv)
                for row in reader:
                    toys.append({
                        "name": row["name"],
                        "position": tuple(map(int, row["position"].split(',')))
                    })
            valid_file = True  
        
        except FileNotFoundError:
            print("\nFile is not found. Please check file name and format")
            print("File input example: <filename>.csv\n")

    return toys

# Python formula to find distance between two points
# REF: https://www.w3resource.com/python-exercises/python-basic-exercise-40.php
def distance(point1, point2):
    return math.sqrt(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))

# Generate the legends
def generate_legend_text(dogs, food_bowls, toys):
    legend_text = r"$\bf{Dogs:}$" + "\n" 
    for dog in dogs:
        dog_info = fr"$\bf{{{dog.get_name()}}}$" + ":\n" + f"Energy - {dog.get_energy():.2f}\n"
        
        # Check if the dog is holding a toy
        if dog.holding_toy is not None:
            dog_info += f"Holding Toy: {dog.holding_toy.get_name()}\n"
        
        legend_text += dog_info

    legend_text += "\n" + r"$\bf{Food Bowls:}$" + "\n" 
    for bowl in food_bowls:
        legend_text += f"Capacity - {bowl.get_food_level():.2f}\n"

    legend_text += "\n" + r"$\bf{Toys:}$" + "\n"
    for toy in toys:
        if toy.is_buried():
            # If the toy is buried, adding the dog's name who buried it
            buried_by = toy.get_buried_by()
            if buried_by is not None:
                legend_text += fr"$\bf{{{toy.get_name()}}}$: Buried by {buried_by}"
            else:
                legend_text += fr"$\bf{{{toy.get_name()}}}$: Buried"
        else:
            # Checking the Availability status of unburied toys
            status = "Available" if toy.is_available() else "Not Available"
            legend_text += fr"$\bf{{{toy.get_name()}}}$: {status}"

        # New line after each toy. Latex form method. 
        legend_text += "\n"

    return legend_text


def main():
    size = (220,190) # map size
    season = "Winter"
    yard = build_yard2(size, season)
    menu()
    dogs_info = take_dog_input()
    squirrels_info = take_squirrel_input()
    humans_info = take_human_input()
    food_bowls_info = take_foodbowl_input()
    toys_info = take_toy_input()

    dog_animals = []
    squirrel_animals = []
    humans = []
    food_bowls = []
    toys = [] # global list of all toys


    # put all dogs in dog_animals list
    for dog in dogs_info:
        dog_animals.append(Dog(dog["name"], dog["age"], dog["colour"], dog["position"]))
   
    # put all squirrels in squirrel_animals list
    for squirrel in squirrels_info:
        squirrel_animals.append(Squirrel(squirrel["name"], squirrel["position"]))

    # put all humans in humans list
    for human in humans_info:
        humans.append(Human(human["name"], human["relation"], human["position"]))

    # put all food bowls in food_bowls list
    for position in food_bowls_info:
        food_bowls.append(FoodBowl(position))

    # Put all toys in toys list
    for toy in toys_info:
        toys.append(Toy(toy["name"], toy["position"])) 

    plt.ion() #interactive mode
    fig, axs = plt.subplots(figsize=(15,10))
    
    # Main simulation loop
    for timestep in range(3000):
        axs.clear()  # Clear the subplot

        # Collecting Simulation Data
        dog_data = collect_dog_data(dog_animals, timestep)
        # Writing the CSV output
        with open('Simulation_Analytics.csv', 'a', newline='') as csvfile:
            fieldnames = ['Name', 'Timestep', 'Toys_Interacted_With', 'Times_Buried_Toy', 'Times_Dropped_Toy', 'Percentage_Toy_Buried', 'Percentage_Toy_Dropped', 'Dug_Up_Toy_Via_Smell', 'Food_Intake_Winter', 'Food_Intake_Summer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Writing header for first timestep
            if timestep == 0:
                writer.writeheader()
            # Writing the rest of the data
            for dog_info in dog_data:
                writer.writerow(dog_info)


        # Movement of each Dog
        for d in dog_animals:  # Update each Dog's position

            # Hungry
            if d.is_hungry() and d.find_nearest_foodbowl(food_bowls) is not None:
                d.detect_surrounding(human, squirrel_animals, True) # Stop Listening to Whistle
                d.interact_with_food(food_bowls, season)

            elif d.is_bored():
                d.detect_surrounding(human, squirrel_animals, True) # Stop Listening to Whistle

                if d.get_has_toy():
                    if(random.random() < 0.5):
                        print(f"Dropping toy: {d.holding_toy.name}")
                        d.drop_toy(toys)
                    else:
                        print(f"Burying toy: {d.holding_toy.name}")
                        d.bury_toy(toys)
                elif d.find_nearest_toy(toys) is not None:
                    d.interact_with_toy(toys)  # New addition

                else:
                    d.move(season, humans, squirrel_animals)

            else:
                d.move(season, humans, squirrel_animals)
                
        # Movement of each Squirrel        
        if season == "Summer":
            for s in squirrel_animals: # Update each squirrel's position
                s.move(dog_animals)

        # Movement of each Human
        for h in humans: # Update each human's position
            h.move(dog_animals)
            if h.get_relation() == "Owner":
                empty_food_bowls = [bowl for bowl in food_bowls if bowl.is_empty()]
                if empty_food_bowls:
                    # Drop new foodbowl
                    new_foodbowl_location = h.get_position()
                    food_bowls.append(FoodBowl(new_foodbowl_location))
                    print(f"{h.get_name()} placed a new food bowl")

                    # Remove empty bowl from list
                    for bowl in empty_food_bowls:
                        food_bowls.remove(bowl)
                    print("Empty food bowl has been removed!")
        
        # Change season
        if timestep % 300 == 0:
            if season == "Summer":
                season = "Winter"
                print(f"Season changed to {season}")
                print(f"Squirrels are hibernating. . .")
                print(f"Dogs are burning more energy to maintain homeostasis. . .")

            else:
                season = "Summer"
                print(f"Season changed to {season}")
        yard = build_yard2(size, season)

        axs.set_title(f"Snoopy Simulator\nMinute #: {timestep}\nCurrent Season: {season}")

        plot_yard(axs, yard)  # Plot the yard grid

        
        for d in dog_animals: ## Plot each Dog on the yard grid
            d.plot_me(axs, size)

        if season == "Summer":
            for s in squirrel_animals:  ## Plot each squirrel on the yard grid
                s.plot_me(axs, size)

        for h in humans:  ## Plot each human on the yard grid
            h.plot_me(axs, size)

        for f in food_bowls: ## Plot each foodBowl on the yard grid
            f.plot_me(axs)

        for t in toys:  # New addition
            t.plot_me(axs, size)  # New addition


        # Add legend text for dogs on the left side
        dog_legend_text = generate_legend_text(dog_animals, food_bowls, toys)
        axs.text(-90, 50, dog_legend_text, verticalalignment='center', fontsize=10)

        fig.canvas.draw()             # this and following lines allow you                        
        fig.canvas.flush_events()    # to refresh plot in the same window
        time.sleep(.01)
        axs.clear()



if __name__ == "__main__":
    main()