import sys
import random

import numpy

from PIL import Image, ImageDraw

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
			new_Y = int(self.coordinates[1] *  random.choice([(1+magnitude), (1-magnitude)]))

			self.coordinates = [new_X, new_Y]

		elif mutation_type == "radius":
			self.radius = self.radius * random.choice([(1+magnitude), (1-magnitude)])

		else:
			new_red_val = min(self.colour.red_val * (random.choice([(1+magnitude), (1-magnitude)])), 255)
			new_green_val = min(self.colour.green_val * (random.choice([(1+magnitude), (1-magnitude)])), 255)
			new_blue_val = min(self.colour.blue_val * (random.choice([(1+magnitude), (1-magnitude)])), 255)

			self.colour = Colour(new_red_val, new_green_val, new_blue_val)


class Organism:

	def __init__(self, size, n_genes):
		self.size = size
		self.genes = [Gene(size) for i in xrange(max(n_genes, 400))] #no more than 400 genes

	def mutate(self):
		for gene in self.genes:
			if random.random() < MUTATION_CHANCE:
				gene.mutate()

	def crossover(self, partner):

		offspring = Gene(self.genes.length)
		mid = this.genes.length/2

		for i in xrange(0, mid):
			offspring.genes[i] = self.genes[i]

		for j in xrange(mid, self.genes.length):
			offspring.genes[j] = self.genes[j]

		return offspring

	def draw(self):
		image = Image.new("RGB",self.size,(255,255,255))
		canvas = ImageDraw.Draw(image)

		for gene in self.genes:
			colour = (gene.colour.red_val,gene.colour.green_val,gene.colour.blue_val)
			canvas.ellipse([gene.coordinates[0]-(2*gene.radius),
							gene.coordinates[1]-(2*gene.radius),
							gene.coordinates[0]+(2*gene.radius),
							gene.coordinates[1]+(2*gene.radius)],
							outline=colour,fill=colour)

        return image

	def fitness(self, target):
		image = draw(self)

		raw_self = numpy.array(image, numpy.int16)
		raw_target = numpy.array(target, numpy.int16)

		delta = float(numpy.sum(numpy.abs(raw_self - raw_target)))

		return ((delta/255) * 100) / raw_self.size