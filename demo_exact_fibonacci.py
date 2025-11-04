#!/usr/bin/env python3
"""
Demonstration of exact Fibonacci computation with GMP
Shows the power of arbitrary precision arithmetic
"""

import fastfib
import time

print("=" * 70)
print("EXACT FIBONACCI COMPUTATION WITH GMP")
print("=" * 70)
try:
    from fastfib import _fastfib
    print(f"Version: {_fastfib.__version__}")
    print(f"Method: {_fastfib.METHOD}")
except:
    print("Version: 2.0.0")
    print("Method: Matrix Exponentiation with GMP")
print(f"Cores: {fastfib.get_num_cores()}")
print()

# Demo 1: Small values (show exact integers)
print("Demo 1: Small Fibonacci Numbers (Exact Values)")
print("-" * 70)
for n in [10, 50, 100]:
    value = fastfib.fib_int(n)
    print(f"F({n:>3}) = {value}")
print()

# Demo 2: Large values (show string representation)
print("Demo 2: Large Fibonacci Numbers")
print("-" * 70)
for n in [1000, 5000, 10000]:
    start = time.time()
    value = fastfib.fib(n)
    elapsed = (time.time() - start) * 1000
    digits = len(value)
    print(f"F({n:>5}) = {value[:40]}...{value[-40:]}")
    print(f"         ({digits:>5} digits, computed in {elapsed:.2f} ms)")
    print()

# Demo 3: Very large values
print("Demo 3: VERY Large Fibonacci Numbers")
print("-" * 70)
huge_values = [100000, 500000, 1000000]
for n in huge_values:
    print(f"Computing F({n:,})...", end=" ", flush=True)
    start = time.time()
    value = fastfib.fib(n)
    elapsed = (time.time() - start) * 1000
    digits = len(value)
    print(f"✓ {elapsed:.0f} ms")
    print(f"  Digits: {digits:,}")
    print(f"  First 50: {value[:50]}...")
    print(f"  Last 50:  ...{value[-50:]}")
    print()

# Demo 4: Range computation (parallel)
print("Demo 4: Parallel Range Computation")
print("-" * 70)
ranges = [(1, 100), (1, 1000), (1, 10000)]
for start, end in ranges:
    count = end - start + 1
    print(f"Computing F({start}) to F({end}) ({count:,} values)...", end=" ", flush=True)
    t0 = time.time()
    results = fastfib.fib_range(start, end)
    elapsed = time.time() - t0
    speed = count / elapsed
    print(f"✓ {elapsed:.3f}s ({speed:.0f} values/sec)")
    last_digits = len(results[-1])
    print(f"  F({end}) has {last_digits:,} digits")
print()

# Demo 5: Digit count (fast check without computing)
print("Demo 5: Digit Count (without computing full value)")
print("-" * 70)
check_values = [10000, 100000, 1000000, 10000000]
for n in check_values:
    start = time.time()
    digits = fastfib.digit_count(n)
    elapsed = (time.time() - start) * 1000
    print(f"F({n:>9,}) has {digits:>9,} digits (checked in {elapsed:.2f} ms)")
print()

# Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("✓ All Fibonacci values are EXACT (no approximation)")
print("✓ No overflow - works for arbitrarily large n")
print("✓ Fast O(log n) matrix exponentiation algorithm")
print(f"✓ Parallel computation using {fastfib.get_num_cores()} CPU cores")
print()
print("Try it yourself:")
print("  import fastfib")
print("  print(fastfib.fib(100))  # Exact 21-digit number")
print("  print(fastfib.fib(1000000))  # Exact 208,988-digit number!")
print("=" * 70)

