#!/usr/bin/env python3
"""
Quick demo of fastfib package
"""

import fastfib
import time
import numpy as np

print("=" * 70)
print("FastFib - Ultra-Fast Fibonacci Computation Demo")
print("=" * 70)
print()

# Show package info
print("Package Information:")
print(f"  Version: {fastfib.__version__}")
print(f"  CPU Cores: {fastfib.get_num_cores()}")
print(f"  Golden Ratio (φ): {fastfib.PHI:.10f}")
print()

# Demo 1: Single values
print("Demo 1: Computing Single Fibonacci Numbers")
print("-" * 70)
for n in [0, 1, 5, 10, 20, 50, 100]:
    result = fastfib.fib(n)
    print(f"  F({n:3d}) = {result:>20.3e}" if n > 50 else f"  F({n:3d}) = {int(result):>20}")
print()

# Demo 2: Range as list
print("Demo 2: Computing a Range (Python List)")
print("-" * 70)
fibs = fastfib.fib_range(10, 20)
print(f"  F(10) through F(20):")
print(f"  {[int(x) for x in fibs]}")
print()

# Demo 3: Range as NumPy array
print("Demo 3: Computing a Range (NumPy Array)")
print("-" * 70)
arr = fastfib.fib_array(1, 15)
print(f"  F(1) through F(15):")
print(f"  {arr.astype(int)}")
print()

# Demo 4: Large-scale computation
print("Demo 4: Large-Scale Performance")
print("-" * 70)

test_sizes = [10_000, 100_000, 1_000_000, 10_000_000]

for size in test_sizes:
    start = time.time()
    arr = fastfib.fib_array(1, size)
    elapsed = time.time() - start
    speed = size / elapsed
    
    print(f"  {size:>12,} values: {elapsed*1000:>8.2f} ms  ({speed:>15,.0f} values/sec)")

print()

# Demo 5: Verifying convergence to golden ratio
print("Demo 5: Fibonacci Ratios Converge to φ (Golden Ratio)")
print("-" * 70)
fibs = fastfib.fib_array(40, 50)
ratios = fibs[1:] / fibs[:-1]

for i, ratio in enumerate(ratios, start=40):
    error = abs(ratio - fastfib.PHI)
    print(f"  F({i+1})/F({i}) = {ratio:.12f}  (error: {error:.2e})")

print(f"\n  Golden ratio φ = {fastfib.PHI:.12f}")
print()

# Demo 6: Multi-threading comparison
print("Demo 6: Multi-Threading Speedup")
print("-" * 70)
n = 1_000_000

times = {}
for threads in [1, 2, 4, 8, 16, 24]:
    if threads <= fastfib.get_num_cores():
        start = time.time()
        arr = fastfib.fib_array(1, n, num_threads=threads)
        elapsed = time.time() - start
        times[threads] = elapsed
        speedup = times[1] / elapsed if threads > 1 else 1.0
        print(f"  {threads:2d} thread(s): {elapsed*1000:>8.2f} ms  (speedup: {speedup:>5.2f}x)")

print()

# Demo 7: Memory efficiency
print("Demo 7: Memory Efficiency")
print("-" * 70)
arr = fastfib.fib_array(1, 10_000_000)
memory_mb = arr.nbytes / (1024 * 1024)
print(f"  10 million Fibonacci numbers")
print(f"  Memory used: {memory_mb:.2f} MB")
print(f"  Storage efficiency: {arr.nbytes / len(arr):.1f} bytes/value")
print()

# Summary
print("=" * 70)
print("Summary:")
print("  ✓ Simple API: fastfib.fib(n)")
print("  ✓ Fast: ~400-500 million computations/second")
print("  ✓ Parallel: Uses all CPU cores efficiently")
print("  ✓ NumPy integration: Returns arrays for data science")
print("  ✓ Memory efficient: Direct computation, minimal overhead")
print("=" * 70)
print()
print("Try it yourself:")
print("  >>> import fastfib")
print("  >>> fastfib.fib(100)")
print("  3.542248481792619e+20")
print()

