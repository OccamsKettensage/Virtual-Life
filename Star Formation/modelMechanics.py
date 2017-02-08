import math
import random

pi = math.pi
class Simulation:

	def __init__(self, (width, height)):
		self.width = width
		self.height = height

		self.particles = []
		self.colour = (144,238,144)

		self.massAir = 0.2
		self.elasticity = 0.75

		self.oneParticleFunctions = []
		self.twoParticleFunctions = []

		self.accelaration= (0,0)

		self.functions = {
			'move': (1, lambda particle: particle.move()),
			'drag': (1, lambda particle: particle.getDragged()),
			'bounce': (1, lambda particle: self.bounce(particle)),
			'accelerate': (1, lambda particle: particle.accelerate(self.accelaration)),
			'collide': (2, lambda p1, p2: ifParticlesCollide(p1, p2)),
			'combine': (2, lambda p1, p2: combine(p1, p2)),
			'attract': (2, lambda p1, p2: p1.attract(p2))
		}

	def addFunctions(self, arrOfFunctions):
		for function in arrOfFunctions:
			(nParticlesInvolved, f) = self.functions.get(function, (-1, None))
			if (nParticlesInvolved == 1):
				self.oneParticleFunctions.append(f)
			elif (nParticlesInvolved == 2):
				self.twoParticleFunctions.append(f)
			else:
				print "error in adding function"

	def insertParticles(self, n=1, **keywordArgs):
		for i in range(n):
			radius =  keywordArgs.get('radius', random.randint(10, 20))
			x = keywordArgs.get('x', random.uniform(radius, self.width-radius))
			y = keywordArgs.get('y', random.uniform(radius, self.height-radius))

			mass = keywordArgs.get('mass', random.randint(100, 1000))
			density = mass/(radius**2)
			p = Particle((x, y), radius, mass)
			p.speed = keywordArgs.get('speed', random.random())
			p.angle = keywordArgs.get('angle', random.uniform(0, 2*math.pi))

			p.colour = keywordArgs.get('colour', (200-density*10, 200-density*10, 255))
			p.drag = keywordArgs.get('drag', (p.mass/(p.mass + self.massAir)) ** p.radius)
			self.particles.append(p)

	def update(self):
		for i, p in enumerate(self.particles):
			for f1 in self.oneParticleFunctions:
				f1(p)
			for p2 in self.particles[i+1:]:
				for f2 in self.twoParticleFunctions:
					f2(p, p2)

	def bounce(self, p):
		if (p.x + p.radius) > self.width:
			p.x = 2*(self.width - p.radius) - p.x
			p.angle = math.pi - p.angle
			p.speed *= self.elasticity
		elif (p.y + p.radius) > self.height:
			p.y = 2*(self.height - p.radius) - p.y
			p.angle*=-1
			p.speed *= self.elasticity
		elif p.x < p.radius:
			p.x = 2*p.radius - p.x
			p.angle = math.pi - p.angle
			p.speed *= self.elasticity
		elif p.y < p.radius:
			p.y = 2*p.radius - p.y
			p.angle *=-1
			p.speed *= self.elasticity

	def getParticle(self, x, y):
		for p in self.particles:
			if (math.hypot(x - p.x, y - p.y) <= p.radius):
				return p
		return None

class Particle:
	def __init__(self, (x, y), radius, mass=1):
		self.x = x
		self.y = y
		self.radius = radius
		self.colour = (255, 255, 255)
		self.thickness = 0
		self.speed = 0
		self.mass = mass
		self.drag = 1
        
		self.angle = 0 #the angle being measured in clockwise direction from +X. (remember +Y is downwards)
		self.elasticity = 0.99
		self.accelaration = 0

	def move(self):
		#(self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
		self.x += math.cos(self.angle) * self.speed
		self.y += math.sin(self.angle) * self.speed
		self.speed *= self.drag

	def mouseSelectMove(self, cursorX, cursorY):
		xDiff = cursorX - self.x
		yDiff = cursorY - self.y

		self.angle = math.atan2(yDiff, xDiff)
		self.speed = math.hypot(xDiff, yDiff) * 0.1

	def getDragged(self):
		self.speed *=self.drag

	def accelerate(self, (angle, magitude)):
		(self.angle, self.speed) = addVectors((self.angle, self.speed), (angle, magitude))

	def attract(self, other):
		dx = (self.x - other.x)
		dy = (self.y - other.y)
		dist  = math.hypot(dx, dy)
		
		if dist < self.radius + other.radius:
			return True

		theta = math.atan2(dy, dx)
		force = 0.2 * self.mass * other.mass / dist**2
		self.accelerate((theta+math.pi, force/self.mass))
		other.accelerate((theta , force/other.mass))

def addVectors((angle1, magnitude1), (angle2, magnitude2)): #takes 2 vectors
	xComponent = magnitude1*math.cos(angle1) + magnitude2*math.cos(angle2)

	yComponent = magnitude1*math.sin(angle1) + magnitude2*math.sin(angle2)

	angle = 2*math.pi - math.atan2(-yComponent, xComponent)
	magitude = math.hypot(xComponent, yComponent)
	#print('angle mag', angle, magitude)
	return (angle, magitude)

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
		
		elasticity = (p1.elasticity + p2.elasticity)/2
		p1.speed *= elasticity
		p2.speed *= elasticity

		overlap = 0.5*(p1.radius + p2.radius - dist+1)

		p1.x += math.cos(normalAngle)*overlap
		p1.y += math.sin(normalAngle)*overlap
		p2.x -= math.cos(normalAngle)*overlap
		p2.y -= math.sin(normalAngle)*overlap

def combine(p1, p2):
	if math.hypot(p1.x - p2.x, p1.y - p2.y) < p1.radius + p2.radius:
		total_mass = p1.mass + p2.mass
		p1.x = (p1.x*p1.mass + p2.x*p2.mass)/total_mass
		p1.y = (p1.y*p1.mass + p2.y*p2.mass)/total_mass
		(p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*p1.mass/total_mass), (p2.angle, p2.speed*p2.mass/total_mass))
		p1.speed *= (p1.elasticity*p2.elasticity) #CHANGE THE PREVIOUS ONE TO THIS
		p1.mass += p2.mass
		p1.collide_with = p2