"""
Module for executing parsed SQL queries against in-memory data.
"""

from typing import List, Dict, Any, Optional


class ExecutionError(Exception):
    """Exception raised during query execution."""
    pass


def execute_query(
    data: List[Dict[str, Any]],
    parsed_query: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Execute a parsed SQL query against in-memory data.
    
    Execution order:
        1. Filter rows using WHERE clause (if present)
        2. Apply aggregation (COUNT) if present
        3. Apply projection (SELECT clause)
        
    Args:
        data: List of dictionaries representing rows
        parsed_query: Dictionary from sql_parser.parse_query()
        
    Returns:
        List of dictionaries with query results
        
    Raises:
        ExecutionError: If columns don't exist or operations fail
    """
    
    # Step 1: Apply WHERE clause
    filtered_data = _apply_where_clause(data, parsed_query['where_clause'])
    
    # Step 2: Apply aggregation
    if parsed_query['aggregate']:
        result = _apply_aggregation(filtered_data, parsed_query['aggregate'])
        return [result]
    
    # Step 3: Apply projection (SELECT)
    result_data = _apply_projection(
        filtered_data,
        parsed_query['select_cols']
    )
    
    return result_data


def _apply_where_clause(
    data: List[Dict[str, Any]],
    where_clause: Optional[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Filter rows based on WHERE clause condition.
    
    Args:
        data: List of rows
        where_clause: Dictionary with 'col', 'op', 'val' or None
        
    Returns:
        Filtered list of rows
        
    Raises:
        ExecutionError: If column doesn't exist
    """
    
    if not where_clause:
        return data
    
    col = where_clause['col']
    op = where_clause['op']
    val = where_clause['val']
    
    filtered = []
    
    for row in data:
        # Check if column exists in row
        if col not in row:
            raise ExecutionError(f"Column '{col}' not found in table.")
        
        row_val = row[col]
        
        # Try to convert row value to same type as comparison value
        try:
            row_val = _coerce_value(row_val, val)
        except ValueError as e:
            raise ExecutionError(
                f"Cannot compare column '{col}' with value '{val}': {e}"
            )
        
        # Apply comparison
        if _compare(row_val, op, val):
            filtered.append(row)
    
    return filtered


def _coerce_value(row_val: Any, comparison_val: Any) -> Any:
    """
    Coerce row value to match the type of comparison value.
    
    Args:
        row_val: Value from the row
        comparison_val: Value to compare against
        
    Returns:
        Coerced row value
        
    Raises:
        ValueError: If coercion is not possible
    """
    
    # If both are already same type, return as-is
    if type(row_val) == type(comparison_val):
        return row_val
    
    # If comparing with string, convert to string
    if isinstance(comparison_val, str):
        return str(row_val)
    
    # If comparing with number, try to convert row_val to number
    if isinstance(comparison_val, (int, float)):
        try:
            if isinstance(comparison_val, float):
                return float(row_val)
            else:
                # Try int first, fall back to float
                if '.' in str(row_val):
                    return float(row_val)
                return int(row_val)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert '{row_val}' to number")
    
    return row_val


def _compare(row_val: Any, op: str, comparison_val: Any) -> bool:
    """
    Compare two values based on operator.
    
    Args:
        row_val: Value from the row
        op: Comparison operator (=, !=, >, <, >=, <=)
        comparison_val: Value to compare against
        
    Returns:
        Boolean result of comparison
        
    Raises:
        ExecutionError: If operator is unknown
    """
    
    if op == '=':
        return row_val == comparison_val
    elif op == '!=':
        return row_val != comparison_val
    elif op == '>':
        return row_val > comparison_val
    elif op == '<':
        return row_val < comparison_val
    elif op == '>=':
        return row_val >= comparison_val
    elif op == '<=':
        return row_val <= comparison_val
    else:
        raise ExecutionError(f"Unknown operator: '{op}'")


def _apply_aggregation(
    data: List[Dict[str, Any]],
    aggregate: Dict[str, str]
) -> Dict[str, Any]:
    """
    Apply aggregation function to data.
    
    Supports COUNT(*) and COUNT(column_name).
    
    Args:
        data: List of rows
        aggregate: Dictionary with 'function' and 'column'
        
    Returns:
        Dictionary with aggregation result
        
    Raises:
        ExecutionError: If column doesn't exist or function is unknown
    """
    
    func = aggregate['function'].upper()
    col = aggregate['column']
    
    if func != 'COUNT':
        raise ExecutionError(f"Unsupported aggregate function: '{func}'")
    
    if col == '*':
        # COUNT(*)
        return {'COUNT(*)': len(data)}
    else:
        # COUNT(column_name) - count non-null values
        if data and col not in data[0]:
            raise ExecutionError(f"Column '{col}' not found in table.")
        
        count = sum(1 for row in data if col in row and row[col] is not None and row[col] != '')
        return {f'COUNT({col})': count}


def _apply_projection(
    data: List[Dict[str, Any]],
    select_cols: List[str]
) -> List[Dict[str, Any]]:
    """
    Project columns from rows.
    
    Args:
        data: List of rows
        select_cols: List of column names or ['*']
        
    Returns:
        List of rows with only selected columns
        
    Raises:
        ExecutionError: If column doesn't exist
    """
    
    if not data:
        return []
    
    # SELECT *
    if select_cols == ['*']:
        return data
    
    # SELECT specific columns
    projected = []
    for row in data:
        projected_row = {}
        for col in select_cols:
            if col not in row:
                raise ExecutionError(f"Column '{col}' not found in table.")
            projected_row[col] = row[col]
        projected.append(projected_row)
    
    return projected
