# target_script.py

def calculate_factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * calculate_factorial(n - 1)

def main():
    number = 5
    print(f"The factorial of {number} is {calculate_factrial(number)}")  # Intentional typo: 'calculate_factrial' instead of 'calculate_factorial'

if __name__ == "__main__":
    main()

