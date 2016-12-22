import pygame
import random
import math

from addVectors import addVectors

background_colour = (144,238,144)
(width, height) = (400, 400)
massAir = 0.2
elasticity = 0.75
gravity = (math.pi/2, 0.002)

def getParticle(particles, x, y):
    for i in particles:
        if math.hypot(i.x - x, i.y - y)<= i.radius:
            return i
    return None


def ifParticlesCollide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.radius + p2.radius:
        normalAngle = math.atan2(dy,dx)
        tangentAngle = 0.5 * math.pi - normalAngle

        #angle1 = math.pi+ 2*normalAngle - p1.angle
        #angle2 = math.pi+ 2*normalAngle - p2.angle
        #speed1 = p2.speed*elasticity
        #speed2 = p1.speed*elasticity

        #(p1.angle, p1.speed) = (angle1, speed1)
        #(p2.angle, p2.speed) = (angle2, speed2)
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (normalAngle, 2*p2.speed*p2.mass/total_mass))
        (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (normalAngle+math.pi, 2*p1.speed*p1.mass/total_mass))
        p1.speed *= elasticity
        p2.speed *= elasticity
        overlap = 0.5*(p1.radius + p2.radius - dist+1)
        p1.x += math.cos(normalAngle)*overlap
        p1.y += math.sin(normalAngle)*overlap
        p2.x -= math.cos(normalAngle)*overlap
        p2.y -= math.sin(normalAngle)*overlap


class Particle():
    def __init__(self, (x, y), radius, mass=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = (255, 255, 255)
        self.thickness = 0
        self.speed = 0
        self.mass = mass
        self.drag = (self.mass/(self.mass + massAir)) ** self.radius
        
        self.angle = 0 #the angle being measured in clockwise direction from +X. (remember +Y is downwards)

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius, self.thickness)

    def move(self):
        #(self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self):
        #we'll just change the angle using simple geometry
        if (self.x + self.radius) > width:
            self.x = 2*(width - self.radius) - self.x
            self.angle = math.pi - self.angle
            self.speed *= elasticity
        elif (self.y + self.radius) > height:
            self.y = 2*(height - self.radius) - self.y
            self.angle*=-1
            self.speed *= elasticity
        elif self.x < self.radius:
            self.x = 2*self.radius - self.x
            self.angle = math.pi - self.angle
            self.speed *= elasticity
        elif self.y < self.radius:
            self.y = 2*self.radius - self.y
            self.angle *=-1
            self.speed *= elasticity

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Physics Simulation')

nParticles = 5
PARTICLES = []

for n in range(nParticles):
    radius = random.randint(10, 20)
    density = random.randint(1, 20)
    x = random.randint(radius, width-radius)
    y = random.randint(radius, height-radius)
    particle = Particle((x, y), radius, density*radius**2)
    particle.speed = random.random()
    particle.angle = random.uniform(0, 2 * math.pi)
    particle.colour = (200-density*10, 200-density*10, 255)
    PARTICLES.append(particle)


selectedParticle = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            (xCoordMouse, yCoordMouse) = pygame.mouse.get_pos()
            selectedParticle =  getParticle(PARTICLES, xCoordMouse, yCoordMouse)
        elif event.type == pygame.MOUSEBUTTONUP:
            selectedParticle = None
        elif event.type == pygame.QUIT:
            pygame.quit()
            break

    if (selectedParticle):
        (xCoordMouse, yCoordMouse) = pygame.mouse.get_pos()
        dx = xCoordMouse - selectedParticle.x
        dy = yCoordMouse - selectedParticle.y
        selectedParticle.angle = math.atan2(dy, dx) 
        selectedParticle.speed = math.hypot(dy, dx) * 0.1 #not moving the mouse means speed = 0, particle doesnt move

    screen.fill(background_colour)

    for i, particle in enumerate(PARTICLES):
        particle.move()
        particle.bounce()
        for p in PARTICLES[i+1:]:
            ifParticlesCollide(particle, p)
        particle.display()

    pygame.display.flip()
