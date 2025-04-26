#!/usr/bin/env python
import sys
import os

# Ensure the src directory is in the Python path
# This allows running 'python main.py' from the project root
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    # Prepend src_path to ensure local modules are found first
    sys.path.insert(0, src_path)

# Check if running inside Nix shell which sets PYTHONPATH
# print(f"Current sys.path: {sys.path}") # Debugging path issues
# print(f"PYTHONPATH env var: {os.getenv('PYTHONPATH')}") # Debugging path issues

# Import the cli module *after* potentially modifying sys.path
try:
    from past_paper_analyzer import cli
except ModuleNotFoundError:
    print("Error: Could not find the 'past_paper_analyzer' module.", file=sys.stderr)
    print(f"Please ensure you are running this script from the project root directory ('{project_root}')", file=sys.stderr)
    print(f"and that the 'src' directory is correctly added to the Python path.", file=sys.stderr)
    print(f"Current sys.path: {sys.path}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    # Check if essential config is okay before running CLI
    # Note: config module runs its check on import
    from past_paper_analyzer import config
    # if not config.INITIAL_CONFIG_OK:
        # Optionally prevent execution if config is bad
        # print("Exiting due to configuration errors.", file=sys.stderr)
        # sys.exit(1)

    cli.main()
