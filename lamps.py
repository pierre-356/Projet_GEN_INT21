# Function to evaluate the "lamp" problem, where we try to place round-shaped lamps to cover a square space
# by Thomas Chabin, Evelyne Lutton, Alberto Tonda, 2018 <alberto.tonda@gmail.com>

from tools import *
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

# parametre de l'algo genetique
mu = 10
lbda = 3
Pc = 0.3
Pm = 1-Pc
nb_it = 30

# parametre de l'aleatoire
delta_xy = 0.2
delta_puiss = 0.2
delta_theta = 0.2
nb_mut = 1


# parametres de l'environnement
# sides of the square, [width, height]
square = [1, 1]

def mutation1_uni(lamp, gener) :
	"""
	fais muter chaque attributs les un apres les autres
	"""
	# les coordonnees
	x_e = min (square[0], max (0, gener.uniform(1-delta_xy, 1+delta_xy)*lamp.x))
	y_e = min (square[1], max (0, gener.uniform(1-delta_xy, 1+delta_xy)*lamp.y))
	
	# puissance
	p = max (0, gener.uniform(1-delta_puiss, 1+delta_puiss)*lamp.puissance)

	# theta
	theta1_e = min (360, max (0, gener.uniform(1-delta_theta, 1+delta_theta)*lamp.theta1))
	theta2_e = min (360, max (theta1_e, gener.uniform(1-delta_theta, 1+delta_theta)*lamp.theta2))
	
	enfant = Ind(x=x_e, y=y_e, puissance=p, theta1=theta1_e, theta2=theta2_e)
	return enfant

def mutation2_uni(lamp, gener) :
	"""
	choisis un attribut a muter
	"""
	enfant = Ind(x=lamp.x, y=lamp.y, puissance=lamp.puissance, theta1=lamp.theta1, theta2=lamp.theta2)
	attribut = gener.randint(0, 2)
	match attribut :
		case 0 :
			enfant.x = min (square[0], max (0, gener.uniform(1-delta_xy, 1+delta_xy)*lamp.x))
			enfant.y = min (square[1], max (0, gener.uniform(1-delta_xy, 1+delta_xy)*lamp.y))
		case 1 :
			enfant.puissance = max (0, gener.uniform(1-delta_puiss, 1+delta_puiss)*lamp.puissance)
		case 2 :
			enfant.theta1 = min (360, max (0, gener.uniform(1-delta_theta, 1+delta_theta)*lamp.theta1))
			enfant.theta2 = min (360, max (lamp.theta1, gener.uniform(1-delta_theta, 1+delta_theta)*lamp.theta2))
	return enfant

def mutation1(lamps, gener) :
	"""
	en fait muter nb_mut
	renvoie le nouveau tableau de lamp
	"""
	nouveau = lamps.copy()
	for i in range (nb_mut) :
		choisi = gener.randint(0, len(nouveau)-1)
		nouveau[choisi] = mutation1_uni(lamps[choisi], gener)
	return nouveau

def mutation2(lamps, gener) :
	"""
	en fait muter nb_mut
	renvoie le nouveau tableau de lamp
	"""
	nouveau = lamps.copy()
	for i in range (nb_mut) :
		choisi = gener.randint(0, len(nouveau)-1)
		nouveau[choisi] = mutation2_uni(lamps[choisi], gener)
	return nouveau

def croisement1_uni (l1, l2, gener) :
	"""
	utilise la meme ponderation de moyenne pour tous les attributs
	"""
	poids = gener.uniform(0,1)
	x_e = poids*l1.x + (1-poids)*l2.x
	y_e = poids*l1.y + (1-poids)*l2.y
	p_e = poids*l1.puissance + (1-poids)*l2.puissance
	t1_e = poids*l1.theta1 + (1-poids)*l2.theta1
	t2_e = poids*l1.theta2 + (1-poids)*l2.theta2
	enfant = Ind(x=x_e, y=y_e, puissance=p_e, theta1=t1_e, theta2=t2_e)
	return enfant

def croisement2_uni (l1, l2, gener) :
	"""
	utilise une ponderation de moyenne differente pour chaques attributs
	"""
	poids = gener.uniform()
	x_e = poids*l1.x + (1-poids)*l2.x
	y_e = poids*l1.y + (1-poids)*l2.y
	poids = gener.uniform()
	p_e = poids*l1.puissance + (1-poids)*l2.puissance
	poids = gener.uniform()
	t1_e = poids*l1.theta1 + (1-poids)*l2.theta1
	t2_e = poids*l1.theta2 + (1-poids)*l2.theta2
	enfant = Ind(x=x_e, y=y_e, puissance=p_e, theta1=t1_e, theta2=t2_e)
	return enfant

def croisement1(lamps1, lamps2, gener) :
	"""
	prend a chaque fois le croisement entre 2 lampes
	"""
	nouveau = []
	for i in range(len(lamps1)) :
		nouveau.append(croisement1_uni(lamps1[i],lamps2[i], gener)) 
	return nouveau

def croisement2(lamps1, lamps2, gener) :
	"""&
	prend a chaque fois le croisement entre 2 lampes
	"""
	nouveau = []
	for i in range(len(lamps1)) :
		nouveau.append(croisement2_uni(lamps1[i],lamps2[i])) 
	return nouveau

def appliquerEvolution(pop, gener) :
    # premiere iteration

    for i in range(nb_it) :
        # les mutations
        mut = []
        for i in range(int(Pm*lbda)) :
            choisi = gener.randint(0, len(pop)-1)
            mut.append(mutation1(pop[choisi], gener))

        # croisements
        crois = []
        for i in range(lbda-int(Pm*lbda)) :
            parent1 = gener.randint(0, len(pop)-1)
            parent2 = gener.randint(0, len(pop)-1)
            while (parent1 == parent2) :
                parent2 = gener.randint(0, len(pop)-1)
                crois.append(croisement1(pop[parent1], pop[parent2], gener))
        pop = pop + mut + crois 
    
        # selection
        pop = sorted(pop, key = lambda x : evaluateLamps(x, square)) # trie
        pop = pop[0:lbda] # garde les meilleurs
        
    return pop[0] # retourne le meilleur



def evaluateLamps(lstLamps, square, visualize=False) :
	
	# this is a very rough discretization of the space
	discretization = 50 # TODO lower discretization here to speed up computation, increase for increased precision
	discretizationStep = square[0] / discretization
	totalArea = square[0] * discretization * square[1] * discretization

	# compute coverage of the square, going step by step
	somme_taux_eclairement = 0.0
	
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
	

	
	pop = []
	for i in range(mu):
		lamps = []
		for j in range(3):
			theta2 = generator.uniform(0,360)
			lamps.append(Ind(x=generator.uniform(0,1), y=generator.uniform(0,1), puissance=generator.uniform(0,1), theta1=generator.uniform(0,1)*theta2, theta2=theta2))
		pop.append(lamps)

	lamps = appliquerEvolution(pop, generator)
	
	print(lamps)
	
	return

if __name__ == "__main__" :
	sys.exit( main() )
