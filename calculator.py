import sys
import parser as infix_parser

def main():
    """
    Main loop
    """
    while True:
        my_parser = infix_parser.Parser()
    
        try:
            expression = input(">> ")
        except EOFError:
            print("\nSee you!")
            sys.exit()
        
        try:
            syntax_tree = my_parser.parse(expression.lstrip(''))
        except infix_parser.ParserException as exc:
            print(exc.message)
            continue

        try:
            print(f"## {syntax_tree.eval():.5f}")
        except ZeroDivisionError:
            print("Cannot divide by zero")
            

if __name__ == "__main__":
    main()
