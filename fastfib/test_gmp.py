#!/usr/bin/env python3
"""
Test script for the GMP-based exact Fibonacci Python library
"""

import sys
import time

try:
    from fastfib import _fastfib as ff
    print("✓ Successfully imported _fastfib module")
except ImportError as e:
    print(f"✗ Failed to import _fastfib: {e}")
    print("\nPlease build the module first:")
    print("  cd fastfib")
    print("  pip install -e .")
    sys.exit(1)

print("\n=== Testing GMP-Based Exact Fibonacci Computation ===\n")

# Test 1: Basic single value computation
print("Test 1: Single value computation")
print("-" * 60)
test_values = [10, 50, 100, 500, 1000]
for n in test_values:
    result = ff.fibonacci(n)
    print(f"F({n}) = {result[:50]}{'...' if len(result) > 50 else ''} ({len(result)} digits)")

# Test 2: Python int version (arbitrary precision)
print("\nTest 2: Python int version (arbitrary precision)")
print("-" * 60)
fib_100 = ff.fibonacci_int(100)
print(f"F(100) = {fib_100}")
print(f"Type: {type(fib_100)}")
print(f"Can do math: F(100) + 1 = {fib_100 + 1}")

# Test 3: Range computation
print("\nTest 3: Range computation (as strings)")
print("-" * 60)
start_time = time.time()
results = ff.fibonacci_range(10, 20)
elapsed = time.time() - start_time
print(f"F(10) to F(20): {results}")
print(f"Time: {elapsed*1000:.2f} ms")

# Test 4: Range computation as Python ints
print("\nTest 4: Range computation (as Python ints)")
print("-" * 60)
start_time = time.time()
results = ff.fibonacci_range_int(10, 20)
elapsed = time.time() - start_time
print(f"F(10) to F(20): {results}")
print(f"Time: {elapsed*1000:.2f} ms")

# Test 5: Large range performance test
print("\nTest 5: Large range performance test")
print("-" * 60)
ranges = [(1, 100), (1, 1000), (1, 10000)]
for start, end in ranges:
    start_time = time.time()
    results = ff.fibonacci_range(start, end)
    elapsed = time.time() - start_time
    count = end - start + 1
    speed = count / elapsed
    print(f"F({start}) to F({end}): {count} values in {elapsed:.3f}s ({speed:.0f} vals/sec)")
    last_digits = len(results[-1])
    print(f"  F({end}) has {last_digits} digits")

# Test 6: Very large Fibonacci numbers
print("\nTest 6: Very large Fibonacci numbers")
print("-" * 60)
large_values = [10000, 50000, 100000]
for n in large_values:
    start_time = time.time()
    result = ff.fibonacci(n)
    elapsed = time.time() - start_time
    digit_count = len(result)
    print(f"F({n}):")
    print(f"  Time: {elapsed*1000:.2f} ms")
    print(f"  Digits: {digit_count}")
    print(f"  First 50: {result[:50]}...")
    print(f"  Last 50:  ...{result[-50:]}")

# Test 7: Digit count function
print("\nTest 7: Digit count function")
print("-" * 60)
for n in [1000, 10000, 100000, 1000000]:
    start_time = time.time()
    digit_count = ff.fibonacci_digit_count(n)
    elapsed = time.time() - start_time
    print(f"F({n}) has {digit_count} digits (computed in {elapsed*1000:.2f} ms)")

# Test 8: CPU info
print("\nTest 8: System information")
print("-" * 60)
num_cores = ff.get_num_cores()
print(f"Available CPU cores: {num_cores}")
print(f"Method: {ff.METHOD}")
print(f"Version: {ff.__version__}")

print("\n✓ All tests completed successfully!")

