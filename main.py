# main.py
from math_utils import add, subtract, multiply, divide
from string_utils import capitalize_string, concatenate_strings, reverse_string, repeat_string

def main():
    result = add_numbers(5, 10)  
    print(f"Addition Result: {result}")

    repeated = repeat_string("Hello", 3)  
    print(f"Repeated String: {repeated}")

    division_result = divide(10, 0)  
    print(f"Division Result: {division_result}")

if __name__ == "__main__":
    main()

