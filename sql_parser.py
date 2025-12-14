"""
Module for parsing SQL queries.
"""

import re
from typing import Dict, Any, Optional, List


class QueryParseError(Exception):
    """Exception raised when SQL parsing fails."""
    pass


def parse_query(query: str) -> Dict[str, Any]:
    """
    Parse a SQL query into its components.
    
    Supported syntax:
        SELECT column1, column2, ... | * FROM table_name [WHERE condition]
        
    Args:
        query: Raw SQL query string
        
    Returns:
        Dictionary with keys:
            - 'select_cols': list of column names or ['*']
            - 'from_table': table name (or derived from CSV filename)
            - 'where_clause': dict with 'col', 'op', 'val' or None
            - 'aggregate': dict with 'function', 'column' or None
            
    Raises:
        QueryParseError: If the query syntax is invalid
    """
    
    # Normalize query: strip whitespace and convert to uppercase for keyword matching
    query = query.strip()
    if not query:
        raise QueryParseError("Empty query provided.")
    
    # Use regex to identify main clauses
    # Pattern: SELECT ... FROM ... [WHERE ...]
    select_pattern = r'SELECT\s+(.*?)\s+FROM\s+([\w]+)(?:\s+WHERE\s+(.+))?'
    match = re.match(select_pattern, query, re.IGNORECASE)
    
    if not match:
        raise QueryParseError(
            "Invalid SQL syntax. Expected: SELECT column(s) FROM table [WHERE condition]"
        )
    
    select_part = match.group(1).strip()
    from_table = match.group(2).strip()
    where_part = match.group(3).strip() if match.group(3) else None
    
    # Parse SELECT clause
    select_cols, aggregate = _parse_select_clause(select_part)
    
    # Parse WHERE clause
    where_clause = None
    if where_part:
        where_clause = _parse_where_clause(where_part)
    
    return {
        'select_cols': select_cols,
        'from_table': from_table,
        'where_clause': where_clause,
        'aggregate': aggregate
    }


def _parse_select_clause(select_part: str) -> tuple[List[str], Optional[Dict[str, str]]]:
    """
    Parse the SELECT clause.
    
    Supports:
        SELECT *
        SELECT column_name
        SELECT col1, col2, col3
        SELECT COUNT(*)
        SELECT COUNT(column_name)
        
    Args:
        select_part: The SELECT clause content
        
    Returns:
        tuple: (list of column names, aggregate dict or None)
        
    Raises:
        QueryParseError: If syntax is invalid
    """
    
    select_part = select_part.strip()
    
    # Check for aggregate functions
    count_pattern = r'COUNT\s*\(\s*(\*|[\w]+)\s*\)'
    count_match = re.match(count_pattern, select_part, re.IGNORECASE)
    
    if count_match:
        column = count_match.group(1).strip()
        return ['*'], {'function': 'COUNT', 'column': column}
    
    # Check for SELECT *
    if select_part == '*':
        return ['*'], None
    
    # Parse individual columns
    columns = [col.strip() for col in select_part.split(',')]
    
    # Validate column names (alphanumeric and underscore)
    for col in columns:
        if not re.match(r'^[\w]+$', col):
            raise QueryParseError(f"Invalid column name: '{col}'")
    
    return columns, None


def _parse_where_clause(where_part: str) -> Dict[str, Any]:
    """
    Parse the WHERE clause.
    
    Supports:
        column = value
        column != value
        column > value
        column < value
        column >= value
        column <= value
        
    Values can be strings (single quotes) or numbers.
    
    Args:
        where_part: The WHERE clause content
        
    Returns:
        Dictionary with keys: 'col', 'op', 'val'
        
    Raises:
        QueryParseError: If syntax is invalid
    """
    
    where_part = where_part.strip()
    
    # Pattern for WHERE clause: column operator value
    # Operators: =, !=, >=, <=, >, <
    pattern = r"([\w]+)\s*(=|!=|>=|<=|>|<)\s*(.+)"
    match = re.match(pattern, where_part)
    
    if not match:
        raise QueryParseError(
            "Invalid WHERE clause syntax. Expected: column operator value"
        )
    
    col = match.group(1).strip()
    op = match.group(2).strip()
    val = match.group(3).strip()
    
    # Parse the value (string or number)
    parsed_val = _parse_value(val)
    
    return {
        'col': col,
        'op': op,
        'val': parsed_val
    }


def _parse_value(val_str: str) -> Any:
    """
    Parse a value from the WHERE clause.
    
    Supports:
        - String literals (single quoted): 'USA'
        - Numbers (int/float): 30, 3.14
        
    Args:
        val_str: The value string
        
    Returns:
        Parsed value (str, int, or float)
        
    Raises:
        QueryParseError: If value format is invalid
    """
    
    val_str = val_str.strip()
    
    # Check for string literal (single quoted)
    if val_str.startswith("'") and val_str.endswith("'"):
        return val_str[1:-1]  # Remove quotes
    
    # Try to parse as number
    try:
        if '.' in val_str:
            return float(val_str)
        else:
            return int(val_str)
    except ValueError:
        raise QueryParseError(
            f"Invalid value: '{val_str}'. "
            "Use single quotes for strings (e.g., 'USA') or unquoted numbers."
        )
