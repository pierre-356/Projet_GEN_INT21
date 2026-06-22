import lamps.py
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
    theta1_lampe = lampe.theta1
    theta2_lampe = lampe.theta2
    
    distance_centre = distance(x_lampe, y_lampe, x, y)
    eclairement_distance = 0
    if(distance_centre < puiss):
        eclairement_distance = (puiss-distance_centre)/puiss

    eclairement_angle = 0
    if(puiss != 0 and eclairement_distance != 0):
        angle_max = (theta1_lampe+theta2_lampe)/2
        angle_max_rad = math.radians(angle_max)
        scal = scalaire(x-x_lampe, y-y_lampe, puiss*math.cos(angle_max_rad), puiss*math.sin(angle_max_rad))
        cos_angle_rad = scal/(puiss*distance_centre)
        angle_rad = math.acos(cos_angle_rad)
        angle = math.degrees(angle_rad)

        if(angle > theta1_lampe and angle < theta2_lampe):
            eclairement_angle = min((2/(theta2_lampe-theta1_lampe))*(angle-theta1_lampe), 2/(theta1_lampe-theta2_lampe)*(angle-theta2_lampe))
    
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
        somme += lstLampe[i].puiss*lstLampe[i].puiss
    return somme