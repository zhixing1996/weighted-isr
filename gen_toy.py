from weighted_isr.applications import gen_line_shape
from weighted_isr.config_loader import ConfigLoader
import os
import sys
sys.dont_write_bytecode = True

def load_config(config_file = "config.conf"):
    return ConfigLoader(config_file)

def main():
    import argparse
    parser = argparse.ArgumentParser(description = "Simple gen toy line-shape scripts")
    parser.add_argument("-c", "--config", default = "config.conf", dest = "config")
    args = parser.parse_args()
    config = load_config(args.config)
    m = [4.0535 + i * 0.001 for i in range(945)]
    gen_line_shape(m, config.func_params)

if __name__ == "__main__":
    main()
