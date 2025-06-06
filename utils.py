import math

def add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def sub(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def length(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def set_mag(v, mag):
    l = length(v)
    if l == 0:
        return (0, 0)
    return (v[0]/l * mag, v[1]/l * mag)

def from_angle(angle):
    return (math.cos(angle), math.sin(angle))

def heading(v):
    return math.atan2(v[1], v[0])

def constrain_angle(angle, target, max_diff):
    diff = angle - target
    while diff > math.pi:
        diff -= 2 * math.pi
    while diff < -math.pi:
        diff += 2 * math.pi
    if diff > max_diff:
        return target + max_diff
    elif diff < -max_diff:
        return target - max_diff
    else:
        return angle
