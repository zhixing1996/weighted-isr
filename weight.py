from weighted_isr.config_loader import ConfigLoader
import os
import sys
sys.dont_write_bytecode = True

def load_config(config_file = "config.conf"):
    return ConfigLoader(config_file)

def write_to_file(samples, isr, eff):
    if not os.path.exists("./results/"): os.makedirs("./results/")
    with open("./results/isr_eff.txt", "w") as f:
        f.write("sample\tisr\teff\n")
        for sample, ki, ke in zip(samples, isr, eff):
            f.write(str(sample) + "\t" + str(isr[ki]) + "\t" + str(eff[ke]) + "\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description = "Simple weight scripts")
    parser.add_argument("-c", "--config", default = "config.conf", dest = "config")
    args = parser.parse_args()
    config = load_config(args.config)
    write_to_file(config.samples, config.weight_isr(), config.weight_eff())

if __name__ == "__main__":
    main()
