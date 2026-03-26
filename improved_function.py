import logging
from typing import List, Tuple, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def process_data(filepath: str) -> List[Tuple[str, str]]:
    """
    Process a CSV-like file and extract the first two columns from each non-empty line.
    
    Args:
        filepath: Path to the file to process
        
    Returns:
        List of tuples containing the first two columns from each valid line
        
    Raises:
        FileNotFoundError: If the specified file does not exist
        PermissionError: If the file cannot be read due to permissions
        ValueError: If the file is empty or contains no valid data
    """
    logger.info(f"Starting to process file: {filepath}")
    
    # Validate file existence and readability
    file_path = Path(filepath)
    if not file_path.exists():
        error_msg = f"File not found: {filepath}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    if not file_path.is_file():
        error_msg = f"Path is not a file: {filepath}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    try:
        # Use context manager for proper file handling
        with open(filepath, 'r', encoding='utf-8') as file:
            data = file.read()
    except PermissionError as e:
        error_msg = f"Permission denied when reading file: {filepath}"
        logger.error(error_msg)
        raise PermissionError(error_msg) from e
    except UnicodeDecodeError as e:
        error_msg = f"Encoding error when reading file: {filepath}. Try specifying encoding."
        logger.error(error_msg)
        raise ValueError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected error reading file: {filepath}"
        logger.error(error_msg, exc_info=True)
        raise
    
    # Check if file is empty
    if not data:
        error_msg = f"File is empty: {filepath}"
        logger.warning(error_msg)
        raise ValueError(error_msg)
    
    lines = data.split('\n')
    logger.info(f"Read {len(lines)} lines from file")
    
    result: List[Tuple[str, str]] = []
    skipped_lines = 0
    processed_lines = 0
    
    for line_num, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        
        # Skip empty lines
        if not stripped_line:
            skipped_lines += 1
            continue
        
        parts = stripped_line.split(',')
        
        # Validate that we have at least 2 columns
        if len(parts) < 2:
            logger.warning(f"Line {line_num}: Insufficient columns (expected >=2, got {len(parts)}): '{stripped_line}'")
            skipped_lines += 1
            continue
        
        # Extract first two columns and strip whitespace
        col1 = parts[0].strip()
        col2 = parts[1].strip()
        
        # Check for empty columns
        if not col1 or not col2:
            logger.warning(f"Line {line_num}: Empty column value in line: '{stripped_line}'")
            skipped_lines += 1
            continue
        
        result.append((col1, col2))
        processed_lines += 1
    
    # Log processing summary
    logger.info(f"Processing complete: {processed_lines} lines processed, {skipped_lines} lines skipped")
    
    if not result:
        error_msg = f"No valid data found in file: {filepath}"
        logger.warning(error_msg)
        raise ValueError(error_msg)
    
    logger.info(f"Returning {len(result)} valid records")
    return result


# Example usage and test function
def example_usage():
    """Example demonstrating the improved function's usage."""
    try:
        # Test with a sample file
        data = process_data("sample.csv")
        print(f"Processed {len(data)} records:")
        for i, (col1, col2) in enumerate(data, start=1):
            print(f"  {i}. {col1} -> {col2}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    example_usage()