import unittest
import sys
import os

# Add src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.dog import Dog
from src.models.human import Human
from src.models.squirrel import Squirrel
from src.models.toy import Toy
from src.models.foodbowl import FoodBowl

class TestModels(unittest.TestCase):
    def test_move_towards_toy(self):
        dog = Dog("Billy", 5, "Brown/White", (0, 0))

        toy = Toy("Ball", (3, 4))


        dog.set_position((0, 0))
        toy.set_position((3, 4))

        dog.move_towards_toy(toy)

        # Check if dog moves towards the toy 1,1 in both x and y
        self.assertEqual(dog.get_position(), (1, 1))  

    def test_move(self):  
        # This test may fail because dog has option to stay in current position for the turn
        dog = Dog("Billy", 5, "Brown/White", (0, 0))
        dog.set_energy(50)

        dog.move("Summer", [], []) 

        # Checking if dog's position has been updated
        self.assertNotEqual(dog.get_position(), (0, 0))

    def test_update_energy_winter(self):
        dog = Dog("Billy", 5, "Brown/White", (0, 0))
        dog.set_energy(50)

        dog.update_energy("Winter")

        # Checking the energy level
        self.assertAlmostEqual(dog.get_energy(), 50 - 3 * dog.energy_decay_rate)  

    def test_update_energy_summer(self):
        dog = Dog("Billy", 5, "Brown/White", (0, 0))
        dog.set_energy(50)

        dog.update_energy("Summer")

        # Check the energy level
        self.assertAlmostEqual(dog.get_energy(), 50 - dog.energy_decay_rate) 

    def test_bark(self):
        dog = Dog("Billy", 3, "Red", (10, 10))

        dog.bark()
        # Check if energy has decreased
        self.assertLess(dog.get_energy(), 50)

    def test_eat(self):
        dog = Dog("Billy", 3, "Red", (10, 10))

        dog.energy = 30
        initial_energy = 30
    
        amount_to_eat = 20
        season = "Summer"

        dog.eat(amount_to_eat, season)

        # Check if energy has increased
        expected_energy = initial_energy + amount_to_eat
        self.assertEqual(dog.get_energy(), expected_energy)


    def test_move_towards_foodbowl(self):
        dog = Dog("Billy", 4, "Brown", (5, 5))

        foodbowl = FoodBowl((3, 3))

        dog.move_towards_foodbowl(foodbowl)

        # Move should move (2,2) towards the food bowl's direction
        self.assertEqual(dog.get_position(), (3, 3))

    def test_play_with_toy(self):
        dog = Dog("Billy", 3, "Black", (10, 10))

        toy = Toy("Ball", (12, 12))

        dog.set_energy(50)

        dog.play_with_toy(toy)

       
        expected_energy = 50 - 10
        self.assertEqual(dog.get_energy(), expected_energy)


        # Checking the dog's interaction with toys counter
        self.assertEqual(dog.interactions_with_toys, 1)

        # Checking if the toy has been added to the list of toys interacted with
        self.assertIn(toy.get_name(), dog.toys_interacted_with)

    def test_pick_up_toy(self):
        dog = Dog("Billy", 5, "Red", (15, 15))
        toy = Toy("Bone", (17, 17))
        toys = [Toy("Ball", (10, 10)), Toy("Stick", (12, 12)), toy, Toy("Rope", (20, 20))]

        dog.pick_up_toy(toy, toys)

        # Checking whether dog is holding the right toy
        self.assertEqual(dog.holding_toy, toy)

        # Checking the availability of the picked up toy
        self.assertFalse(toy.is_available())

        # Checking if toy has been removed from list of toys
        self.assertNotIn(toy, toys)

    def test_drop_toy(self):
        dog = Dog("Billy", 5, "Red", (15, 15))
        toy = Toy("Bone", (17, 17))

        dog.holding_toy = toy

        toys = [Toy("Ball", (10, 10)), Toy("Stick", (12, 12)), Toy("Rope", (20, 20))]

        dog.drop_toy(toys)

        # Dog should no longer hold the toy
        self.assertIsNone(dog.holding_toy)

        # The toy should now be available
        self.assertTrue(toy.is_available())

        # The toy should be back in to the list of toys
        self.assertIn(toy, toys)

    def test_bury_toy(self):
        dog = Dog("Billy", 5, "Red", (15, 15))
        toy = Toy("Bone", (17, 17))

        dog.holding_toy = toy

        toys = [Toy("Ball", (10, 10)), Toy("Stick", (12, 12)), Toy("Rope", (20, 20))]

        dog.bury_toy(toys)

        # Dog should not be holding any toy
        self.assertIsNone(dog.holding_toy)

        # Toy should be marked as buried
        self.assertTrue(toy.is_buried())

        # Buried toy should have the dog's name
        self.assertEqual(toy.get_buried_by(), dog.get_name())

        # Dog should have less energy after burying toy
        self.assertLess(dog.get_energy(), 100)


    def test_dig_up_toy(self):
        dog = Dog("Billy", 6, "Red", (20, 20))

        buried_toy = Toy("Squeaky Toy", (22, 22))
        buried_toy.set_buried(True)
        buried_toy.set_buried_by("Richard")  # Buried by another dog

        toys = [buried_toy, Toy("Frisbee", (18, 18)), Toy("Chew Toy", (25, 25))]

        dog.dig_up_toy(buried_toy, toys)

        # The dog should hold the same toy that has been dug up
        self.assertEqual(dog.holding_toy, buried_toy)

        # The dug up toy should not be available for other dogs
        self.assertFalse(buried_toy.is_available())

        # The dug up toy should not be marked as buried
        self.assertFalse(buried_toy.is_buried())

        # The dog's energy should be reduced after digging up toy
        self.assertLess(dog.get_energy(), 100)


    def test_detect_surrounding_squirrel(self):
        squirrel = Squirrel("Squire", (49, 49))

        barking_dog_position = (48, 48)
        barking_dog = Dog("Billy", 5, "Black", barking_dog_position)
        barking_dog.start_barking()

        initial_position = squirrel.get_position()

        squirrel.detect_surrounding([barking_dog])

        # Squirrel should move away from the barking dog
        self.assertNotEqual(squirrel.get_position(), initial_position)


    def test_whistling(self):
        human = Human("John", "Friend", (50, 50))

        # Human should not be whistling by default
        self.assertFalse(human.is_whistling())

        human.start_whistling()

        # Human should whistle once the above method is called
        self.assertTrue(human.is_whistling())

        human.stop_whistling()

        # Humans should stop whisling once the above method is called
        self.assertFalse(human.is_whistling())

    def test_decrease_food(self):
        food_bowl = FoodBowl((10, 10))
        # food bowls have 100 units of food by default

        food_bowl.decrease_food(20)

        # Food level should be at 80 
        self.assertEqual(food_bowl.get_food_level(), 80)



    def test_interact(self):
        dog = Dog("Billy", 3, "Brown", (0, 0))
        toy = Toy("Ball", (5, 5))

        # Toy should be available by default
        self.assertTrue(toy.is_available())

        toy.interact(dog)

        # Toy should not be available after dog interaction
        self.assertFalse(toy.is_available())


if __name__ == '__main__':
    unittest.main()