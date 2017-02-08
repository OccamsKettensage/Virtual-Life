import sys
import random

try:
	POPULATION_PER_GENERATION = int(raw_input("Enter population size (preferably between 50 and 75): "))
except ValueError:
	print "Didn't enter a number. Choosing 50 as the population size"
	POPULATION_PER_GENERATION = 50

try:
	MUTATION_CHANCE = float(raw_input("Enter mutation probability (a number between 1 and 5 ): "))/100
except ValueError:
	print "Didn't enter a number. Choosing 1% mutation rate"
	MUTATION_CHANCE = 0.01


class Colour:

	def __init__(self, red_val, green_val, blue_val):
		self.red_val = red_val
		self.green_val = green_val
		self.blue_val = blue_val

class Gene:

	def __init__(self, max_size):
		self.max_size = max_size
		self.radius = random.uniform(1, 3)
		self.coordinates = [random.randint(0, max_size[0]), random.randint(0, max_size[1])]
		self.colour = Colour(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

	def mutate(self):
		mutation_type = random.choice(["radius", "coordinates", "colour"])
		magnitude = random.random()
		if mutation_type == "coordinates":
			new_X = int(self.coordinates[0] * random.choice([(1+magnitude), (1-magnitude)]))
			new_Y = int(self.coordinates[1]*  random.choice([(1+magnitude), (1-magnitude)]))

			self.coordinates = [new_X, new_Y]

		elif mutation_type == "radius":
			self.radius = self.radius * random.choice([(1+magnitude), (1-magnitude)])

		else:
			new_red_val = min(self.colour.red_val * (random.choice([(1+magnitude), (1-magnitude)])), 255)
			new_green_val = min(self.colour.green_val * (random.choice([(1+magnitude), (1-magnitude)])), 255)
			new_blue_val = min(self.colour.blue_val * (random.choice([(1+magnitude), (1-magnitude)])), 255)

			self.colour = Colour(new_red_val, new_green_val, new_blue_val)









