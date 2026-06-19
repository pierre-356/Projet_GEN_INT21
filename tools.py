import lamps.py
import math


#calcule la distance entre les points de coordonnées (x1, y1) et (x2, y2)
def distance(x1, y1, x2, y2):
    d_carre = (x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)
    return math.sqrt(d_carre)


# Calcule le taux d'eclairement du point de coordonnées (x,y) par rapport à l'individu : lampe 
def taux_eclairement(lampe, x, y):
    x_lampe = lampe.x
    y_lampe = lampe.y
    puiss = lampe.puissance
    theta1_lampe = lampe.theta1
    theta2_lampe = lampe.theta2
    
    distance_centre = distance(x_lampe, y_lampe, x, y)
    eclairement_distance = 0
    if(distance_centre < puiss):
        eclairement_distance = (puiss-distance_centre)/puiss
    
    eclairement_angle = 1
    if(theta2_lampe-theta1_lampe < 359):
        eclairement_angle = 
