'''
helper.py: Utility functions for the Snoopy Simulation
'''

import math

def flip_coords(position, LIMITS):
    """
    Flips the map coordinates.
    
    Args:
        position (tuple): Original x,y coordinates
        LIMITS (tuple): Map limits
        
    Returns:
        tuple: Flipped coordinates
    """
    return (position[1], position[0])

def distance(point1, point2):
    """
    Calculates the Euclidean distance between two points.
    
    Args:
        point1 (tuple): First point (x, y)
        point2 (tuple): Second point (x, y)
        
    Returns:
        float: Distance between the two points
    """
    return math.sqrt(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))