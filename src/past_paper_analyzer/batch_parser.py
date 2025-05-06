import re
import sys
from typing import List, Tuple, Optional, Dict

# Expected format for paper specifiers in the batch file:
# y<YYYY>p<XX>
# y[<YYYY>-<YYYY>]p<XX>
# y<YYYY>p[<XX>-<XX>]
# y[<YYYY>-<YYYY>]p[<XX>-<XX>]
# Optional course hint: "Course Name: y<YYYY>p<XX>"

# Regex to capture the course hint and the main specifier part
LINE_PATTERN = re.compile(r"^(?:([^:]+):\s*)?(.*)$")

# Regex to parse the paper specifier part (e.g., y2022p06 or y[2020-2022]p[01-03])
SPECIFIER_PATTERN = re.compile(
    r"y(?:(\d{4})|\[(\d{4})-(\d{4})\])"  # Year or Year Range
    r"p(?:(\d{1,2})|\[(\d{1,2})-(\d{1,2})\])",  # Paper or Paper Range
    re.IGNORECASE,
)


def _parse_range(val_str: Optional[str], start_str: Optional[str], end_str: Optional[str]) -> List[int]:
    """Helper to parse single values or ranges from regex matches."""
    if val_str:
        return [int(val_str)]
    if start_str and end_str:
        start = int(start_str)
        end = int(end_str)
        if start > end:
            # Or raise error, or return empty list
            print(f"Warning: Invalid range {start}-{end}, start is greater than end.", file=sys.stderr)
            return []
        return list(range(start, end + 1))
    return []


def parse_batch_file_line(line: str) -> List[Dict[str, any]]:
    """
    Parses a single line from the batch download file.

    A line can be:
    - "y<YYYY>p<XX>"
    - "y[<YYYY>-<YYYY>]p<XX>"
    - "y<YYYY>p[<XX>-<XX>]"
    - "y[<YYYY>-<YYYY>]p[<XX>-<XX>]"
    - "Optional Course Hint: <specifier>"

    Returns:
        A list of dictionaries, each containing 'year', 'paper_code', 
        and 'course_hint' (which can be None).
        Returns an empty list if parsing fails for the line.
    """
    line = line.strip()
    if not line or line.startswith("#"):  # Skip empty lines and comments
        return []

    line_match = LINE_PATTERN.match(line)
    if not line_match:
        print(f"Warning: Could not parse line structure: {line}", file=sys.stderr)
        return []

    course_hint_str = line_match.group(1)
    specifier_str = line_match.group(2)

    course_hint = course_hint_str.strip() if course_hint_str else None

    spec_match = SPECIFIER_PATTERN.fullmatch(specifier_str.strip())
    if not spec_match:
        print(f"Warning: Invalid paper specifier format: '{specifier_str}' in line: '{line}'", file=sys.stderr)
        print("Expected format like: yYYYYpXX or y[YYYY-YYYY]p[XX-XX]", file=sys.stderr)
        return []

    year_single, year_range_start, year_range_end, \
    paper_single, paper_range_start, paper_range_end = spec_match.groups()

    years = _parse_range(year_single, year_range_start, year_range_end)
    papers = _parse_range(paper_single, paper_range_start, paper_range_end)

    if not years or not papers:
        print(f"Warning: Could not extract valid years or papers from specifier: '{specifier_str}'", file=sys.stderr)
        return []

    parsed_items = []
    for year_val in years:
        for paper_val in papers:
            # Format paper_code consistently (e.g., p6 -> p06)
            paper_code = f"p{paper_val:02d}"
            parsed_items.append({
                "year": year_val,
                "paper_code": paper_code,
                "course_hint": course_hint
            })
    
    return parsed_items


def load_batch_file(filepath: str) -> List[Dict[str, any]]:
    """
    Loads and parses a batch download file.

    Args:
        filepath: Path to the batch download file.

    Returns:
        A list of all parsed paper specifications from the file.
        Each item is a dictionary: {'year': int, 'paper_code': str, 'course_hint': Optional[str]}
    """
    all_paper_specs = []
    try:
        with open(filepath, "r") as f:
            for i, line_content in enumerate(f):
                parsed_line_items = parse_batch_file_line(line_content)
                if parsed_line_items:
                    all_paper_specs.extend(parsed_line_items)
                elif line_content.strip() and not line_content.strip().startswith("#"):
                    print(f"Info: Line {i+1} in '{filepath}' did not yield any valid paper specifications.", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: Batch file not found: {filepath}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error reading or parsing batch file '{filepath}': {e}", file=sys.stderr)
        return []
    
    return all_paper_specs

if __name__ == '__main__':
    # Example Usage for testing
    test_lines = [
        "y2022p06",
        "Computer Graphics: y2021p7",
        "y[2020-2021]p01",
        "Algorithms: y2023p[2-3]",
        "y[2019-2020]p[10-11]",
        "Invalid line format",
        "# This is a comment",
        "  ",
        "Operating Systems: y[2022-2021]p01", # Invalid year range
        "Further Topics: y2020p99", # Valid format, specific paper
    ]

    print("--- Testing parse_batch_file_line ---")
    for test_line in test_lines:
        print(f"\nParsing line: '{test_line}'")
        results = parse_batch_file_line(test_line)
        if results:
            for res in results:
                print(f"  - {res}")
        else:
            print("  - No results or warning issued.")
    
    # Create a dummy batch file for testing load_batch_file
    dummy_batch_content = "\n".join(test_lines)
    dummy_filepath = "dummy_batch_file.txt"
    with open(dummy_filepath, "w") as f:
        f.write(dummy_batch_content)

    print(f"\n--- Testing load_batch_file with '{dummy_filepath}' ---")
    all_specs = load_batch_file(dummy_filepath)
    if all_specs:
        print(f"Total paper specifications loaded: {len(all_specs)}")
        for i, spec in enumerate(all_specs):
            print(f"  {i+1}. Year: {spec['year']}, Paper: {spec['paper_code']}, Hint: {spec['course_hint']}")
    else:
        print("No specifications loaded from dummy file.")
    
    # Clean up dummy file
    import os
    os.remove(dummy_filepath)
