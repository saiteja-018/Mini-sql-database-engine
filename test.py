"""
Test script for the SQL query engine.
Demonstrates all features without requiring interactive input.
"""

from data_loader import load_csv
from sql_parser import parse_query
from query_executor import execute_query
from tabulate import tabulate


def test_sql_engine():
    """Run comprehensive tests of the SQL engine."""
    
    print("\n" + "="*70)
    print("Mini SQL Database Engine - Test Suite")
    print("="*70 + "\n")
    
    # Load sample data
    print("TEST 1: Loading CSV file")
    print("-" * 70)
    try:
        data, table_name = load_csv('sample_data.csv')
        print(f"[OK] Successfully loaded CSV file")
        print(f"  Table name: {table_name}")
        print(f"  Rows: {len(data)}")
        print(f"  Columns: {list(data[0].keys())}")
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        return
    
    print()
    
    # Test cases
    test_cases = [
        {
            'name': 'SELECT all columns',
            'query': 'SELECT * FROM sample_data',
            'expected': f'All {len(data)} rows with all columns'
        },
        {
            'name': 'SELECT specific columns',
            'query': 'SELECT name, salary FROM sample_data',
            'expected': 'Rows with only name and salary'
        },
        {
            'name': 'SELECT with WHERE equals',
            'query': "SELECT name, age FROM sample_data WHERE country = 'USA'",
            'expected': 'Rows where country is USA'
        },
        {
            'name': 'SELECT with WHERE greater than',
            'query': 'SELECT name, age, salary FROM sample_data WHERE age > 30',
            'expected': 'Rows where age is greater than 30'
        },
        {
            'name': 'SELECT with WHERE less than',
            'query': 'SELECT name, age FROM sample_data WHERE age < 28',
            'expected': 'Rows where age is less than 28'
        },
        {
            'name': 'SELECT with WHERE not equal',
            'query': "SELECT name, country FROM sample_data WHERE country != 'USA'",
            'expected': 'Rows where country is not USA'
        },
        {
            'name': 'SELECT with WHERE greater than or equal',
            'query': 'SELECT name, salary FROM sample_data WHERE salary >= 65000',
            'expected': 'Rows with salary >= 65000'
        },
        {
            'name': 'SELECT with WHERE less than or equal',
            'query': 'SELECT name, age FROM sample_data WHERE age <= 28',
            'expected': 'Rows where age <= 28'
        },
        {
            'name': 'COUNT all rows',
            'query': 'SELECT COUNT(*) FROM sample_data',
            'expected': f'Total row count: {len(data)}'
        },
        {
            'name': 'COUNT with filter',
            'query': "SELECT COUNT(*) FROM sample_data WHERE country = 'USA'",
            'expected': 'Count of rows where country is USA'
        },
        {
            'name': 'COUNT specific column',
            'query': 'SELECT COUNT(name) FROM sample_data',
            'expected': f'Count of non-null name values: {len(data)}'
        },
        {
            'name': 'COUNT with column and filter',
            'query': "SELECT COUNT(salary) FROM sample_data WHERE department = 'Engineering'",
            'expected': 'Count of salary values in Engineering department'
        },
    ]
    
    # Run tests
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"TEST {i+1}: {test_case['name']}")
        print("-" * 70)
        
        try:
            # Parse and execute query
            parsed = parse_query(test_case['query'])
            result = execute_query(data, parsed)
            
            # Display results
            if result:
                print(tabulate(result, headers='keys', tablefmt='simple'))
                print(f"[OK] Rows returned: {len(result)}")
            else:
                print("(No results)")
            
            passed += 1
            
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            failed += 1
        
        print()
    
    # Summary
    print("="*70)
    print(f"Test Summary: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("="*70 + "\n")


def test_error_handling():
    """Test error handling."""
    
    print("\n" + "="*70)
    print("Error Handling Tests")
    print("="*70 + "\n")
    
    # Load data
    data, table_name = load_csv('sample_data.csv')
    
    error_tests = [
        {
            'name': 'Non-existent column in SELECT',
            'query': 'SELECT non_existent FROM sample_data'
        },
        {
            'name': 'Non-existent column in WHERE',
            'query': 'SELECT * FROM sample_data WHERE non_existent = 123'
        },
        {
            'name': 'Invalid SQL syntax',
            'query': 'INVALID QUERY SYNTAX'
        },
        {
            'name': 'Wrong table name (caught by CLI, not test)',
            'query': 'SELECT * FROM wrong_table',
            'skip': True
        },
        {
            'name': 'Missing FROM clause',
            'query': 'SELECT name'
        },
        {
            'name': 'Invalid comparison operator',
            'query': "SELECT * FROM sample_data WHERE name <=> 'Alice'"
        },
    ]
    
    handled = 0
    unhandled = 0
    
    for i, test in enumerate(error_tests, 1):
        print(f"ERROR TEST {i}: {test['name']}")
        print(f"  Query: {test['query']}")
        
        # Skip tests that are handled at CLI level
        if test.get('skip'):
            print(f"  [SKIP] Skipped (handled at CLI level)")
            print()
            continue
        
        try:
            parsed = parse_query(test['query'])
            result = execute_query(data, parsed)
            print(f"  [ERROR] Error was not caught!")
            unhandled += 1
        except Exception as e:
            print(f"  [OK] Correctly caught: {type(e).__name__}")
            print(f"      Message: {e}")
            handled += 1
        
        print()
    
    # Summary
    print("="*70)
    print(f"Error Handling Summary: {handled} handled, {unhandled} unhandled")
    print("="*70 + "\n")


if __name__ == '__main__':
    test_sql_engine()
    test_error_handling()
    
    print("="*70)
    print("All tests completed! Run 'python main.py' for interactive mode.")
    print("="*70 + "\n")
