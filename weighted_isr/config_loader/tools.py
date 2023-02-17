import os
import pickle
from math import sqrt
from array import array
import random
from .line_shape import line_shape, line_shape_0

def parse_file(file_name):
    dic = {}
    try:
        with open(file_name, "r") as f:
            for line in f.readlines():
                if "#" in line: continue
                try:
                    fargs = list(map(float, line.strip().split()))
                    key, values = int(fargs[0]), []
                    for i in range(1, len(fargs)): values.append(fargs[i])
                    dic[key] = values
                except ValueError as e:
                    if "could not convert string to float" in str(e): pass
        return dic
    except FileNotFoundError:
        print("{} does not exist, please check!".format(file_name))
        exit()

def load_pickle(file_name):
    if not os.path.exists("./pickles/"): os.makedirs("./pickles/")
    pickle_name = './pickles/' + file_name.split('/')[-1].split('.')[0] + '.pickle'
    if os.path.isfile(pickle_name):
        with open(pickle_name, "rb") as f:
            return pickle.load(f)
    m_j = []
    with open(file_name, "r") as f:
        for line in f.readlines(): m_j.append(float(line.strip('\n')))
    with open(pickle_name, "wb") as f:
        pickle.dump(m_j, f, protocol = pickle.HIGHEST_PROTOCOL)
    return m_j

def cal_weight(m, params, ecms, params_0 = []):
    weight = 0
    for mj in m:
        weight += (line_shape(mj, params) * line_shape_0(ecms, params_0))/(line_shape(ecms, params) * line_shape_0(mj, params_0))
    return weight

def cov_gen(C, NP):
    z, x = array('f', NP*[0.]), array('f', NP*[0.])
    for i in range(NP):
        z[i] = random.gauss(0, 1)
    for i in range(NP):
        x[i] = 0
        for j in range(NP):
            if j > i: continue
            x[i] += C[i][j] * z[j]
    return x
    

def sqrt_matrix(V, NP):
    C = []
    for i in range(NP):
        tmp = []
        for j in range(NP):
            tmp.append(0)
        C.append(tmp)
    for i in range(NP):
        Ck = 0
        for j in range(NP):
            if j >=i: continue
            Ck += C[i][j] * C[i][j]
        C[i][i] = sqrt(abs(V[i][i] - Ck))
        for j in range(i + 1, NP):
            Ck = 0
            for k in range(NP):
                if k >= i: continue
                Ck += C[j][k] * C[i][k]
            C[j][i] = (V[j][i] - Ck)/C[i][i]
    return C

def sampling(Nrand, params, cov_params):
    NP = len(cov_params)
    sqrt_cov = sqrt_matrix(cov_params, NP)
    iloop = 0
    params_sample = []
    while iloop < Nrand:
        params_new = array('f', NP*[0.])
        params_new = cov_gen(sqrt_cov, NP)
        for i in range(NP):
            params_new[i] += params[i]
        params_sample.append(params_new)
        iloop += 1
    return params_sample
