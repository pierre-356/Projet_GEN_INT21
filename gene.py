from lamps import *
import math


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

def croisement (l1, l2) :
	

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