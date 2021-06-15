import math

def line_shape(x, params):
    left = params[0] / x
    numerator = math.sqrt(12.0*math.pi*params[1]*params[2])
    denominator = complex(x*x - params[0]*params[0], params[0]*params[1])
    middle = numerator/denominator
    return left*middle
