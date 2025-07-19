import os

def load_config(filename="config.txt"):
    config = {}
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    key, sep, value = line.strip().partition("=")
                    if sep:
                        config[key.strip()] = value.strip()
    return config
