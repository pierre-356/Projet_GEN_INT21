# Function to evaluate the "lamp" problem, where we try to place round-shaped lamps to cover a square space
# by Thomas Chabin, Evelyne Lutton, Alberto Tonda, 2018 <alberto.tonda@gmail.com>

from tools import *
from gene import *
import math
import matplotlib.pyplot as plt
import numpy as np
import sys
from random import Random
import time
from dataclasses import dataclass


from matplotlib.patches import Circle, Rectangle

@dataclass
class Ind:
	x: float
	y: float
	puissance: float
	theta1: float
	theta2: float



# parametres de l'environnement
# sides of the square, [width, height]
square = [1, 1]


def evaluateLamps(lstLamps, square, visualize=False) :
	
	# this is a very rough discretization of the space
	discretization = 50 # TODO lower discretization here to speed up computation, increase for increased precision
	discretizationStep = square[0] / discretization
	totalArea = square[0] * discretization * square[1] * discretization

	# compute coverage of the square, going step by step
	somme_taux_eclairement = 0.0

	print("mamacita")
	
	for x in np.arange(0.0, square[0], discretizationStep) :
		for y in np.arange(0.0, square[1], discretizationStep) :
			eclairement = calcule_eclairement(lstLamps, x, y)
			somme_taux_eclairement += 100*eclairement/discretization
	
	# the global fitness can be computed in different ways
	globalFitness = somme_taux_eclairement / somme_puissance(lstLamps) # just as total coverage by all lamps
	#globalFitness = (coverage - overlap) / totalArea # or maybe you'd like to also minimize overlap!

	# if the flag "visualize" is true, let's plot the situation
	if visualize :
		figure = plt.figure()
		ax = figure.add_subplot(111, aspect='equal')
		
		# matplotlib needs a list of "patches", polygons that it is going to render
		for l in lstLamps :
			ax.add_patch( Circle( (l.x,l.y), radius=0.01, color='b', alpha=0.4) )
		ax.add_patch( Rectangle( (0,0), square[0], square[1], color='w', alpha=0.4 ) )

		
        # Affichage des points de discrétisation avec une couleur interpolée
		for x in np.arange(0.0, square[0], discretizationStep) :
			for y in np.arange(0.0, square[1], discretizationStep) :
				e = calcule_eclairement(lstLamps, x, y)
            	# Interpolation linéaire entre blanc (0) et bleu pur (1)
				color = (abs(1 - e), abs(1 - e), 1)  # RGB : (R, V, B)
				rect = Rectangle(
                    (x, y),
                    discretizationStep,
                    discretizationStep,
                    color=color,
                    alpha=1.0,
                    linewidth=0
                )
				ax.add_patch(rect)

		print("goofy")

		ax.set_title(f"Lamp coverage of the arena (fitness {globalFitness:.2f})")
		plt.show()
		plt.close(figure)
	
	return globalFitness






# this main is just here to try the function, and give you an idea of how it works
def main() :

	generator = Random()
	generator.seed(time.time())
	
	# sides of the square, [width, height]
	square = [1, 1]
	
	
	# Création de 4 lampes dans le carré (0,1)
	lamps = [
    Ind(x=0.2, y=0.2, puissance=0.2, theta1=90.0, theta2=270.0),  # Lampe en bas à gauche
    Ind(x=0.8, y=0.2, puissance=0.3, theta1=0.0, theta2=180.0),  # Lampe en bas à droite
	]
	
	# calling the function; the argument "visualize=True" makes it plot the current situation
	fitness = evaluateLamps(lamps, square, visualize=True)
	
	return

if __name__ == "__main__" :
	sys.exit( main() )
