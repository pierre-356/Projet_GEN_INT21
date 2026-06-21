import lamps.py
import math


#calcule la distance entre les points de coordonnées (x1, y1) et (x2, y2)
def distance(x1, y1, x2, y2):
    d_carre = (x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)
    return math.sqrt(d_carre)


def scalaire(x1, y1, x2, y2):
    return (x1*x2+y1*y2)





def taux(lampe, x, y):
    x_lampe = lampe.x
    y_lampe = lampe.y
    puiss = lampe.puissance
    theta1_lampe = lampe.theta1
    theta2_lampe = lampe.theta2
    # Calcul de l'angle entre la lampe et le point (x, y)
    dx = x - x_lampe
    dy = y - y_lampe
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad) % 360  # Normalisation entre 0 et 360°

    # Détermination de la zone d'intérêt
    theta_min = min(theta1_lampe, theta2_lampe)
    theta_max = max(theta1_lampe, theta2_lampe)

    # Cas où la zone d'intérêt traverse 0° (ex: 350° à 10°)
    if theta_max - theta_min > 180:
        # Si l'angle est dans la zone [theta_min, 360°] ou [0°, theta_max]
        in_zone = (angle_deg >= theta_min) or (angle_deg <= theta_max)
    else:
        # Sinon, vérifie si l'angle est entre theta_min et theta_max
        in_zone = theta_min <= angle_deg <= theta_max

    if not in_zone:
        return 0.0

    # Calcul du centre de la zone d'intérêt
    centre = (theta1_lampe + theta2_lampe) / 2
    if centre > 180:
        centre -= 360

    # Calcul de la distance angulaire entre l'angle et le centre
    distance_au_centre = abs(angle_deg - centre)
    distance_au_centre = min(distance_au_centre, 360 - distance_au_centre)

    # Calcul de la largeur de la zone d'intérêt
    largeur_zone = abs(theta2_lampe - theta1_lampe)
    if largeur_zone > 180:
        largeur_zone = 360 - largeur_zone

    # Calcul de la valeur affine (1 au centre, 0 aux bords)
    if largeur_zone == 0:
        return 1.0  # Cas où la zone est un point

    # Normalisation de la distance pour obtenir une valeur entre 0 et 1
    valeur = 1 - (distance_au_centre / (largeur_zone / 2))
    return max(0.0, min(1.0, valeur))


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

    eclairement_angle = taux(lampe, x, y)
    
    return eclairement_distance*eclairement_angle