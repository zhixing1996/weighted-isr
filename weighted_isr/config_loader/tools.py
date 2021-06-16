import os
import pickle
from .line_shape import line_shape

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

def cal_weight(m, params, ecms):
    weight = 0
    for mj in m:
        weight += line_shape(mj, params)/line_shape(ecms, params)
    return weight
