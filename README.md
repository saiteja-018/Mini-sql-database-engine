# Mini SQL Database Engine

A simplified, in-memory SQL query engine built from scratch using Python. This project demonstrates fundamental database concepts including data loading, SQL parsing, query execution, and CLI design.

## Features

- **Data Loading**: Load CSV files into an in-memory data structure (list of dictionaries)
- **SQL Parser**: Parse a subset of SQL syntax including SELECT, FROM, and WHERE clauses
- **Query Execution**: 
  - Projection: SELECT all columns (`*`) or specific columns
  - Filtering: WHERE clause with comparison operators
  - Aggregation: COUNT(*) and COUNT(column_name) functions
- **Interactive CLI**: REPL interface for executing queries interactively
- **Error Handling**: Clear, informative error messages
- **Formatted Output**: Results displayed in tabular format

## Supported SQL Grammar

```
SELECT_STATEMENT ::= 
    SELECT <select_list> FROM <table_name> [WHERE <condition>]

<select_list> ::=
    '*' 
    | <column_name> { ',' <column_name> }
    | 'COUNT' '(' ('*' | <column_name>) ')'

<table_name> ::= <identifier>

<condition> ::= <column_name> <operator> <value>

<operator> ::= '=' | '!=' | '>' | '<' | '>=' | '<='

<value> ::= <string_literal> | <number>

<string_literal> ::= "'" <any_characters> "'"

<number> ::= <integer> | <decimal>

<column_name> ::= <identifier>

<identifier> ::= [a-zA-Z_][a-zA-Z0-9_]*
```

## Installation

1. Clone or navigate to the project directory:
```bash
cd Mini-sql-database-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Engine

```bash
python main.py
```

### Loading a CSV File

```
> LOAD data.csv
✓ Successfully loaded 'data.csv'
  Table name: data
  Rows: 1000
  Columns: id, name, age, country, salary
```

The table name is automatically derived from the CSV filename (without the `.csv` extension).

### Running Queries

#### Select All Columns
```
> SELECT * FROM data
```

#### Select Specific Columns
```
> SELECT name, age FROM data
```

#### Filter with WHERE Clause
```
> SELECT name, salary FROM data WHERE country = 'USA'
```

#### Use Comparison Operators
```
> SELECT * FROM data WHERE age > 30
> SELECT * FROM data WHERE salary >= 50000
> SELECT * FROM data WHERE age != 25
```

#### Count Rows
```
> SELECT COUNT(*) FROM data
```

#### Count Non-null Values in a Column
```
> SELECT COUNT(name) FROM data
```

#### Combined Filtering and Aggregation
```
> SELECT COUNT(*) FROM data WHERE country = 'USA'
```

### Commands

- `LOAD <filepath>` - Load a CSV file
- `HELP` - Show help information
- `EXIT` or `QUIT` - Exit the engine

## Project Structure

```
Mini-sql-database-engine/
├── main.py                 # CLI and REPL interface
├── data_loader.py          # CSV loading functionality
├── sql_parser.py           # SQL parsing logic
├── query_executor.py       # Query execution engine
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Module Descriptions

### `data_loader.py`
Handles CSV file loading with error checking:
- Validates file existence and format
- Uses `csv.DictReader` for loading data into list of dictionaries
- Derives table name from filename
- Includes comprehensive error messages

**Key Function:**
- `load_csv(file_path)` → Returns (rows, table_name)

### `sql_parser.py`
Parses SQL queries into structured components:
- Identifies SELECT, FROM, WHERE clauses using regex patterns
- Extracts column names, table name, and filter conditions
- Supports aggregate functions (COUNT)
- Validates syntax and provides informative errors

**Key Function:**
- `parse_query(query)` → Returns parsed query dictionary

### `query_executor.py`
Executes parsed queries against in-memory data:
- Applies WHERE filtering first
- Then applies aggregation if present
- Finally applies SELECT projection
- Type coercion for comparisons
- Comprehensive error checking

**Key Function:**
- `execute_query(data, parsed_query)` → Returns result rows

### `main.py`
Command-line interface and REPL:
- Interactive prompt for loading files and executing queries
- Formatted table output using `tabulate` library
- Help system
- Error handling and user feedback

## Example Workflow

```bash
$ python main.py

╔══════════════════════════════════════════════════════════════════╗
║         Welcome to the Mini SQL Database Engine!               ║
║                                                                  ║
║  Type 'HELP' for available commands or 'LOAD <file>' to start   ║
╚══════════════════════════════════════════════════════════════════╝

> LOAD employees.csv

✓ Successfully loaded 'employees.csv'
  Table name: employees
  Rows: 100
  Columns: id, name, department, salary, hire_date

> SELECT name, salary FROM employees WHERE salary > 50000

╒════════════════╤════════════╕
│ name           │ salary     │
╞════════════════╪════════════╡
│ Alice Johnson  │ 60000      │
│ Bob Smith      │ 75000      │
│ Carol White    │ 55000      │
╘════════════════╧════════════╛

Rows returned: 3

> SELECT COUNT(*) FROM employees WHERE department = 'Engineering'

╒════════════════╕
│ COUNT(*)       │
╞════════════════╡
│ 25             │
╘════════════════╛

Rows returned: 1

> EXIT
✓ Goodbye!
```

## Error Handling

The engine handles various error conditions gracefully:

### Parse Errors
- Invalid SQL syntax
- Malformed WHERE clauses
- Invalid column names
- Incorrect value formats

### Execution Errors
- Non-existent columns
- Type mismatches in comparisons
- Table name mismatch with loaded data

### Loading Errors
- File not found
- Invalid CSV format
- Empty files
- Missing header row

Example error messages:
```
✗ Parse Error: Invalid column name: '123invalid'
✗ Execution Error: Column 'salary' not found in table.
✗ Error loading file: File 'data.csv' not found.
```

## Test Data

To test the engine, create a sample CSV file:

```csv
id,name,age,country,salary
1,Alice Johnson,32,USA,65000
2,Bob Smith,28,Canada,55000
3,Carol White,35,USA,72000
4,David Brown,29,UK,58000
5,Eve Davis,31,USA,68000
```

Then run:
```bash
python main.py
> LOAD sample.csv
> SELECT * FROM sample
> SELECT name, salary FROM sample WHERE age > 30
> SELECT COUNT(*) FROM sample WHERE country = 'USA'
```

## Limitations & Future Enhancements

### Current Limitations
- Single WHERE condition only (no AND/OR)
- Only COUNT aggregate function (no SUM, AVG, MIN, MAX)
- No JOIN operations
- No ORDER BY or GROUP BY
- No CREATE or INSERT operations
- Table name must match loaded CSV filename

### Possible Enhancements
1. Multiple WHERE conditions with AND/OR logic
2. Additional aggregate functions (SUM, AVG, MIN, MAX)
3. ORDER BY clause
4. GROUP BY clause with aggregation
5. LIMIT clause
6. DISTINCT keyword
7. INSERT, UPDATE, DELETE operations
8. Table aliasing
9. JOIN operations
10. Nested queries

## Dependencies

- **tabulate** (0.9.0): For formatted table output
- **Python 3.7+**: Built-in modules: csv, re, pathlib

## Author Notes

This project is designed as an educational tool to understand:
- How database engines parse SQL queries
- How data filtering and projection works
- How aggregation functions are computed
- How to design clean, modular code
- The importance of comprehensive error handling

The simplified parsing approach (regex-based) is suitable for basic SQL. Production databases use more sophisticated parsing techniques (e.g., tokenizers and recursive descent parsers).

## License

This project is provided as-is for educational purposes.
