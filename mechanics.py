import pygame
import random
import math

background_colour = (144,238,144)
(width, height) = (800, 800)

class Particle():
    def __init__(self, (x, y), radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = (255, 255, 255)
        self.thickness = 0
        self.speed = 0.01
        self.angle = math.pi/2 #the angle being measured in clockwise direction from +X. (remember +Y is downwards)

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius, self.thickness)

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def bounce(self):
        #we'll just change the angle using simple geometry
        if (self.x + self.radius) > width:
            self.angle = math.pi - self.angle#self.angle += math.pi/2 
        elif (self.y + self.radius) > height:
            self.angle*=-1
        elif self.x < self.radius:
            self.angle = math.pi - self.angle
        elif self.y < self.radius:
            self.angle *=-1


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics Simulation')

number_of_particles = 10
my_particles = []

for n in range(number_of_particles):
    radius = random.randint(10, 20)
    x = random.randint(radius, width-radius)
    y = random.randint(radius, height-radius)
    particle = Particle((x, y), radius)
    particle.speed =  random.random()
    particle.angle =  random.uniform(0, math.pi/2)

    my_particles.append(particle)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    screen.fill(background_colour)

    for particle in my_particles:
        particle.move()
        particle.bounce()
        particle.display()

    pygame.display.flip()
