# Function to evaluate the "lamp" problem, where we try to place round-shaped lamps to cover a square space
# by Thomas Chabin, Evelyne Lutton, Alberto Tonda, 2018 <alberto.tonda@gmail.com>

import math
import matplotlib.pyplot as plt
import numpy as np
import sys
from random import Random
import time

from matplotlib.patches import Circle, Rectangle


@dataclass
class Ind:
	x: float
	y: float
	puissance: float
	theta1: float
	theta2: float

# parametre de l'algo genetique
mu = 0.3
lbda = 0.7
Pc = 0.3
Pm = 1-Pc
pas_arret = 4 # difference entre 2 iterations pour valider la convergence

# parametre de l'aleatoire
delta_xy = 0.2
delta_puiss = 0.2
delta_theta = 0.2

# parametres de l'environnement
# sides of the square, [width, height]
square = [1, 1]


def evaluateLamps(lamps, radius, square, visualize=False) :
	
	globalFitness = 0.0
	individualFitness = [0] * len(lamps)
	
	# this is a very rough discretization of the space
	discretization = 100 # TODO lower discretization here to speed up computation, increase for increased precision
	discretizationStep = square[0] / discretization
	totalArea = square[0] * discretization * square[1] * discretization
	
	# compute coverage of the square, going step by step
	coverage = 0.0
	overlap = 0.0
	
	for x in np.arange(0.0, square[0], discretizationStep) :
		for y in np.arange(0.0, square[1], discretizationStep) :
			coveredByLamps = 0
			for l in range(0, len(lamps)) :
				
				lamp = lamps[l]

				# if the distance between the point and the center of any lamp is less than
				# the radius of the lamps, then the point is lightened up!
				distance = math.sqrt( math.pow(lamp[0] - x, 2) + math.pow(lamp[1] - y, 2) )
				if distance <= radius : 
					coveredByLamps += 1
					individualFitness[l] += 1
			
			# now, if the point is covered by at least one lamp, the global fitness increases 
			if coveredByLamps > 0 : coverage += 1
			# but if it is covered by two or more, there's a 'waste' of light here, an overlap
			if coveredByLamps > 1 : overlap += 1
	
	# the global fitness can be computed in different ways
	globalFitness = coverage / totalArea # just as total coverage by all lamps
	#globalFitness = (coverage - overlap) / totalArea # or maybe you'd like to also minimize overlap!
	
	# if the flag "visualize" is true, let's plot the situation
	if visualize :
		
		figure = plt.figure()
		ax = figure.add_subplot(111, aspect='equal')
		
		# matplotlib needs a list of "patches", polygons that it is going to render
		for l in lamps :
			ax.add_patch( Circle( (l[0],l[1]), radius=radius, color='b', alpha=0.4) )
		ax.add_patch( Rectangle( (0,0), square[0], square[1], color='w', alpha=0.4 ) )
		
		ax.set_title("Lamp coverage of the arena (fitness %.2f)" % globalFitness)
		plt.show()
		plt.close(figure)
	
	return globalFitness

def mutation1(lamp, gener) :
	"""
	fais muter chaque attributs les un apres les autres
	"""
	# les coordonnees
	x = min (square[0], max (0, gener.uniform(1-delta_xy, 1+delta_xy)*lamp.x))
	lamp.x = x
	y = min (square[1], max (0, gener.uniform(1-delta_xy, 1+delta_xy)*lamp.y))
	lamp.y = y

	# puissance
	lamp.puissance = max (0, gener.uniform(1-delta_puiss, 1+delta_puiss)*lamp.puissance)

	# theta
	lamp.theta1 = min (360, max (0, gener.uniform(1-delta_theta, 1+delta_theta)*lamp.theta1))
	lamp.theta2 = min (360, max (lamp.theta1, gener.uniform(1-delta_theta, 1+delta_theta)*lamp.theta2))


def mutation1(lamp, gener) :
	"""
	choisis un attribut a muter
	"""
	attribut = gener.randint(0, 3)
	match attribut :
		case 0 :
			lamp.x = min (square[0], max (0, gener.uniform(1-delta_xy, 1+delta_xy)*lamp.x))
			lamp.y = min (square[1], max (0, gener.uniform(1-delta_xy, 1+delta_xy)*lamp.y))
		case 1 :
			lamp.puissance = max (0, gener.uniform(1-delta_puiss, 1+delta_puiss)*lamp.puissance)
		case 2 :
			lamp.theta1 = min (360, max (0, gener.uniform(1-delta_theta, 1+delta_theta)*lamp.theta1))
			lamp.theta2 = min (360, max (lamp.theta1, gener.uniform(1-delta_theta, 1+delta_theta)*lamp.theta2))

def appliquerEvolution(lamps) :
	fit = evaluateLamps(lamps)
	# premiere iteration
	"""
	mutation
	croisement
	selection
	"""
	tmp = evaluateLamps(lamps)
	delta = math.abs(tmp - fit)
	fit = tmp
	while(delta > pas_arret) :
		"""
		mutation
		croisement
		selection
		"""
		tmp = evaluateLamps(lamps)
		delta = math.abs(tmp - fit)
		fit = tmp
	return



# this main is just here to try the function, and give you an idea of how it works
def main() :

	generator = Random()
	generator.seed(time.time())
	
	# sides of the square, [width, height]
	square = [1, 1]
	
	# radius of the lamps
	radius = 0.3
	
	# coordinates of the lamps [ [x1,y1], [x2,y2], [x3,y4], ... ]
	lamps = [ [0.3,0.3], [0.3,0.7], [0.7,0.3], [0.7,0.7] ]
	
	# calling the function; the argument "visualize=True" makes it plot the current situation
	fitness = evaluateLamps(lamps, radius, square, visualize=True)
	
	return

if __name__ == "__main__" :
	sys.exit( main() )
