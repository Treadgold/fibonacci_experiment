# Quick Start Guide

## Build Everything

```bash
make          # Build all programs
make clean    # Clean build artifacts
make info     # Show compiler and system info
```

## Run Programs

### Main Program (200M Fibonacci computations)
```bash
./fib_stairs
```

**Expected output:**
```
=== Ultra-Fast Parallel Fibonacci Computation ===
Using Binet's Formula: F(n) ≈ φ^n / √5

Using 24 CPU cores
Computing F(n) for n = 3 to 200000000 (fast mode)

=== Results ===
Total computed: 199999998 Fibonacci numbers
Time elapsed: ~100-200 ms
Speed: ~1-2 billion computations/second
```

### Verification Program
```bash
make test
# or
./verify
```

Shows accuracy comparison between Binet and exact iteration for small n.

### Comprehensive Benchmark
```bash
make benchmark
```

Runs full test suite including verification and thread scaling tests.

## Customization

### Edit fib_stairs.cpp

**Change the computation range:**
```cpp
const long long START_N = 3;
const long long END_N = 200000000;  // Change this
```

**Choose computation mode** (in `main()` function):

```cpp
// Mode 1: Compute with sum and show some results
compute_fibonacci_range_sum(START_N, END_N);

// Mode 2: Maximum speed (default)
compute_fibonacci_range_fast(START_N, END_N);

// Mode 3: Compute and store all results
std::vector<double> results;
compute_and_store_fibonacci(START_N, END_N, results);
```

### Control Thread Count

**Using environment variable:**
```bash
export OMP_NUM_THREADS=8
./fib_stairs
```

**Or modify in code:**
```cpp
omp_set_num_threads(8);  // Use 8 threads
```

## Performance Tips

1. **For maximum speed:** Use Mode 2 (fast mode) - it computes without storing
2. **For analysis:** Use Mode 1 to see sample results and sums
3. **For further processing:** Use Mode 3 to store results in memory
4. **Best thread count:** Usually equals your CPU core count (default)
5. **Compile flags:** Already optimized with `-O3 -march=native -flto`

## Understanding Results

### What does it compute?
For each n from 3 to 200,000,000, it calculates:
```
F(n) = φ^n / √5
```
where φ = (1 + √5) / 2 ≈ 1.618 (the golden ratio)

### Why so fast?
- **O(1) per computation:** Direct formula, no iteration
- **Parallel:** All CPU cores working simultaneously
- **Optimized math:** Using `exp(n × ln(φ))` instead of `pow(φ, n)`
- **No storage overhead:** Results computed on-the-fly in fast mode

### Accuracy notes
- **Exact:** For F(n) where n ≤ 78 (fits in uint64)
- **Approximate:** For larger n (uses double precision)
- **Purpose:** Great for analysis, pattern recognition, or when exact large integers aren't needed

## System Requirements

- **Compiler:** GCC 7+ or Clang 6+ with C++17 support
- **OpenMP:** For parallel processing
- **Memory:** Minimal (~MB for program, ~1.6GB if storing 200M results)
- **CPU:** Any modern CPU (optimizes for your specific architecture)

## Quick Commands Reference

```bash
make           # Build everything
make run       # Build and run main program
make test      # Build and run verification
make benchmark # Run full benchmark suite
make clean     # Remove executables
make info      # Show build configuration
make debug     # Build with debug symbols
```

## Example: Custom Range

Want to compute F(1000) to F(2000)?

1. Edit `fib_stairs.cpp`:
```cpp
const long long START_N = 1000;
const long long END_N = 2000;
```

2. Rebuild and run:
```bash
make clean && make run
```

## Troubleshooting

**"Command not found: g++"**
```bash
sudo apt install build-essential
```

**"OpenMP not found"**
- Usually included with GCC
- On macOS: `brew install libomp`

**Wrong thread count shown**
- Check: `echo $OMP_NUM_THREADS`
- Unset: `unset OMP_NUM_THREADS`
- Let OpenMP auto-detect (default behavior)

**Program too fast to measure**
- This is normal! Computing 200M Fibonacci numbers in ~100ms
- For longer runs, increase END_N

## Files Overview

- `fib_stairs.cpp` - Main ultra-fast parallel program
- `verify.cpp` - Accuracy verification and comparison
- `Makefile` - Build configuration
- `benchmark.sh` - Automated benchmark suite
- `README.md` - Detailed documentation
- `USAGE.md` - This quick start guide

---

**Ready to go!** Just run `make benchmark` to see everything in action.

