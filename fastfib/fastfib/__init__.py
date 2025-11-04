"""
FastFib - Ultra-fast Fibonacci computation using C++ and Binet's formula

This package provides highly optimized Fibonacci number computation using:
- Binet's formula: F(n) ≈ φ^n / √5
- Multi-core parallel processing with OpenMP
- Optimized C++ implementation with Python bindings

Examples:
    >>> import fastfib
    >>> fastfib.fib(10)
    55.0
    
    >>> fastfib.fib(100)
    3.542248481792619e+20
    
    >>> fastfib.fib_range(10, 15)
    [55.0, 89.0, 144.0, 233.0, 377.0, 610.0]
    
    >>> import numpy as np
    >>> arr = fastfib.fib_array(1, 10)
    >>> arr
    array([1., 1., 2., 3., 5., 8., 13., 21., 34., 55.])
"""

from ._fastfib import (
    fibonacci,
    fibonacci_range,
    fibonacci_array,
    get_num_cores,
    set_num_threads,
    get_phi,
    PHI,
    SQRT5,
    __version__
)

# User-friendly aliases
fib = fibonacci
fib_range = fibonacci_range
fib_array = fibonacci_array

__all__ = [
    # Main functions
    'fib',
    'fibonacci',
    'fib_range',
    'fibonacci_range',
    'fib_array',
    'fibonacci_array',
    
    # Utility functions
    'get_num_cores',
    'set_num_threads',
    'get_phi',
    
    # Constants
    'PHI',
    'SQRT5',
    
    # Version
    '__version__',
]

# Module metadata
__author__ = 'FastFib Contributors'
__license__ = 'MIT'

def info():
    """Print information about the fastfib package."""
    print(f"FastFib v{__version__}")
    print(f"Available CPU cores: {get_num_cores()}")
    print(f"Golden ratio (φ): {PHI}")
    print(f"\nCompute Fibonacci numbers at ~1+ billion/second!")
    print(f"\nUsage:")
    print(f"  fastfib.fib(n)              - Single Fibonacci number")
    print(f"  fastfib.fib_range(a, b)     - Range as Python list")
    print(f"  fastfib.fib_array(a, b)     - Range as NumPy array")

