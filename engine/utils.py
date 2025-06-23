import math

def normalize(v):
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length == 0:
        return [0, 0, 0]
    return [v[0] / length, v[1] / length, v[2] / length]

def reflect(incident, normal):
    dot = sum(i * n for i, n in zip(incident, normal))
    return [i - 2 * dot * n for i, n in zip(incident, normal)]