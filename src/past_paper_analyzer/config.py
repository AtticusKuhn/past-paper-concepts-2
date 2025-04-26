import os
import sys
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
# Searches parent directories for .env file as well
load_dotenv(
    override=True
)  # `override=True` ensures .env takes precedence over system env vars

# --- Authentication ---
CL_AUTH_COOKIE = os.getenv("CL_AUTH_COOKIE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- File Paths ---
DEFAULT_GRAPH_PATH = "data/concept_graph.graphml"
GRAPH_DATA_PATH = os.getenv("GRAPH_DATA_PATH", DEFAULT_GRAPH_PATH)


# --- Validation and Setup ---
def check_config():
    """Checks essential configuration and creates directories."""
    config_ok = True
    if not CL_AUTH_COOKIE:
        print(
            "Warning: CL_AUTH_COOKIE environment variable not set in .env file. Downloading will fail.",
            file=sys.stderr,
        )
        # Depending on the command, this might be critical or not.
        # For now, just warn. We could raise an error later if needed.
        # config_ok = False # Uncomment if download is always essential

    # We might not need the API key for all operations (e.g., just downloading or visualizing)
    # Check for it specifically when the llm_extractor is used.

    # Ensure the directory for the graph data exists
    data_dir = os.path.dirname(GRAPH_DATA_PATH)
    if data_dir:  # Only create if path includes a directory
        try:
            os.makedirs(data_dir, exist_ok=True)
            # print(f"Ensured data directory exists: {data_dir}") # Optional: confirmation message
        except OSError as e:
            print(f"Error creating data directory '{data_dir}': {e}", file=sys.stderr)
            config_ok = False

    # Ensure downloads directory exists (used by downloader)
    download_dir = "downloads"
    try:
        os.makedirs(download_dir, exist_ok=True)
        # print(f"Ensured downloads directory exists: {download_dir}") # Optional
    except OSError as e:
        print(
            f"Error creating downloads directory '{download_dir}': {e}", file=sys.stderr
        )
        config_ok = False

    return config_ok


# Perform checks when the module is loaded
INITIAL_CONFIG_OK = check_config()

# Example of how to access config:
# from . import config
# api_key = config.OPENAI_API_KEY
