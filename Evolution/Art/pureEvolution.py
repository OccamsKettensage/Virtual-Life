import random
import numpy

from copy import deepcopy

from PIL import Image, ImageDraw

import multiprocessing


POPULATION_PER_GENERATION = 200
MUTATION_CHANCE = 0.01
N_GENES = 300

try:
    TARGET = Image.open("target.png")
except IOError:
    print "target.png must be present in current directory. Exiting"
    exit()


class Colour:

    def __init__(self, red_val, green_val, blue_val):
        self.red_val = red_val
        self.green_val = green_val
        self.blue_val = blue_val

#Genotype
class Gene:

    def __init__(self, max_size):
        self.max_size = max_size
        self.radius = random.uniform(2, 8)

        self.coordinates = [random.randint(0, max_size[0]),
                            random.randint(0, max_size[1])]

        self.colour = Colour(random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255))

    def mutate(self):
        mutation_type = random.choice(["radius", "coordinates", "colour"])
        magnitude = max(1, int(round(random.gauss(15, 4))))/100

        if mutation_type == "coordinates":
            new_X = max(0, random.randint(
                                    int(self.coordinates[0]*(1-magnitude)),
                                    int(self.coordinates[0]*(1+magnitude))))
            new_Y = max(0, random.randint(
                                    int(self.coordinates[1]*(1-magnitude)),
                                    int(self.coordinates[1]*(1+magnitude))))

            self.coordinates = [new_X, new_Y]

        elif mutation_type == "radius":
            self.radius = max(1, random.randint(
                                    int(self.radius*(1-magnitude)),
                                    int(self.radius*(1+magnitude))))

        else:
            new_red_val = min(max(0, random.randint(
                                    int(self.colour.red_val*(1-magnitude)),
                                    int(self.colour.red_val*(1+magnitude)))),
                              255)

            new_green_val = min(max(0, random.randint(
                                    int(self.colour.green_val*(1-magnitude)),
                                    int(self.colour.green_val*(1+magnitude)))),
                                255)
            new_blue_val = min(max(0, random.randint(
                                    int(self.colour.blue_val*(1-magnitude)),
                                    int(self.colour.blue_val*(1+magnitude)))),
                               255)

            self.colour = Colour(new_red_val, new_green_val, new_blue_val)

#Phenotype
class Organism:

    def __init__(self, size):
        self.size = size
        self.genes = [Gene(size) for i in xrange(N_GENES)]

    def mutate(self):
        for gene in self.genes:
            if random.random() > MUTATION_CHANCE:
                gene.mutate()
        if 0.3 < random.random():
            self.genes.append(Gene(self.size))
        if len(self.genes) > 0 and 0.2 < random.random():
            self.genes.remove(random.choice(self.genes))

    def crossover(self, partner):

        offspring = Organism(self.size, len(self.genes))

        for i in xrange(0, len(self.genes)):
            if random.random() < 0.5:
                offspring.genes[i] = self.genes[i]
            else:
                offspring.genes[i] = partner.genes[i]

        return offspring

    def draw(self):

        image = Image.new("RGB", self.size, (255, 255, 255))
        canvas = ImageDraw.Draw(image)

        for gene in self.genes:
            colour = (int(gene.colour.red_val),
                      int(gene.colour.green_val),
                      int(gene.colour.blue_val))

            canvas.ellipse([gene.coordinates[0]-(2*gene.radius),
                            gene.coordinates[1]-(2*gene.radius),
                            gene.coordinates[0]+(2*gene.radius),
                            gene.coordinates[1]+(2*gene.radius)],
                           outline=colour, fill=colour)

        return image

    def set_fitness(self, target):
        new = deepcopy(self)
        image = new.draw()

        raw_self = numpy.array(image, numpy.int16)
        raw_target = numpy.array(target, numpy.int16)

        delta = float(numpy.sum(numpy.abs(raw_self - raw_target)))

        #lower fitness is better
        self.fitness = (delta / 255.0 * 100) / raw_self.size


def FITNESS(organism_image, target):
    """
    not a method cuz need it in global scope for pickling
    see multiprocessing docs
    """

    raw_self = numpy.array(organism_image, numpy.int16)
    raw_target = numpy.array(target, numpy.int16)

    delta = numpy.sum(numpy.abs(raw_self - raw_target))
    return (delta / 255.0 * 100) / raw_self.size

def MUTATE(organism):
    copy_organism = deepcopy(organism)
    copy_organism.mutate()
    organism_image = copy_organism.draw()
    target = TARGET
    tuple1 =  (FITNESS(organism_image, target), copy_organism)
    return tuple1


def MUTATE_ALL(multi, organism, pop_per_gen):
    return multi.map(MUTATE, [organism] * (pop_per_gen -1) )


class Population:

    def __init__(self, target):
        self.population = [Organism(target.size, N_GENES) for i in xrange(POPULATION_PER_GENERATION)]
        self.mating_pool = []
        self.generations = 0
        self.max_fitness = 0

    def set_fitness(self, target):
        """
        pooling only helps when the N_GENES and pop_per_gen are big
        """
        multi = multiprocessing.Pool(multiprocessing.cpu_count())
        results = multi.map(FITNESS, self.population)
        for i in xrange(len(self.population)):
            self.population[i].fitness = results[i]

    def generate(self, target):
        """
        take 200 fittest members, and choose parents randomly
        could be the culprit behind premature convergence.
        """
        sorted_population = sorted(self.population, key=lambda (o): o.fitness)[:200]
        for i in xrange(len(self.population)):
            parent_A = random.choice(sorted_population)
            parent_B = random.choice(sorted_population)

            offspring = parent_A.crossover(parent_B)
            offspring.mutate()
            offspring.set_fitness(target)

            self.population[i] = offspring
        self.generations += 1

    def best_of_generation(self):
        curr_best = self.population[0]
        for organism in self.population:
            if organism.fitness < curr_best.fitness:
                curr_best = organism
        return curr_best

    def average_fitness(self):
        total_fitness = 0
        for organism in self.population:
            total_fitness += organism.fitness
        return total_fitness/len(self.population)


def start():
    n_generations = 0

    curr_best = Organism(TARGET.size)

    multi = multiprocessing.Pool(multiprocessing.cpu_count() - 1)

    while n_generations < 10000:
        print "on generation" + str(n_generations)
        if n_generations % 100 == 0: #save every 100th generation
            curr_best.draw().save(str(n_generations) + ".png")
            print "Saved best of generation " + str(n_generations)

        evolved_population = MUTATE_ALL(multi, curr_best, POPULATION_PER_GENERATION)
        evolved_population = sorted(evolved_population, key=lambda i: i[0])
        curr_best = evolved_population[0][1]
        print "curr best fitness", evolved_population[0][0]
        n_generations += 1


if __name__ == "__main__":
    print "Starting up. Sit back- this will take a while."
    start()
