from .base_config import BaseConfig
from .tools import parse_file, load_pickle, cal_weight
import numpy as np

class ConfigLoader(BaseConfig):
    """ class for loading config.conf """

    def __init__(self, file_name, share_dict = None):
        if share_dict is None:
            share_dict = {}
        super().__init__(file_name, share_dict)
        self.samples = [int(sample) for sample in self.config.get("init", "samples").split(",")]
        self.init_isr = parse_file(self.config.get("init", "isr"))
        self.truth = [load_pickle(self.config.get("init", "truth").replace("sample", str(sample))) for sample in self.samples]
        self.event = [load_pickle(self.config.get("init", "event").replace("sample", str(sample))) for sample in self.samples]
        self.samples_info = parse_file(self.config.get("init", "samples_info"))
        self.func_params = [float(param) for param in self.config.get("weight", "func_params").split(",")]
        self.weight_truth = [cal_weight(m_truth, self.func_params, self.samples_info[sample][0]) for sample, m_truth in zip(self.samples, self.truth)]
        self.weight_event = [cal_weight(m_event, self.func_params, self.samples_info[sample][0]) for sample, m_event in zip(self.samples, self.event)]

    def weight_isr(self):
        dic = {}
        for sample, weight in zip(self.samples, self.weight_truth): dic[sample] = self.init_isr[sample][0]*weight/self.samples_info[sample][1]
        return dic

    def weight_eff(self):
        dic = {}
        for sample, weight_truth, weight_event in zip(self.samples, self.weight_truth, self.weight_event): dic[sample] = weight_event/weight_truth
        return dic
