# FastFib Python Package - Complete Usage Guide

## Installation

```bash
cd /home/mike/code/play/fastfib
pip install -e .
```

Or install from PyPI (when published):
```bash
pip install fastfib
```

## Quick Start

### Basic Usage

```python
import fastfib

# Single Fibonacci number
print(fastfib.fib(10))          # 55.0
print(fastfib.fib(100))         # 3.542248481792619e+20

# Range as Python list
fibs = fastfib.fib_range(10, 20)
print(fibs)  # [55.0, 89.0, 144.0, ...]

# Range as NumPy array (faster for large ranges)
import numpy as np
arr = fastfib.fib_array(1, 100)
print(arr)  # array([1., 1., 2., 3., 5., ...])
```

## API Reference

### Main Functions

#### `fastfib.fib(n)` 
Compute single Fibonacci number.

```python
>>> fastfib.fib(10)
55.0
>>> fastfib.fib(50)
12586269025.0
>>> fastfib.fib(100)
3.542248481792619e+20
```

**Parameters:**
- `n` (int): Non-negative integer index

**Returns:**
- `float`: The nth Fibonacci number

---

#### `fastfib.fib_range(start, end, num_threads=-1)`
Compute range of Fibonacci numbers (returns list).

```python
>>> fastfib.fib_range(10, 15)
[55.0, 89.0, 144.0, 233.0, 377.0, 610.0]

>>> fastfib.fib_range(1, 10, num_threads=4)  # Use 4 cores
[1.0, 1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0, 55.0]
```

**Parameters:**
- `start` (int): Starting index
- `end` (int): Ending index (inclusive)
- `num_threads` (int, optional): Number of CPU cores (-1 = all)

**Returns:**
- `list[float]`: List of Fibonacci numbers

---

#### `fastfib.fib_array(start, end, num_threads=-1)`
Compute range of Fibonacci numbers (returns NumPy array).

```python
>>> import numpy as np
>>> arr = fastfib.fib_array(1, 10)
>>> arr
array([ 1.,  1.,  2.,  3.,  5.,  8., 13., 21., 34., 55.])

>>> arr.dtype
dtype('float64')
```

**Parameters:**
- `start` (int): Starting index
- `end` (int): Ending index (inclusive)
- `num_threads` (int, optional): Number of CPU cores (-1 = all)

**Returns:**
- `numpy.ndarray`: NumPy array of Fibonacci numbers

---

### Utility Functions

#### `fastfib.get_num_cores()`
Get available CPU cores.

```python
>>> fastfib.get_num_cores()
24
```

#### `fastfib.set_num_threads(n)`
Set number of threads globally.

```python
>>> fastfib.set_num_threads(8)  # Use 8 cores
>>> arr = fastfib.fib_array(1, 1000000)
```

#### `fastfib.get_phi()`
Get the golden ratio.

```python
>>> fastfib.get_phi()
1.618033988749895
```

#### `fastfib.info()`
Display package information.

```python
>>> fastfib.info()
FastFib v1.0.0
Available CPU cores: 24
Golden ratio (φ): 1.618033988749895

Compute Fibonacci numbers at ~1+ billion/second!

Usage:
  fastfib.fib(n)              - Single Fibonacci number
  fastfib.fib_range(a, b)     - Range as Python list
  fastfib.fib_array(a, b)     - Range as NumPy array
```

---

### Constants

```python
>>> fastfib.PHI
1.618033988749895

>>> fastfib.SQRT5
2.23606797749979

>>> fastfib.__version__
'1.0.0'
```

## Real-World Examples

### Example 1: Data Analysis

```python
import fastfib
import numpy as np
import matplotlib.pyplot as plt

# Generate Fibonacci sequence
fibs = fastfib.fib_array(1, 50)

# Compute ratios (approaches φ)
ratios = fibs[1:] / fibs[:-1]

# Plot convergence
plt.figure(figsize=(10, 6))
plt.plot(ratios, marker='o')
plt.axhline(y=fastfib.PHI, color='r', linestyle='--', label='Golden Ratio')
plt.xlabel('n')
plt.ylabel('F(n+1) / F(n)')
plt.title('Fibonacci Ratios Converge to φ')
plt.legend()
plt.grid(True)
plt.show()
```

### Example 2: Large-Scale Computation

```python
import fastfib
import time

# Compute 100 million Fibonacci numbers
print("Computing 100 million Fibonacci numbers...")
start = time.time()
arr = fastfib.fib_array(1, 100_000_000)
elapsed = time.time() - start

print(f"Time: {elapsed:.2f} seconds")
print(f"Speed: {len(arr)/elapsed:,.0f} values/second")
print(f"Memory: {arr.nbytes / (1024**2):.1f} MB")

# Statistics
print(f"Max: {arr.max():.3e}")
print(f"Sum: {arr.sum():.3e}")
```

### Example 3: Performance Comparison

```python
import fastfib
import time

def fib_python_iterative(n):
    """Traditional iterative Python implementation"""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Compare performance
n = 10000

# Pure Python
start = time.time()
py_results = [fib_python_iterative(i) for i in range(1, n+1)]
py_time = time.time() - start

# FastFib
start = time.time()
ff_results = fastfib.fib_range(1, n)
ff_time = time.time() - start

print(f"Pure Python: {py_time:.3f}s")
print(f"FastFib: {ff_time:.3f}s")
print(f"Speedup: {py_time/ff_time:.1f}x faster!")
```

### Example 4: Scientific Computing

```python
import fastfib
import numpy as np

# Generate Fibonacci numbers
fibs = fastfib.fib_array(1, 100)

# Convert to logarithmic scale (for large numbers)
log_fibs = np.log10(fibs)

# Verify Binet's formula: log(F(n)) ≈ n × log(φ) - log(√5)
n = np.arange(1, 101)
expected = n * np.log10(fastfib.PHI) - np.log10(fastfib.SQRT5)

# Compare
error = np.abs(log_fibs - expected)
print(f"Average error: {error.mean():.6f}")
print(f"Max error: {error.max():.6f}")
```

### Example 5: Parallel Processing Control

```python
import fastfib
import time

n = 1_000_000

# Test different thread counts
print("Thread scaling test:")
print(f"Computing {n:,} Fibonacci numbers\n")

for threads in [1, 2, 4, 8, 16]:
    if threads <= fastfib.get_num_cores():
        start = time.time()
        arr = fastfib.fib_array(1, n, num_threads=threads)
        elapsed = time.time() - start
        
        speedup = 1.0 if threads == 1 else (times[1] / elapsed)
        print(f"{threads:2d} threads: {elapsed*1000:>8.2f} ms  "
              f"(speedup: {speedup:>5.2f}x)")
        
        if threads == 1:
            times = {1: elapsed}
```

### Example 6: Integration with Pandas

```python
import fastfib
import pandas as pd
import numpy as np

# Create DataFrame with Fibonacci analysis
n_values = range(1, 51)
fibs = fastfib.fib_array(1, 50)

df = pd.DataFrame({
    'n': n_values,
    'F(n)': fibs,
    'log10(F(n))': np.log10(fibs),
    'F(n+1)/F(n)': np.concatenate([[np.nan], fibs[1:] / fibs[:-1]]),
})

# Calculate deviation from golden ratio
df['φ_error'] = np.abs(df['F(n+1)/F(n)'] - fastfib.PHI)

print(df.tail(10))
print(f"\nAverage φ error (last 10): {df['φ_error'].tail(10).mean():.2e}")
```

### Example 7: Error Handling

```python
import fastfib

try:
    # Invalid input (negative)
    result = fastfib.fib(-5)
except ValueError as e:
    print(f"Error: {e}")  # "n must be non-negative"

try:
    # Invalid range
    result = fastfib.fib_range(10, 5)
except ValueError as e:
    print(f"Error: {e}")  # "start must be <= end"

try:
    # Invalid thread count
    fastfib.set_num_threads(0)
except ValueError as e:
    print(f"Error: {e}")  # "Number of threads must be positive"
```

## Performance Tips

### 1. Use `fib_array()` for Large Ranges
```python
# Slower (list overhead)
fibs = fastfib.fib_range(1, 1000000)

# Faster (direct NumPy array)
fibs = fastfib.fib_array(1, 1000000)
```

### 2. Let OpenMP Auto-Detect Threads
```python
# Usually optimal (uses all cores)
arr = fastfib.fib_array(1, 1000000)

# Manual control only if needed
arr = fastfib.fib_array(1, 1000000, num_threads=8)
```

### 3. Batch Operations
```python
# Less efficient (many function calls)
fibs = [fastfib.fib(i) for i in range(1, 10001)]

# More efficient (single call)
fibs = fastfib.fib_array(1, 10000)
```

### 4. Memory Management
```python
# For very large ranges, process in chunks
chunk_size = 10_000_000
for start in range(1, 100_000_001, chunk_size):
    end = min(start + chunk_size - 1, 100_000_000)
    chunk = fastfib.fib_array(start, end)
    # Process chunk...
    del chunk  # Free memory
```

## Precision Notes

- **Exact integers**: n ≤ 78 (fits in uint64)
- **Double precision**: n > 78 (uses 64-bit float)
- **Practical limit**: n ≤ ~10^6 (before floating-point overflow)

For exact arbitrary-precision integers, use Python's built-in or libraries like `gmpy2` (much slower).

## Troubleshooting

### Import Error
```python
ModuleNotFoundError: No module named 'fastfib'
```
**Solution:** Install the package: `pip install -e .`

### OpenMP Not Found
```
error: unsupported option '-fopenmp'
```
**Solution:** Install OpenMP support (usually included with GCC)

### Slow Performance
```python
# Check thread count
print(fastfib.get_num_cores())  # Should show all cores

# Verify OpenMP is working
import os
print(os.environ.get('OMP_NUM_THREADS', 'auto'))
```

## Advanced Topics

### Understanding Binet's Formula

The package uses Binet's formula:
```
F(n) = (φ^n - ψ^n) / √5
```

Where:
- φ = (1 + √5) / 2 ≈ 1.618 (golden ratio)
- ψ = (1 - √5) / 2 ≈ -0.618

For large n, ψ^n → 0, so:
```
F(n) ≈ φ^n / √5 = exp(n × ln(φ)) / √5
```

This gives O(1) time complexity!

### Thread Scaling

Expected speedup with N threads:
- **Ideal**: N×
- **Typical**: 0.8-0.95 × N
- **Factors**: Memory bandwidth, cache, OS overhead

### Memory Layout

NumPy arrays are stored contiguously:
```python
arr = fastfib.fib_array(1, 100)
print(arr.flags)  # Shows C_CONTIGUOUS = True
```

This enables:
- Fast iteration
- Efficient slicing
- SIMD operations

## Support & Contributing

- **GitHub**: (add your repo URL)
- **Issues**: Report bugs or request features
- **Documentation**: This guide and README.md

## See Also

- [README.md](README.md) - Package overview
- [demo.py](demo.py) - Interactive demo
- [test_fastfib.py](test_fastfib.py) - Test suite

---

**Happy computing!** 🚀

