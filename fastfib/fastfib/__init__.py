"""
FastFib - Ultra-fast EXACT Fibonacci computation using GMP and matrix exponentiation

This package provides highly optimized Fibonacci number computation using:
- Matrix exponentiation: O(log n) time complexity
- GMP arbitrary precision arithmetic for EXACT results
- Multi-core parallel processing with OpenMP
- Optimized C++ implementation with Python bindings

Examples:
    >>> import fastfib
    >>> fastfib.fib(10)
    '55'
    
    >>> fastfib.fib(100)
    '354224848179261915075'
    
    >>> fastfib.fib_int(100)  # Returns Python int
    354224848179261915075
    
    >>> fastfib.fib_range(10, 15)
    ['55', '89', '144', '233', '377', '610']
    
    >>> fastfib.fib_range_int(10, 15)  # Returns Python ints
    [55, 89, 144, 233, 377, 610]
"""

from ._fastfib import (
    fibonacci,
    fibonacci_int,
    fibonacci_range,
    fibonacci_range_int,
    fibonacci_array,
    fibonacci_digit_count,
    get_num_cores,
    set_num_threads,
    METHOD,
    __version__
)

# User-friendly aliases
fib = fibonacci
fib_int = fibonacci_int
fib_range = fibonacci_range
fib_range_int = fibonacci_range_int
fib_array = fibonacci_array
digit_count = fibonacci_digit_count

__all__ = [
    # Main functions
    'fib',
    'fib_int',
    'fibonacci',
    'fibonacci_int',
    'fib_range',
    'fib_range_int',
    'fibonacci_range',
    'fibonacci_range_int',
    'fib_array',
    'fibonacci_array',
    'digit_count',
    'fibonacci_digit_count',
    
    # Utility functions
    'get_num_cores',
    'set_num_threads',
    
    # Constants
    'METHOD',
    
    # Version
    '__version__',
]

# Module metadata
__author__ = 'FastFib Contributors'
__license__ = 'MIT'

def info():
    """Print information about the fastfib package."""
    print(f"FastFib v{__version__}")
    print(f"Method: {METHOD}")
    print(f"Available CPU cores: {get_num_cores()}")
    print(f"\nCompute EXACT Fibonacci numbers using matrix exponentiation!")
    print(f"\nUsage:")
    print(f"  fastfib.fib(n)                 - Single Fibonacci as string")
    print(f"  fastfib.fib_int(n)             - Single Fibonacci as Python int")
    print(f"  fastfib.fib_range(a, b)        - Range as list of strings")
    print(f"  fastfib.fib_range_int(a, b)    - Range as list of Python ints")
    print(f"  fastfib.fib_array(a, b)        - Range as NumPy array")
    print(f"  fastfib.digit_count(n)         - Get number of digits in F(n)")
