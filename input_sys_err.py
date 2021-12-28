from weighted_isr.config_loader import ConfigLoader
import os
import sys
sys.dont_write_bytecode = True

def load_config(config_file = "config.conf"):
    return ConfigLoader(config_file)

def write_to_file(samples, eff, isr):
    if not os.path.exists("./results/"): os.makedirs("./results/")
    for sample in samples:
        with open("./results/isr_eff_"+str(sample)+"_sys.txt", "w") as f:
            f.write("iloop\tisr\teff\n")
            for k_isr, k_eff in zip(isr, eff):
                f.write(str(k_isr) + "\t" + str(isr[k_isr][sample]) + "\t" + str(eff[k_eff][sample]) + "\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description = "Estimate systematic uncertainty stemmed from input line-shape")
    parser.add_argument("-c", "--config", default = "config.conf", dest = "config")
    args = parser.parse_args()
    config = load_config(args.config)
    eff, isr = config.input_sys_err()
    write_to_file(config.samples, eff, isr)

if __name__ == "__main__":
    main()
