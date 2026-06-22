from lamps import *
import math


#calcule la distance entre les points de coordonnées (x1, y1) et (x2, y2)
def distance(x1, y1, x2, y2):
    d_carre = (x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)
    return math.sqrt(d_carre)


def scalaire(x1, y1, x2, y2):
    return (x1*x2+y1*y2)



# Calcule le taux d'eclairement du point de coordonnées (x,y) par rapport à l'individu : lampe 
def taux_eclairement_unaire(lampe, x, y):
    x_lampe = lampe.x
    y_lampe = lampe.y
    puiss = lampe.puissance
    theta1 = lampe.theta1
    theta2 = lampe.theta2
    
    distance_centre = distance(x_lampe, y_lampe, x, y)
    eclairement_distance = 0
    if(distance_centre < puiss):
        eclairement_distance = (puiss-distance_centre)/puiss

    dx = x - x_lampe
    dy = y - y_lampe
    angle_rad = math.atan2(dy, dx)  # Angle en radians, entre -pi et pi
    angle = math.degrees(angle_rad) % 360  # Conversion en degrés, entre 0 et 360

    # Cas normal : theta1 <= theta2 (ex: 30° à 60°)
    if theta1 <= angle <= theta2:
        eclairement_angle = 1
    else:
        eclairement_angle = 0
    
    return eclairement_distance*eclairement_angle


#Calcule l'éclairement du point de coordonnées (x, y) pour toutes les lampes de lstLampe
def calcule_eclairement(lstLampe, x, y):
    eclairement_total = 0 
    for i in range(len(lstLampe)):
        eclairement_total += taux_eclairement_unaire(lstLampe[i], x, y)
        if(eclairement_total > 1):
            return 1
    return eclairement_total


def somme_puissance(lstLampe):
    somme = 0.0
    for i in range(len(lstLampe)):
        somme += lstLampe[i].puissance*lstLampe[i].puissance*(lstLampe[i].theta2-lstLampe[i].theta1)/360
    return somme