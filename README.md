# Tookits for An Iterative Weighting Method to Apply the ISR Correction
Maybe you have noticed that a new method for ISR iteration has been proposed by Liangliang Wang (llwang@ihep.ac.cn) and Wenyu Sun (sunwenyu@ihep.ac.cn), recently. After the check doing by Tong Liu (liutong2016@ihep.ac.cn) (MC generation examples could be found in example/(the energy threshould should be the same as that of sum of final states, and the start energy point at xs_user.dat should be the threshould), tagISR should not be opened and tagFSR should be opened), this method has been proved correct and is very time saving. This repository provides a relative general package for user to use this method. The structure of codes are inspired by TF-PWA (https://github.com/jiangyi15/tf-pwa) written by Yi Jiang and recieve lots of help from Lianjin Wu (wulj@ihep.ac.cn), which is very appreciated. If you are not familiar with GitHub operations, you can copy the codes from /besfs/users/jingmq/weighted-isr, if the storage path changes, the newest path will be updated here, also, all the changes will be updated to this repository in GitHub.

## Install

> cd [Your Work Directory]

> git clone https://github.com/zhixing1996/weighted-isr.git

## Setup

Python Version: python3.x

## Changes you need to do

> config.conf: configuration file, user's changes will happen in here mostly.

1. [init]: initial information.
    1. samples: samples you want to deal with;
    2. isr: isr correction factor calculated by the flat dressed cross section line-shape;
    3. truth: m_truth in MC truth;
    4. event: m_truth in samples after selection (wrong combination events have been removed)
    5. samples_info: corresponding samples information.
    6. P.S.: how to get m_truth?
        1. KKMC: for m_truth, the FSR photons other than those from psi(4260) (Particle ID: 9030443) have to be added;
        2. ConExc: for m_truth, can be recognized as gamma* (Particle ID: 90022);

        There is an example code:
        ```
        from ROOT import TLorentzVector
        mc_truth = TLorentzVector(0, 0, 0, 0)
        all_truth = TLorentzVector(0, 0, 0, 0)
        is_psi4260_gen = False
        is_gamma_star_gen = False
        for i in xrange(t_in.indexmc):
            if t_in.pdgid[i] == 9030443: is_psi4260_gen = True # for KKMC
            if t_in.pdgid[i] == 90022: is_gamma_star_gen = True # for ConExc
        tag_psi4260 = False
        for i in xrange(t_in.indexmc):
            if is_psi4260_gen == True:
                if t_in.pdgid[i] == 9030443:
                    tag_psi4260 = True
                    mc_truth.SetPxPyPzE(t_in.p4_mc_all[i*4 + 0], t_in.p4_mc_all[i*4 + 1], t_in.p4_mc_all[i*4 + 2], t_in.p4_mc_all[i*4 + 3])
                    all_truth += mc_truth
                if t_in.pdgid[i] == -22 and tag_psi4260 == False:
                    mc_truth.SetPxPyPzE(t_in.p4_mc_all[i*4 + 0], t_in.p4_mc_all[i*4 + 1], t_in.p4_mc_all[i*4 + 2], t_in.p4_mc_all[i*4 + 3])
                    all_truth += mc_truth
            if is_gamma_star_gen == True:
                if t_in.pdgid[i] == 90022: mc_truth.SetPxPyPzE(t_in.p4_mc_all[i*4 + 0], t_in.p4_mc_all[i*4 + 1], t_in.p4_mc_all[i*4 + 2], t_in.p4_mc_all[i*4 + 3])
        m_m_truthall[0] = all_truth.M()
        ```

2. [weight]:
    1. func_params: line-shape function parameters.

> weighted_isr/config_loader/line_shape.py: line-shape function parameters.

## Execute

> cd [Your Work Directory]/weighted-isr

> python3 weight.py [--config config.conf]

## For developers 
 
- Fork the code with your personal github ID. See [details](https://help.github.com/articles/fork-a-repo/)
 
> git clone https://github.com/zhixing1996/weighted_isr.git
 
- Make your change, commit and push
 
> git commit -a -m "Added feature A, B, C"
 
> git push
 
- Make a pull request. See [details](https://help.github.com/articles/using-pull-requests/)
 
## Some styles to follow 
- Minimize the number of main codes
- Keep functions length less than one screen
- Seperate hard-coded cuts into script file
- Use pull-request mode on git 
- Document well the high-level bash file for work flow 