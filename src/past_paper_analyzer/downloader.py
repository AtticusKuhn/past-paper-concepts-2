import requests
import os
import sys
from . import config

# Ensure the downloads directory exists (redundant if check_config runs first, but safe)
os.makedirs("downloads", exist_ok=True)

def download_pdf(year: int, paper_code: str, question_number: str) -> str | None:
    """
    Downloads a specific past paper solutions PDF from the CL website.

    Args:
        year: The exam year (e.g., 2022).
        paper_code: The paper code (e.g., "p06").
        question_number: The question number (e.g., "q01").

    Returns:
        The local file path to the downloaded PDF if successful, None otherwise.
    """
    # Example URL: https://www.cl.cam.ac.uk/teaching/exams/solutions/2022/2022-p06-q01-solutions.pdf
    filename = f"{year}-{paper_code}-{question_number}-solutions.pdf"
    url = f"https://www.cl.cam.ac.uk/teaching/exams/solutions/{year}/{filename}"
    output_path = os.path.join("downloads", filename)

    print(f"Attempting to download: {url}")

    if not config.CL_AUTH_COOKIE:
        print("Error: CL_AUTH_COOKIE is not set in the .env file. Cannot authenticate.", file=sys.stderr)
        return None

    # Use the cookie value directly in the Cookie header
    headers = {
        'Cookie': f'cl_raven_auth={config.CL_AUTH_COOKIE}',
        'User-Agent': 'PastPaperConceptAnalyzer/0.1 (Python script; contact example@example.com)' # Good practice
    }

    try:
        # Use a session object for potential connection reuse
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(url, stream=True, timeout=60) # Increased timeout

            # Check status code immediately after the request
            if response.status_code == 403:
                 print(f"Download failed: 403 Forbidden. Check your CL_AUTH_COOKIE value in .env.", file=sys.stderr)
                 return None
            elif response.status_code == 404:
                 print(f"Download failed: 404 Not Found. Check year ({year}), paper code ({paper_code}), and question number ({question_number}).", file=sys.stderr)
                 return None

            # Raise an exception for other bad status codes (e.g., 5xx)
            response.raise_for_status()

            # Stream the download
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Successfully downloaded '{filename}' to '{output_path}'")
            return output_path

    except requests.exceptions.Timeout:
        print(f"Error: Download timed out for {url}", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during download: {e}", file=sys.stderr)
        return None

# Example usage (for direct testing):
# if __name__ == '__main__':
#     # Make sure you have a .env file with CL_AUTH_COOKIE set correctly
#     if config.INITIAL_CONFIG_OK:
#         downloaded_path = download_pdf(2022, "p06", "q01")
#         if downloaded_path:
#             print(f"Test download successful: {downloaded_path}")
#         else:
#             print("Test download failed.")
#     else:
#         print("Config check failed, cannot run download test.")
