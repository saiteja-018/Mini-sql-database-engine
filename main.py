"""
Command-line interface for the SQL query engine.
"""

from typing import List, Dict, Any
from tabulate import tabulate

from data_loader import load_csv
from sql_parser import parse_query, QueryParseError
from query_executor import execute_query, ExecutionError


class SQLEngine:
    """Interactive SQL query engine."""
    
    def __init__(self):
        """Initialize the SQL engine."""
        self.data: List[Dict[str, Any]] = []
        self.table_name: str = ""
        self.is_loaded = False
    
    def load_table(self, file_path: str) -> None:
        """
        Load a CSV file into the engine.
        
        Args:
            file_path: Path to the CSV file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid
        """
        try:
            self.data, self.table_name = load_csv(file_path)
            self.is_loaded = True
            print(f"\n[OK] Successfully loaded '{file_path}'")
            print(f"  Table name: {self.table_name}")
            print(f"  Rows: {len(self.data)}")
            print(f"  Columns: {', '.join(self.data[0].keys())}\n")
        except (FileNotFoundError, ValueError) as e:
            print(f"\n[ERROR] Error loading file: {e}\n")
    
    def execute_sql(self, query: str) -> None:
        """
        Parse and execute a SQL query.
        
        Args:
            query: SQL query string
        """
        if not self.is_loaded:
            print("\n[ERROR] No table loaded. Use 'LOAD <filepath>' first.\n")
            return
        
        try:
            # Parse the query
            parsed = parse_query(query)
            
            # Validate table name matches loaded table
            if parsed['from_table'] != self.table_name:
                print(
                    f"\n[ERROR] Table '{parsed['from_table']}' not found. "
                    f"Currently loaded table: '{self.table_name}'\n"
                )
                return
            
            # Execute the query
            result = execute_query(self.data, parsed)
            
            # Display results
            self._display_results(result)
            
        except QueryParseError as e:
            print(f"\n[ERROR] Parse Error: {e}\n")
        except ExecutionError as e:
            print(f"\n[ERROR] Execution Error: {e}\n")
        except Exception as e:
            print(f"\n[ERROR] Unexpected Error: {e}\n")
    
    def _display_results(self, result: List[Dict[str, Any]]) -> None:
        """
        Display query results in a formatted table.
        
        Args:
            result: List of result rows
        """
        if not result:
            print("\n(No results)\n")
            return
        
        print()
        print(tabulate(result, headers='keys', tablefmt='grid'))
        print(f"\nRows returned: {len(result)}\n")
    
    def show_help(self) -> None:
        """Display help information."""
        help_text = """
==================================================================
            SQL Query Engine - Help
==================================================================

COMMANDS:
  LOAD <filepath>   - Load a CSV file
  EXIT or QUIT      - Exit the engine
  HELP              - Show this help message

SQL SYNTAX (Case-insensitive):
  SELECT col1, col2, ... | * FROM table_name [WHERE condition]

EXAMPLES:
  > LOAD data.csv
  > SELECT * FROM data
  > SELECT name, age FROM data WHERE age > 30
  > SELECT COUNT(*) FROM data
  > SELECT COUNT(name) FROM data WHERE age > 30

WHERE OPERATORS:
  =   : Equal to
  !=  : Not equal to
  >   : Greater than
  <   : Less than
  >=  : Greater than or equal
  <=  : Less than or equal

VALUE FORMATS:
  String: Use single quotes (e.g., 'USA')
  Number: No quotes needed (e.g., 30)
"""
        print(help_text)


def main():
    """Main entry point for the CLI."""
    engine = SQLEngine()
    
    print("""
==================================================================
      Welcome to the Mini SQL Database Engine!
      
  Type 'HELP' for available commands or 'LOAD <file>' to start
==================================================================
""")
    
    while True:
        try:
            # Get user input
            user_input = input("> ").strip()
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split(maxsplit=1)
            command = parts[0].upper()
            
            # Handle commands
            if command in ['EXIT', 'QUIT']:
                print("\n[OK] Goodbye!\n")
                break
            elif command == 'HELP':
                engine.show_help()
            elif command == 'LOAD':
                if len(parts) < 2:
                    print("\n[ERROR] LOAD command requires a file path.\n")
                else:
                    file_path = parts[1]
                    engine.load_table(file_path)
            else:
                # Treat as SQL query
                engine.execute_sql(user_input)
        
        except KeyboardInterrupt:
            print("\n\n[OK] Goodbye!\n")
            break
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}\n")


if __name__ == '__main__':
    main()
