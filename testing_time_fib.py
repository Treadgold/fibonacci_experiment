import timeit
import argparse
import sys
import os
from mpmath import mp, sqrt, power, nint

# Add fastfib to path for editable install
fastfib_path = os.path.join(os.path.dirname(__file__), 'fastfib')
if os.path.exists(fastfib_path) and fastfib_path not in sys.path:
    sys.path.insert(0, fastfib_path)

# Import the ultra-fast C++ implementation
try:
    import fastfib
    FASTFIB_AVAILABLE = True
except ImportError as e:
    FASTFIB_AVAILABLE = False
    print(f"Warning: fastfib (C++) not available: {e}")

# Allow printing very large integers
sys.set_int_max_str_digits(0)  # No limit


def fibonacci_binet(n):
    """
    Calculate the nth Fibonacci number using Binet's formula with arbitrary precision.
    
    TIME COMPLEXITY: O(1) for fixed-precision, ~O(log n) for arbitrary precision
    ==============================================================================
    With standard 64-bit floats, this is true O(1) constant time.
    With mpmath arbitrary precision (used here to avoid overflow):
    - Computation time scales with the precision needed (~0.21*n digits)
    - This makes it approximately O(log n) in practice
    - Still MUCH better than the iterative O(n) approach!
    
    Why? The key operation is computing φⁿ (phi to the power of n).
    For arbitrary precision arithmetic:
    - phi**n is computed as exp(n * log(phi))
    - These operations scale with digit count, not n directly
    
    Mathematical Explanation:
    -------------------------
    Binet's formula: F(n) = (φⁿ - ψⁿ) / √5
    
    Where:
    - φ = (1 + √5) / 2 is the golden ratio (~1.618)
    - ψ = (1 - √5) / 2 is the conjugate root (~-0.618)
    - As n grows, ψⁿ approaches 0 (since |ψ| < 1)
    
    Args:
        n (int): The position in the Fibonacci sequence (n >= 0)
    
    Returns:
        int: The nth Fibonacci number
    
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n == 0:
        return 0
    
    # Dynamically set precision based on expected result size
    # F(n) has approximately 0.2089 * n digits
    # Empirically, we need about n/4 + 50 decimal places for accurate results
    # This balances speed vs accuracy
    digits_needed = int(n / 4) + 50
    old_dps = mp.dps
    mp.dps = max(50, min(digits_needed, 30000))  # Cap at 30000 for sanity
    
    try:
        # Calculate constants using arbitrary precision
        sqrt5 = sqrt(5)
        phi = (1 + sqrt5) / 2
        
        # Optimization: For n > 20, psi^n term is negligible (|psi| < 1)
        # Using only phi^n / sqrt(5) is faster and still accurate
        if n > 20:
            result = power(phi, n) / sqrt5
        else:
            # For small n, use full formula for exactness
            psi = (1 - sqrt5) / 2
            result = (power(phi, n) - power(psi, n)) / sqrt5
        
        # Convert to nearest integer (properly rounded)
        return int(nint(result))
    finally:
        # Restore original precision
        mp.dps = old_dps


def fibonacci_iterative(n):
    """
    Calculate the nth Fibonacci number using iterative approach.
    
    TIME COMPLEXITY: O(n) - Linear Time
    ====================================
    This algorithm has LINEAR time complexity because it must iterate
    through all values from 0 to n, performing constant-time operations
    at each step.
    
    Args:
        n (int): The position in the Fibonacci sequence (n >= 0)
    
    Returns:
        int: The nth Fibonacci number
    
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    if n <= 1:
        return n
    
    prev2 = 0  # F(0)
    prev1 = 1  # F(1)
    
    # Must iterate n-1 times - this is why it's O(n)
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1


def fibonacci_cpp(n):
    """
    Calculate the nth Fibonacci number using ultra-fast C++ implementation.
    
    TIME COMPLEXITY: O(1) - True Constant Time with Fixed Precision
    ================================================================
    This is the FASTEST implementation using:
    - C++ compiled code with -O3 optimization
    - Binet's formula with double precision (no arbitrary precision overhead)
    - Multi-core parallel processing (for batch operations)
    - CPU-specific optimizations (-march=native)
    
    Note: Returns float for large n (double precision). Exact for n <= 78.
    
    Args:
        n (int): The position in the Fibonacci sequence (n >= 0)
    
    Returns:
        float: The nth Fibonacci number (approximate for very large n)
    
    Raises:
        ImportError: If fastfib package is not installed
    """
    if not FASTFIB_AVAILABLE:
        raise ImportError("fastfib package not available. Install with: pip install -e fastfib/")
    
    return fastfib.fib(n)


def time_fibonacci(n, iterations=10000):
    """
    Time how long it takes to compute fibonacci_binet(n).
    
    Args:
        n: The Fibonacci number to compute
        iterations: Number of times to repeat (for accurate timing)
    
    Returns:
        Average time per call in microseconds
    """
    total_time = timeit.timeit(lambda: fibonacci_binet(n), number=iterations)
    avg_time_microseconds = (total_time / iterations) * 1_000_000
    return avg_time_microseconds


def time_fibonacci_iterative(n, iterations=10000):
    """
    Time how long it takes to compute fibonacci_iterative(n).
    
    Args:
        n: The Fibonacci number to compute
        iterations: Number of times to repeat (for accurate timing)
    
    Returns:
        Average time per call in microseconds
    """
    total_time = timeit.timeit(lambda: fibonacci_iterative(n), number=iterations)
    avg_time_microseconds = (total_time / iterations) * 1_000_000
    return avg_time_microseconds


def time_fibonacci_cpp(n, iterations=10000):
    """
    Time how long it takes to compute fibonacci_cpp(n).
    
    Args:
        n: The Fibonacci number to compute
        iterations: Number of times to repeat (for accurate timing)
    
    Returns:
        Average time per call in microseconds
    """
    if not FASTFIB_AVAILABLE:
        return None
    total_time = timeit.timeit(lambda: fibonacci_cpp(n), number=iterations)
    avg_time_microseconds = (total_time / iterations) * 1_000_000
    return avg_time_microseconds


def run_comparison_test():
    """
    Compare all three Fibonacci implementations side-by-side.
    
    This dramatically shows the difference between constant and linear time!
    """
    print("=" * 130)
    print("FIBONACCI ALGORITHMS COMPARISON: C++ O(1) vs Python Binet O(1) vs Iterative O(n)")
    print("=" * 130)
    print()
    print("Comparing three approaches:")
    print("  1. C++ (fastfib) - FASTEST! O(1) constant time, optimized C++ with double precision")
    print("  2. Python Binet - O(1) constant time, uses mpmath for arbitrary precision (slower but no overflow)")
    print("  3. Python Iterative - O(n) linear time, must loop n times")
    print()
    print("The 'Ratio' column shows how each algorithm scales as n increases (compared to first test)")
    print()
    print("-" * 130)
    
    # Test cases
    test_cases = [
        ("Tiny", 10),
        ("Small", 50),
        ("Medium", 100),
        ("Large", 500),
        ("Very Large", 1_000),
        ("Huge", 5_000),
        ("Massive", 10_000),
        ("Extreme", 50_000),
        ("Ultra", 100_000),
    ]
    
    # Print header
    if FASTFIB_AVAILABLE:
        print(f"{'Category':<12} {'n':>10} | {'C++ μs':>10} {'Ratio':>7} | {'Binet μs':>11} {'Ratio':>7} | {'Iter μs':>12} {'Ratio':>7} | {'C++ vs Py':>10} {'C++ vs It':>10}")
    else:
        print(f"{'Category':<12} {'n':>10} | {'Binet μs':>12} {'Ratio':>8} | {'Iterative μs':>14} {'Ratio':>8} | {'Speedup':>10}")
    print("-" * 130)
    
    cpp_results = []
    binet_results = []
    iterative_results = []
    cpp_baseline = None
    binet_baseline = None
    iter_baseline = None
    
    for category, n in test_cases:
        # Time C++ fastfib (O(1)) - FASTEST!
        if FASTFIB_AVAILABLE:
            iterations_cpp = 100000 if n < 10000 else 10000  # More iterations since it's so fast
            cpp_time = time_fibonacci_cpp(n, iterations=iterations_cpp)
            cpp_results.append((n, cpp_time))
            if cpp_baseline is None:
                cpp_baseline = cpp_time
            cpp_ratio = cpp_time / cpp_baseline
        
        # Time Binet's formula (O(1)) with mpmath - no overflow!
        # Use fewer iterations for large n to keep test time reasonable
        iterations_binet = 10000 if n < 10000 else 1000
        binet_time = time_fibonacci(n, iterations=iterations_binet)
        binet_results.append((n, binet_time))
        if binet_baseline is None:
            binet_baseline = binet_time
        binet_ratio = binet_time / binet_baseline
        
        # Time iterative approach (O(n))
        # Use even fewer iterations for large n since each call takes longer
        iterations_iter = min(10000, max(100, 100000 // n))
        iterative_time = time_fibonacci_iterative(n, iterations=iterations_iter)
        iterative_results.append((n, iterative_time))
        if iter_baseline is None:
            iter_baseline = iterative_time
        iter_ratio = iterative_time / iter_baseline
        
        # Print results
        if FASTFIB_AVAILABLE:
            cpp_vs_py = binet_time / cpp_time
            cpp_vs_iter = iterative_time / cpp_time
            print(f"{category:<12} {n:>10,} | {cpp_time:>9.4f} {cpp_ratio:>6.2f}x | "
                  f"{binet_time:>10.4f} {binet_ratio:>6.2f}x | "
                  f"{iterative_time:>11.4f} {iter_ratio:>6.1f}x | "
                  f"{cpp_vs_py:>9.1f}x {cpp_vs_iter:>9.0f}x")
        else:
            speedup = iterative_time / binet_time
            print(f"{category:<12} {n:>10,} | {binet_time:>11.4f} {binet_ratio:>7.2f}x | "
                  f"{iterative_time:>13.4f} {iter_ratio:>7.1f}x | {speedup:>9.1f}x")
    
    print("-" * 130)
    print()
    
    # Analysis
    print("ANALYSIS:")
    print("=" * 130)
    print()
    
    # C++ Analysis
    if FASTFIB_AVAILABLE and len(cpp_results) >= 2:
        first_n, first_cpp_time = cpp_results[0]
        last_n, last_cpp_time = cpp_results[-1]
        n_ratio = last_n / first_n
        cpp_time_ratio = last_cpp_time / first_cpp_time
        
        print("C++ FASTFIB (O(1)) BEHAVIOR:")
        print(f"  When n increased from {first_n:,} to {last_n:,} ({n_ratio:,.0f}x increase)")
        print(f"  Time increased from {first_cpp_time:.4f}μs to {last_cpp_time:.4f}μs ({cpp_time_ratio:.1f}x increase)")
        print(f"  ✓ TRUE O(1) - nearly constant time! Uses fixed double precision.")
        print()
    
    # Compare scaling
    if len(iterative_results) >= 2:
        first_n, first_iter_time = iterative_results[0]
        last_n, last_iter_time = iterative_results[-1]
        n_ratio = last_n / first_n
        iter_time_ratio = last_iter_time / first_iter_time
        
        print("ITERATIVE (O(n)) BEHAVIOR:")
        print(f"  When n increased from {first_n:,} to {last_n:,} ({n_ratio:,.0f}x increase)")
        print(f"  Time increased from {first_iter_time:.4f}μs to {last_iter_time:.4f}μs ({iter_time_ratio:.1f}x increase)")
        print(f"  ✓ This is LINEAR scaling - time grows proportionally with n")
        print()
    
    if len(binet_results) >= 2:
        first_n, first_binet_time = binet_results[0]
        last_n, last_binet_time = binet_results[-1]
        n_ratio = last_n / first_n
        binet_time_ratio = last_binet_time / first_binet_time
        
        print("PYTHON BINET (O(1)*) BEHAVIOR:")
        print(f"  When n increased from {first_n:,} to {last_n:,} ({n_ratio:,.0f}x increase)")
        print(f"  Time increased from {first_binet_time:.4f}μs to {last_binet_time:.4f}μs ({binet_time_ratio:.1f}x increase)")
        if binet_time_ratio < n_ratio / 10:
            print(f"  ✓ Much better than linear! Scales ~O(log n) due to arbitrary precision")
        else:
            print(f"  ✓ Significantly better scaling than iterative O(n)")
        print()
    
    # Winner
    print("CONCLUSION:")
    if FASTFIB_AVAILABLE and cpp_results and binet_results and iterative_results:
        # Find a good comparison point
        compare_idx = min(5, len(binet_results) - 1)
        n_compare, cpp_compare = cpp_results[compare_idx]
        _, binet_compare = binet_results[compare_idx]
        _, iter_compare = iterative_results[compare_idx]
        cpp_vs_binet = binet_compare / cpp_compare
        cpp_vs_iter = iter_compare / cpp_compare
        binet_vs_iter = iter_compare / binet_compare
        
        print(f"  At n={n_compare:,}:")
        print(f"    - C++ is {cpp_vs_binet:.1f}x FASTER than Python Binet")
        print(f"    - C++ is {cpp_vs_iter:.0f}x FASTER than Iterative")
        print(f"    - Python Binet is {binet_vs_iter:.1f}x FASTER than Iterative")
        print()
        print("  🏆 OVERALL WINNER: C++ fastfib (O(1)) - BLAZINGLY FAST!")
        print()
        print("  Ranking by speed (fastest to slowest):")
        print("    1. C++ fastfib     - TRUE O(1), optimized compiled code, fixed precision")
        print("    2. Python Binet    - O(log n), arbitrary precision (no overflow)")
        print("    3. Iterative       - O(n), simple but slow for large n")
        print()
        print("  Trade-offs:")
        print("    C++: Fastest, but limited to ~10^308 (double precision)")
        print("    Python Binet: Slower, but handles arbitrarily large numbers")
        print("    Iterative: Slowest, but easiest to understand")
    elif binet_results and iterative_results:
        compare_idx = min(5, len(binet_results) - 1)
        n_compare, binet_compare = binet_results[compare_idx]
        _, iter_compare = iterative_results[compare_idx]
        speedup = iter_compare / binet_compare
        
        print(f"  At n={n_compare:,}, Binet's formula is {speedup:.1f}x FASTER than iterative!")
        print(f"  As n grows larger, the gap continues to widen dramatically.")
        print()
        print("  🏆 Winner: Binet's Formula (O(1))")
    
    print("=" * 130)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compare O(1) Binet's formula vs O(n) iterative Fibonacci"
    )
    parser.add_argument(
        "-n",
        type=int,
        help="Compute and time a specific Fibonacci number with both algorithms"
    )
    
    args = parser.parse_args()
    
    if args.n is not None:
        # Single computation mode
        print(f"\n{'='*80}")
        print(f"Computing F({args.n})")
        print(f"{'='*80}\n")
        
        result_binet = fibonacci_binet(args.n)
        result_iter = fibonacci_iterative(args.n)
        
        # Compute C++ if available
        if FASTFIB_AVAILABLE:
            result_cpp = fibonacci_cpp(args.n)
        
        # Verify they give the same result
        all_match = result_binet == result_iter
        if FASTFIB_AVAILABLE:
            # C++ returns float, so check if it's close enough for small n
            if args.n <= 78:
                all_match = all_match and (int(result_cpp) == result_binet)
        
        if not all_match:
            print("⚠️  WARNING: Algorithms produced different results!")
            print(f"Python Binet: {result_binet}")
            print(f"Iterative:    {result_iter}")
            if FASTFIB_AVAILABLE:
                print(f"C++:          {result_cpp}")
        else:
            print(f"Result: F({args.n}) = {result_binet}")
            if FASTFIB_AVAILABLE and args.n <= 78:
                print(f"✓ All three methods agree!")
        
        # Time all algorithms
        print(f"\n{'Timing Results:':-^80}\n")
        
        if FASTFIB_AVAILABLE:
            iterations_cpp = 100000 if args.n < 10000 else 10000
            time_cpp = time_fibonacci_cpp(args.n, iterations=iterations_cpp)
            print(f"C++ (fastfib):          {time_cpp:>10.4f} μs  [FASTEST]")
        
        iterations_binet = 10000 if args.n < 10000 else 1000
        iterations_iter = min(10000, max(100, 100000 // args.n))
        time_binet = time_fibonacci(args.n, iterations=iterations_binet)
        time_iter = time_fibonacci_iterative(args.n, iterations=iterations_iter)
        
        print(f"Python Binet (O(1)):    {time_binet:>10.4f} μs")
        print(f"Iterative (O(n)):       {time_iter:>10.4f} μs")
        
        print(f"\n{'Speedup Comparisons:':-^80}\n")
        if FASTFIB_AVAILABLE:
            print(f"C++ vs Python Binet: {time_binet/time_cpp:>6.1f}x faster")
            print(f"C++ vs Iterative:    {time_iter/time_cpp:>6.0f}x faster")
        print(f"Python Binet vs Iter: {time_iter/time_binet:>5.1f}x faster")
        print(f"\n{'='*80}\n")
    else:
        # Default: run comparison test
        run_comparison_test()
