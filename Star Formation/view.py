import pygame
import modelMechanics
import random

(width, height) = (400, 400)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star formation')

universe = modelMechanics.Simulation((width, height))
universe.colour = (0,0,0)
universe.addFunctions(['move', 'attract', 'combine'])

def calculateRadius(mass):
    return 0.5 * mass ** (0.5)

for p in range(100):
    particle_mass = random.randint(1,4)
    particle_radius = calculateRadius(particle_mass)
    universe.insertParticles(mass=particle_mass, radius=particle_radius, speed=0, colour=(255,255,255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(universe.colour)
    universe.update()
    
    particles_to_remove = []
    for p in universe.particles:
        if 'collide_with' in p.__dict__:
            particles_to_remove.append(p.collide_with)
            p.radius = calculateRadius(p.mass)
            del p.__dict__['collide_with']

        if p.radius < 2:
            pygame.draw.rect(screen, p.colour, (int(p.x), int(p.y), 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), int(p.radius), 0)
    
    for p in particles_to_remove:
        if p in universe.particles:
            universe.particles.remove(p)

    pygame.display.flip()