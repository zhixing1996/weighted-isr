import os
from weighted_isr.config_loader.tools import line_shape

def gen_line_shape(m, params):
    if not os.path.exists("./line_shapes/"): os.makedirs("./line_shapes/")
    with open("./line_shapes/xs_user.dat", "w") as f:
        for mj in m: f.write(str(round(mj, 4)) + " " + str(abs(line_shape(mj, params))) + "\n")
