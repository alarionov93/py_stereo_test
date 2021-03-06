import math


class Sort_pnt_by_circle():
    """docstring for ."""

    def __init__(self, origin, refvec):
        self.origin = origin
        self.refvec = refvec
    def sort_pnt_by_circle(self, point):
        # Vector between point and the origin: v = p - o
        vector = [point[0]- self.origin[0], point[1]-self.origin[1]]
        # Length of vector: ||v||
        lenvector = math.hypot(vector[0], vector[1])
        # If length is zero there is no angle
        if lenvector == 0:
            return -math.pi, 0
        # Normalize vector: v/||v||
        normalized = [vector[0]/lenvector, vector[1]/lenvector]
        dotprod  = normalized[0]*self.refvec[0] + normalized[1]*self.refvec[1]     # x1*x2 + y1*y2
        diffprod = self.refvec[1]*normalized[0] - self.refvec[0]*normalized[1]     # x1*y2 - y1*x2
        angle = math.atan2(diffprod, dotprod)
        # Negative angles represent counter-clockwise angles so we need to subtract them
        # from 2*pi (360 degrees)
        if angle < 0:
            return 2*math.pi+angle, lenvector
        # I return first the angle because that's the primary sorting criterium
        # but if two vectors have the same angle then the shorter distance should come first.
        return angle, lenvector
