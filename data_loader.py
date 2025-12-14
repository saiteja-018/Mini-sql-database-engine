"""
Module for loading CSV data into an in-memory data structure.
"""

import csv
from pathlib import Path
from typing import List, Dict, Any


def load_csv(file_path: str) -> tuple[List[Dict[str, Any]], str]:
    """
    Load data from a CSV file into a list of dictionaries.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        tuple: (list of dictionaries representing rows, table name derived from filename)
        
    Raises:
        FileNotFoundError: If the CSV file does not exist
        ValueError: If the file is empty or not a valid CSV
    """
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found.")
    
    # Check if it's a CSV file
    if path.suffix.lower() != '.csv':
        raise ValueError(f"File '{file_path}' is not a CSV file.")
    
    # Extract table name from filename (without extension)
    table_name = path.stem
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or has no header row.")
            
            # Load all rows into a list of dictionaries
            rows = list(reader)
            
            if not rows:
                raise ValueError("CSV file has no data rows.")
            
            return rows, table_name
            
    except csv.Error as e:
        raise ValueError(f"Error reading CSV file: {e}")
