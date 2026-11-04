class ConfigError(Exception):
    pass


REQUIRED_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]


def to_int(key, value):
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"{key} must be a number, got '{value}'")


def to_coords(key, value):
    parts = value.split(",")
    if len(parts) != 2:
        raise ConfigError(f"{key} must look like x,y, got '{value}'")
    return (to_int(key, parts[0]), to_int(key, parts[1]))


def load_config(path):
    try:
        with open(path) as f:
            lines = f.readlines()
    except OSError:
        raise ConfigError(f"cannot open file '{path}'")

    config = {}
    for line in lines:
        line = line.strip()

        if line == "" or line.startswith("#"):
            continue

        if "=" not in line:
            raise ConfigError(f"missing '=' in line '{line}'")

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if key in config:
            raise ConfigError(f"key {key} appears twice")

        config[key] = value

    for key in REQUIRED_KEYS:
        if key not in config:
            raise ConfigError(f"missing key {key}")

    width = to_int("WIDTH", config["WIDTH"])
    height = to_int("HEIGHT", config["HEIGHT"])
    entry = to_coords("ENTRY", config["ENTRY"])
    exit = to_coords("EXIT", config["EXIT"])

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be greater than 0")

    for name, (x, y) in [("ENTRY", entry), ("EXIT", exit)]:
        if x < 0 or x >= width or y < 0 or y >= height:
            raise ConfigError(f"{name} {x},{y} is outside the maze")

    if entry == exit:
        raise ConfigError("ENTRY and EXIT must be different")

    if config["PERFECT"] not in ("True", "False"):
        raise ConfigError(
            f"PERFECT must be True or False, got '{config['PERFECT']}'")

    seed = None
    if "SEED" in config:
        seed = to_int("SEED", config["SEED"])

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit,
        "output_file": config["OUTPUT_FILE"],
        "perfect": config["PERFECT"] == "True",
        "seed": seed,
    }
