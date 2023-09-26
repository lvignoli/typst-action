"""Script to compile Typst source files."""
import logging
import subprocess
import sys
from pathlib import Path


def compile(filename: Path, options: list[str]) -> bool:
    """Compiles a Typst file with the specified global options.

    Returns True if the typst command exited with status 0, False otherwise.
    """
    command = ["typst"] + options + ["compile", str(filename)]
    logging.debug("Running: " + " ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)
    try:
        result.check_returncode()
    except subprocess.CalledProcessError:
        logging.error(f"Compiling {filename} failed with stderr: \n {result.stderr}")
        return False

    return True


def parse_source_files(source_files_input: list[str]) -> list[Path]:
    """
    Handles globs and directories in the source files argument.
    """
    source_files_paths = []
    for source_file in source_files_input:
        source_file = source_file.strip()
        if source_file == "":
            continue
        source_file_path = Path(source_file)
        if source_file_path.is_dir():
            source_files_paths.extend(source_file_path.glob("**/*.typ"))
        elif source_file_path.is_file():
            source_files_paths.append(source_file_path)
        elif "*" in source_file:
            source_files = list(Path.cwd().glob(source_file))
            if not source_files:
                logging.error(f"No matching files found for {source_file}.")
                logging.debug(f"Current directory: {Path.cwd()}")
                logging.debug(f"First 10 files: {list(Path.cwd().iterdir())[:10]}")
            else:
                source_files_paths.extend(source_files)
        else:
            logging.error(f"Source file {source_file} does not exist.")
    return source_files_paths


def main():
    logging.basicConfig(level=logging.INFO)

    # Parse the positional arguments, expected in the following form
    #   1. The Typst files to compile in a line separated string
    #   2. The global Typst CLI options, in a line separated string. It means each
    #      whitespace separated field should be on its own line.
    source_files = parse_source_files(sys.argv[1].splitlines())
    options = sys.argv[2].splitlines()

    version = subprocess.run(
        ["typst", "--version"], capture_output=True, text=True
    ).stdout
    logging.info(f"Using version {version}")

    success: dict[str, bool] = {}

    logging.info(f"Got {len(source_files)} files to compile…")
    for file in source_files:
        logging.info(f"Compiling {file}…")
        success[str(file)] = compile(file, options)

    # Log status of each input files.
    for file, status in success.items():
        logging.info(f"{file}: {'✔' if status else '❌'}")

    if not all(success.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
