import os
from .base_config import BaseConfig
from .tools import parse_file, load_pickle, cal_weight, sampling

class ConfigLoader(BaseConfig):
    """ class for loading config.conf """

    def __init__(self, file_name, share_dict = None):
        if share_dict is None:
            share_dict = {}
        super().__init__(file_name, share_dict)
        self.samples = [int(sample) for sample in self.config.get("init", "samples").split(",")]
        self.init_isr = parse_file(self.config.get("init", "isr"))
        os.system("rm -rf ./pickles")
        self.truth = [load_pickle(self.config.get("init", "truth").replace("sample", str(sample))) for sample in self.samples]
        self.event = [load_pickle(self.config.get("init", "event").replace("sample", str(sample))) for sample in self.samples]
        self.samples_info = parse_file(self.config.get("init", "samples_info"))
        self.func_params = [float(param) for param in self.config.get("weight", "func_params").split(",")]
        self.func_params_0 = [float(param) for param in self.config.get("weight", "func_params_0").split(",")]
        self.weight_truth = [cal_weight(m_truth, self.func_params, self.samples_info[sample][0], self.func_params_0) for sample, m_truth in zip(self.samples, self.truth)]
        self.weight_event = [cal_weight(m_event, self.func_params, self.samples_info[sample][0], self.func_params_0) for sample, m_event in zip(self.samples, self.event)]
        self.nrand = 0
        self.cov_params = []
        if self.config.get("sys", "switch") == 'on':
            self.nrand = int(self.config.get("sys", "nrand"))
            cov_params_temp = [float(cp) for cp in self.config.get("sys", "cov_params").split(",")]
            NP = len(self.func_params)
            cov_params = []
            for i in range(NP):
                temp = []
                for j in range(NP):
                    temp.append(cov_params_temp[j + i * NP])
                cov_params.append(temp)
            self.cov_params = cov_params

    def weight_isr(self):
        dic = {}
        for sample, weight in zip(self.samples, self.weight_truth): dic[sample] = self.init_isr[sample][0]*weight/self.samples_info[sample][1]
        return dic

    def weight_eff(self):
        dic = {}
        for sample, weight_truth, weight_event in zip(self.samples, self.weight_truth, self.weight_event): dic[sample] = weight_event/weight_truth
        return dic

    def input_sys_err(self):
        params_new = sampling(self.nrand, self.func_params, self.cov_params)
        eff_summary = {}
        isr_summary = {}
        print('-'*50)
        print('Input parameters:\n', self.func_params)
        for irand, params in enumerate(params_new):
            print('Parameters in {}th sampling:\n{}'.format(irand, params))
            weight_truth = [cal_weight(m_truth, params, self.samples_info[sample][0], self.func_params_0) for sample, m_truth in zip(self.samples, self.truth)]
            weight_event = [cal_weight(m_event, params, self.samples_info[sample][0], self.func_params_0) for sample, m_event in zip(self.samples, self.event)]
            eff = {}
            for sample, w_truth, w_event in zip(self.samples, weight_truth, weight_event): eff[sample] = w_event/w_truth
            eff_summary[irand] = eff
            isr = {}
            for sample, weight in zip(self.samples, weight_truth):
                isr[sample] = self.init_isr[sample][0]*weight/self.samples_info[sample][1]
            isr_summary[irand] = isr
        print('-'*50)
        return eff_summary, isr_summary
