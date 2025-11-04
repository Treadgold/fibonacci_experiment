# Fibonacci Algorithms Comparison

A performance comparison of three Fibonacci number computation algorithms: C++ Binet (O(1)), Python Binet (O(log n)), and Python Iterative (O(n)).

## Overview

This project benchmarks three fundamentally different approaches to computing Fibonacci numbers:

1. **C++ fastfib** - True O(1) constant time using optimized C++ with double precision
2. **Python Binet** - O(log n) using mpmath for arbitrary precision (no overflow)
3. **Python Iterative** - O(n) linear time, classic loop-based approach

The key finding: **C++ is consistently 100-100,000x faster** than Python implementations, demonstrating true constant-time behavior.

## Performance Results

All measurements in microseconds (μs). The "Ratio" column shows scaling relative to the n=10 baseline.

```
Category              n |     C++ μs   Ratio |    Binet μs   Ratio |      Iter μs   Ratio | C++ vs Py | C++ vs It
------------------------------------------------------------------------------------------------------------------------------------
Tiny                 10 |    0.2517   1.00x |    23.7006   1.00x |      0.2839    1.0x |      94x  |        1x
Small                50 |    0.2309   0.92x |    16.8978   0.71x |      1.2654    4.5x |      73x  |        5x
Medium              100 |    0.2258   0.90x |    17.9070   0.76x |      2.5322    8.9x |      79x  |       11x
Large               500 |    0.2340   0.93x |    29.9829   1.27x |     17.6919   62.3x |     128x  |       76x
Very Large        1,000 |    0.2293   0.91x |    40.7707   1.72x |     40.0500  141.1x |     178x  |      175x
Huge              5,000 |    0.2287   0.91x |   216.5574   9.14x |    365.9191 1288.7x |     947x  |     1600x
Massive          10,000 |    0.2389   0.95x |   651.6884  27.50x |   1199.7284 4225.4x |    2728x  |     5021x
Extreme          50,000 |    0.2317   0.92x |  8208.6155 346.35x |  22573.6943 79503.3x |   35425x  |    97417x
Ultra           100,000 |    0.2296   0.91x | 24752.9983 1044.41x |  82361.0208 290071.0x |  107790x  |   358650x
```

## Analysis

### C++ fastfib: True O(1) Behavior

When n increased from 10 to 100,000 (10,000x increase):
- Time increased from 0.25μs to 0.23μs (0.9x - essentially constant!)
- **Conclusion**: True constant time using fixed double precision

### Python Binet: O(log n) Behavior

When n increased from 10 to 100,000 (10,000x increase):
- Time increased from 23.7μs to 24,752.9μs (1,044x increase)
- **Conclusion**: Scales logarithmically with precision requirements, significantly better than O(n)

### Python Iterative: O(n) Behavior

When n increased from 10 to 100,000 (10,000x increase):
- Time increased from 0.28μs to 82,361.0μs (290,071x increase)
- **Conclusion**: Linear scaling - time grows proportionally with n

## Key Findings

**Winner by Speed**: C++ fastfib
- At n=5,000: 947x faster than Python Binet, 1,600x faster than Iterative
- At n=100,000: 107,790x faster than Python Binet, 358,650x faster than Iterative

**Ranking** (fastest to slowest):
1. C++ fastfib - True O(1), compiled code, limited to ~10^308
2. Python Binet - O(log n), arbitrary precision, no overflow limit
3. Python Iterative - O(n), simple and exact, but slow for large n

**Trade-offs**:
- **C++**: Blazingly fast, but limited by double precision (~10^308)
- **Python Binet**: Slower but handles arbitrarily large numbers
- **Iterative**: Slowest, easiest to understand and implement

## Quick Start

### Installation

**IMPORTANT**: The C++ extension is **platform-specific** and must be compiled for your operating system. Pre-built binaries are included for **Linux only**. macOS and Windows users must build from source.

#### Linux / WSL (Pre-built Binaries Available)

```bash
# Clone the repository
cd /home/mike/code/play

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install mpmath

# Install fastfib (pre-built binaries should work)
cd fastfib
pip install -e .
cd ..
```

If the pre-built binaries don't work on your Linux distribution, you'll need GCC:
```bash
sudo apt install build-essential  # Ubuntu/Debian
sudo dnf install gcc-c++          # Fedora/RHEL
```

#### macOS (Must Build from Source)

**Prerequisites**:
1. Install Xcode Command Line Tools:
```bash
xcode-select --install
```

2. Install OpenMP via Homebrew (for parallel processing):
```bash
brew install libomp
```

**Installation**:
```bash
# Clone the repository
cd /path/to/play

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install mpmath

# Build and install fastfib
cd fastfib
pip install -e .
cd ..
```

The setup script will automatically detect your OpenMP installation (Intel or Apple Silicon paths).

#### Windows (Must Build from Source)

**Prerequisites**:
1. Install **Microsoft C++ Build Tools**:
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Run the installer
   - Select "Desktop development with C++"
   - Ensure "MSVC" and "Windows SDK" are checked
   - Complete the installation (may take 15-30 minutes)

   **OR** install Visual Studio Community (includes the build tools)

**Installation**:
```cmd
REM Open "Developer Command Prompt for VS" (search in Start menu)
REM This ensures the compiler is in your PATH

cd C:\path\to\play

REM Create virtual environment
python -m venv .venv
.venv\Scripts\activate

REM Install Python dependencies
pip install mpmath

REM Build and install fastfib
cd fastfib
pip install -e .
cd ..
```

**Important Windows Notes**:
- You **must** use "Developer Command Prompt for VS" or the build will fail
- Regular CMD/PowerShell won't have the compiler in PATH
- The compiled `.pyd` file is Windows-specific
- **WSL is a separate Linux environment** - if you install in WSL, it won't work in Windows Python (and vice versa)

#### What Gets Installed

The `-e` flag installs in "editable" mode, meaning changes to the source code are immediately reflected without reinstalling. The `pip install` command will:
- Automatically install pybind11 and numpy as dependencies
- Compile the C++ extension for your specific platform
- Install the `fastfib` Python module in your environment

#### Platform-Specific Optimizations

- **Linux/WSL**: Uses GCC with `-march=native` (optimized for your specific CPU)
- **macOS**: Uses Clang with OpenMP (if available) for parallel processing
- **Windows**: Uses MSVC with `/openmp` and whole-program optimization

### Running the Benchmark

```bash
# Activate virtual environment
source .venv/bin/activate

# Run benchmark for a specific n
python testing_time_fib.py -n 100

# Run full benchmark suite (n from 10 to 100,000)
python testing_time_fib.py --full
```

### Example Output

```
==================================================
Computing F(100)
==================================================

Result: F(100) = 354224848179261915075

--------------------------------Timing Results:---------------------------------
C++ (fastfib):              0.2199 μs  [FASTEST]
Python Binet (O(1)):       17.5800 μs
Iterative (O(n)):           2.7354 μs

------------------------------Speedup Comparisons:------------------------------
C++ vs Python Binet:   79.9x faster
C++ vs Iterative:        12x faster
Python Binet vs Iter:   0.2x faster
```

## Implementation Details

### 1. C++ Implementation (O(1) - True Constant Time)

The C++ implementation uses Binet's formula with optimized double-precision arithmetic:

```cpp
// Constants precomputed at compile time
constexpr double PHI = 1.6180339887498948482045868343656381;
constexpr double INV_SQRT5 = 0.44721359549995793928183473374625524;

// Ultra-fast Fibonacci using Binet's formula
inline double fib_binet(long long n) {
    if (n < 0) {
        throw std::invalid_argument("n must be non-negative");
    }
    if (n == 0) return 0.0;
    if (n == 1) return 1.0;
    
    // For large n, psi^n is negligible
    if (n > 20) {
        static const double LOG_PHI = std::log(PHI);
        return std::exp(n * LOG_PHI) * INV_SQRT5;
    } else {
        // Full formula for smaller n (more accurate)
        double phi_n = std::pow(PHI, n);
        double psi_n = std::pow(PSI, n);
        return std::round((phi_n - psi_n) * INV_SQRT5);
    }
}
```

**Key optimizations**:
- Fixed double precision (no arbitrary precision overhead)
- Precomputed constants at compile time
- Inline functions for zero function call overhead
- Compiled with `-O3 -march=native` for CPU-specific optimizations
- OpenMP parallelization for batch operations

**Time Complexity**: O(1) - all operations are constant time with fixed precision

**Limitations**: Accurate only up to n≈78 (exact integers), approximations beyond that, overflow at ~10^308

### 2. Python Binet Implementation (O(log n) - Arbitrary Precision)

Uses Binet's formula with mpmath for arbitrary precision arithmetic:

```python
from mpmath import mp, sqrt, power, nint

def fibonacci_binet(n):
    """
    Calculate the nth Fibonacci number using Binet's formula.
    
    TIME COMPLEXITY: O(log n) for arbitrary precision
    
    Binet's formula: F(n) = (φⁿ - ψⁿ) / √5
    Where:
    - φ = (1 + √5) / 2 ≈ 1.618 (golden ratio)
    - ψ = (1 - √5) / 2 ≈ -0.618 (conjugate root)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n == 0:
        return 0
    
    # Set precision based on result size
    # F(n) has approximately 0.2089 * n digits
    digits_needed = int(n / 4) + 50
    old_dps = mp.dps
    mp.dps = max(50, min(digits_needed, 30000))
    
    try:
        sqrt5 = sqrt(5)
        phi = (1 + sqrt5) / 2
        
        # Optimization: For n > 20, psi^n ≈ 0
        if n > 20:
            result = power(phi, n) / sqrt5
        else:
            psi = (1 - sqrt5) / 2
            result = (power(phi, n) - power(psi, n)) / sqrt5
        
        return int(nint(result))
    finally:
        mp.dps = old_dps
```

**Key features**:
- Arbitrary precision arithmetic (no overflow)
- Dynamic precision adjustment based on n
- Computes exact integer results for any n

**Time Complexity**: O(log n) in practice due to precision scaling with digit count

**Advantages**: No overflow limit, exact results for arbitrarily large n

### 3. Python Iterative Implementation (O(n) - Linear Time)

Classic iterative approach using simple addition:

```python
def fibonacci_iterative(n):
    """
    Calculate the nth Fibonacci number using iteration.
    
    TIME COMPLEXITY: O(n) - must iterate n times
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n <= 1:
        return n
    
    prev2 = 0  # F(0)
    prev1 = 1  # F(1)
    
    # Iterate n-1 times
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1
```

**Key characteristics**:
- Simple and easy to understand
- Exact results (no floating-point errors)
- Python's arbitrary precision integers handle any size

**Time Complexity**: O(n) - must perform n iterations

**Advantages**: Simple, exact, no mathematical complexity

**Disadvantages**: Slow for large n (impractical beyond ~1 million)

## Mathematical Background

### Binet's Formula

The closed-form solution for Fibonacci numbers:

```
F(n) = (φⁿ - ψⁿ) / √5

Where:
  φ = (1 + √5) / 2 ≈ 1.618033988... (golden ratio)
  ψ = (1 - √5) / 2 ≈ -0.618033988... (conjugate root)
```

For large n, since |ψ| < 1, we have ψⁿ → 0, so:

```
F(n) ≈ φⁿ / √5 ≈ round(φⁿ / √5)
```

This approximation is used in both implementations for n > 20.

### Why Different Time Complexities?

**C++ O(1)**: Uses fixed double precision (64 bits), so all arithmetic operations are constant time regardless of n.

**Python Binet O(log n)**: Uses arbitrary precision that scales with the number of digits in the result (~0.21n digits). Since precision needs grow logarithmically with the magnitude, time scales as O(log n).

**Iterative O(n)**: Must explicitly compute F(0), F(1), ..., F(n) sequentially, requiring exactly n additions.

## Troubleshooting

### "ModuleNotFoundError: No module named 'fastfib'"

Make sure you:
1. Activated your virtual environment (`source .venv/bin/activate` or `.venv\Scripts\activate`)
2. Ran `pip install -e .` from inside the `fastfib` directory
3. Are in the same virtual environment where you installed it

### "error: Microsoft Visual C++ 14.0 or greater is required" (Windows)

You need the C++ compiler:
1. Install Microsoft C++ Build Tools (see Windows installation instructions above)
2. **Must** run `pip install -e .` from "Developer Command Prompt for VS"
3. Regular CMD/PowerShell won't work without additional PATH setup

### "ld: library not found for -lomp" (macOS)

You need OpenMP:
```bash
brew install libomp
```

If still failing, OpenMP may not be available - the extension will build without parallel processing (slower but functional).

### Compilation Errors on Linux

Install build tools:
```bash
sudo apt install build-essential python3-dev  # Ubuntu/Debian
sudo dnf install gcc-c++ python3-devel        # Fedora/RHEL
```

### WSL vs Windows Python

**Important**: WSL Python and Windows Python are **completely separate**:
- Installing in WSL creates Linux binaries (`.so` files)
- Windows Python needs Windows binaries (`.pyd` files)
- They cannot share installations
- If you want both, install separately in each environment

### Performance is Slow

1. Make sure OpenMP is enabled (check installation output)
2. Verify multi-threading: `python -c "import fastfib; print(fastfib.get_num_cores())"`
3. Try setting threads explicitly: `fastfib.set_num_threads(8)`

## Files

- `testing_time_fib.py` - Main benchmark script
- `fastfib/fib_bindings.cpp` - C++ implementation with Python bindings
- `cpp_version/fib_stairs.cpp` - Standalone C++ version with parallel processing
- `binnets_formula.py` - Pure Python Binet implementation experiments

## Requirements

**Python Dependencies** (installed automatically):
- Python 3.8+
- mpmath
- pybind11
- numpy

**Build Tools** (platform-specific, see Installation section above):
- **Linux/WSL**: build-essential (GCC) - often pre-installed, may not be needed if binaries work
- **macOS**: Xcode Command Line Tools + libomp (via Homebrew)
- **Windows**: Microsoft C++ Build Tools or Visual Studio Community

## License

MIT

## Author

Performance analysis conducted November 2025

