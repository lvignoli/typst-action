"""Script to compile Typst source files."""
import logging
import subprocess
import sys


def compile(filename: str, options: list[str]) -> bool:
    """Compiles a Typst file with the specified global options.

    Returns True if the typst command exited with status 0, False otherwise.
    """
    command = ["typst"] + ["compile", filename] + options
    logging.debug("Running: " + " ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)
    try:
        result.check_returncode()
    except subprocess.CalledProcessError:
        logging.error(f"Compiling {filename} failed with stderr: \n {result.stderr}")
        return False

    return True


def main():

    logging.basicConfig(level=logging.INFO)

    # Parse the positional arguments, expected in the following form
    #   1. The Typst files to compile in a line separated string
    #   2. The global Typst CLI options, in a line separated string. It means each
    #      whitespace separated field should be on its own line.
    source_files = sys.argv[1].splitlines()
    options = sys.argv[2].splitlines()

    version = subprocess.run(
        ["typst", "--version"], capture_output=True, text=True
    ).stdout
    logging.info(f"Using version {version}")

    success: dict[str, bool] = {}

    for filename in source_files:
        filename = filename.strip()
        if filename == "":
            continue
        logging.info(f"Compiling {filename}…")
        success[filename] = compile(filename, options)

    # Log status of each input files.
    for filename, status in success.items():
        logging.info(f"{filename}: {'✔' if status else '❌'}")

    if not all(success.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
