import logging
import subprocess
import sys


def compile(command: list[str]) -> bool:
    logging.debug("Running: " + " ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)
    try:
        result.check_returncode()
    except subprocess.CalledProcessError:
        logging.error(f"Compiling {filename} failed with stderr: \n {result.stderr}")
        return False

    return True


source_files = sys.argv[1].splitlines()
options = sys.argv[2].splitlines()

logging.basicConfig(level=logging.DEBUG)

version = subprocess.run(["typst", "--version"], capture_output=True, text=True).stdout
logging.info(f"Using version {version}")

success: dict[str, bool] = {}

for filename in source_files:

    filename = filename.strip()

    if filename == "":
        continue

    logging.info(f"Building {filename}")
    command = ["typst"] + options + ["compile", filename]
    success[filename] = compile(command)


for filename, status in success.items():
    logging.info(f"{filename}: {'✔' if status else '❌'}")

if not all(success.values()):
    sys.exit(1)
