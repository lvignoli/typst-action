import argparse
import logging
import subprocess
import sys


source_files = sys.argv[1]
options = sys.argv[2:]

print(source_files)
print(options)


logging.basicConfig(level=logging.INFO)

version = subprocess.run(["typst", "--version"], capture_output=True, text=True).stdout
logging.info(f"Using version {version}")

source_files: list[str] = []
options: list[str] = []

for filename in source_files:

    if filename == "":
        continue

    logging.info(f"Building {filename}")
    command = ["typst", "compile", filename].extend(options)

    try:
        compilation = subprocess.run(
            command, capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        logging.error(f"Compiling {filename} failed with stderr:")
        logging.error(compilation.stderr)
