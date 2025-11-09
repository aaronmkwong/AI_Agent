# main.py

import sys
from pkg.calculator import Calculator # our evaluator
from pkg.render import format_json_output # pretty JSON output


def main():
    calculator = Calculator()  # create a calculator instance

     # if no expression was provided on the command line, show help and exit
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return
    
     # join all CLI args into a single space-separated expression string
    expression = " ".join(sys.argv[1:])
    
    try:
        result = calculator.evaluate(expression) # compute the result
        if result is not None:                   # ignore empty/whitespace expressions
            to_print = format_json_output(expression, result) # build JSON string
            print(to_print)                       # print to stdout
        else:
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        # catch and show any evaluation/formatting errors as user-friendly text
        print(f"Error: {e}")

# run main() only when executed as a script (not when imported)
if __name__ == "__main__":
    main()
