import sys
from . import config

# Placeholder for actual LLM interaction logic
# We'll need to install and import the specific LLM library (e.g., openai)
# Example:
# try:
#     import openai
# except ImportError:
#     print("Warning: 'openai' library not found. LLM extraction will fail. Install with 'pip install openai'", file=sys.stderr)
#     openai = None


def extract_concepts_from_pdf(pdf_path: str) -> list[dict]:
    """
    Uses a Vision LLM to extract concepts from a given PDF file. (Placeholder)

    Args:
        pdf_path: Path to the solutions PDF file.

    Returns:
        A list of dictionaries, where each dictionary represents a concept
        and its context (e.g., {'concept_name': '...', 'definition': '...', 'question_context': '...'}).
        Returns an empty list if extraction fails or is not implemented.
    """
    print(f"--- LLM Extractor Placeholder ---")
    print(f"Processing PDF: '{pdf_path}'")

    if not config.OPENAI_API_KEY:
         print("Error: OPENAI_API_KEY not set in .env file. Cannot call LLM.", file=sys.stderr)
         return []

    # if openai is None:
    #      print("Error: OpenAI library not available.", file=sys.stderr)
    #      return []

    # --- Actual LLM Interaction Logic Would Go Here ---
    # 1. Configure the OpenAI client (if not already done globally)
    #    openai.api_key = config.OPENAI_API_KEY
    #
    # 2. Load/prepare the PDF data for the Vision model.
    #    - This might involve sending the PDF bytes directly if the API supports it,
    #    - or converting pages to images and sending image data/URLs.
    #    - Example using images (requires libraries like pdf2image, Pillow):
    #      from pdf2image import convert_from_path
    #      import base64
    #      images = convert_from_path(pdf_path)
    #      base64_images = []
    #      for img in images:
    #          # Convert PIL image to base64
    #          # ... (implementation needed) ...
    #          base64_images.append(base64_data)
    #
    # 3. Construct the prompt for the Vision LLM (e.g., GPT-4o). This is critical.
    #    prompt_messages = [
    #        {
    #            "role": "system",
    #            "content": "You are an expert computer science assistant analyzing Cambridge Tripos exam solutions PDFs..." # More detail needed
    #        },
    #        {
    #            "role": "user",
    #            "content": [
    #                {"type": "text", "text": "Analyze the provided exam solution PDF pages. For each distinct question or sub-question, identify the key computer science concepts discussed or applied. Provide the output as a JSON list, where each item has 'concept_name' (canonical form), 'definition' (brief, 1-2 sentences), and 'question_context' (e.g., 'Question 1a', 'Section B Q3')."},
    #                # Add image data if sending images
    #                # {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image_data}"}}
    #                # ... for each page/image ...
    #            ]
    #        }
    #    ]
    #
    # 4. Send the request to the LLM API.
    #    try:
    #        response = openai.chat.completions.create(
    #            model="gpt-4o", # Or your chosen vision model
    #            messages=prompt_messages,
    #            max_tokens=1000, # Adjust as needed
    #            # Potentially use response_format={"type": "json_object"} if supported and reliable
    #        )
    #        llm_output_content = response.choices[0].message.content
    #    except Exception as e:
    #        print(f"Error calling LLM API: {e}", file=sys.stderr)
    #        return []
    #
    # 5. Parse the response (expecting JSON).
    #    import json
    #    try:
    #        extracted_concepts = json.loads(llm_output_content)
    #        if not isinstance(extracted_concepts, list):
    #             print("Error: LLM did not return a valid JSON list.", file=sys.stderr)
    #             return []
    #        # Further validation of list items structure?
    #        return extracted_concepts
    #    except json.JSONDecodeError:
    #        print(f"Error: Could not parse JSON response from LLM: {llm_output_content}", file=sys.stderr)
    #        return []
    # --- End of Actual Logic Placeholder ---

    # Dummy data for now:
    print("Placeholder: Returning dummy concept data.")
    dummy_concepts = [
        {"concept_name": "Dummy Concept A", "definition": "A placeholder concept.", "question_context": "Question 1 Part A"},
        {"concept_name": "Dummy Concept B", "definition": "Another placeholder.", "question_context": "Question 1 Part B"},
        {"concept_name": "dummy concept a", "definition": "Duplicate placeholder.", "question_context": "Question 2"}, # Test canonicalization
    ]
    print(f"--- End LLM Extractor Placeholder ---")
    return dummy_concepts

# Example usage (for direct testing):
# if __name__ == '__main__':
#     # Assuming a dummy PDF exists or was downloaded
#     pdf_file = "downloads/2022-p06-q01-solutions.pdf" # Replace with actual path if needed
#     if os.path.exists(pdf_file) and config.INITIAL_CONFIG_OK:
#         concepts = extract_concepts_from_pdf(pdf_file)
#         print("\nExtracted Concepts (Dummy):")
#         if concepts:
#             for concept in concepts:
#                 print(f"- {concept.get('concept_name', 'N/A')} ({concept.get('question_context', 'N/A')})")
#         else:
#             print("No concepts returned.")
#     else:
#         print(f"Cannot run test: PDF '{pdf_file}' not found or config check failed.")

