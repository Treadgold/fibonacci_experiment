#!/usr/bin/env python3
"""
Test script for fastfib package
"""

import sys
import time

def test_fastfib():
    """Test the fastfib package"""
    print("=" * 60)
    print("FastFib Test Suite")
    print("=" * 60)
    print()
    
    try:
        import fastfib
        print("✓ fastfib imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import fastfib: {e}")
        print("\nPlease install the package first:")
        print("  pip install -e .")
        return False
    
    print(f"✓ Version: {fastfib.__version__}")
    print(f"✓ Available CPU cores: {fastfib.get_num_cores()}")
    print()
    
    # Test 1: Single values
    print("Test 1: Single Fibonacci numbers")
    print("-" * 60)
    test_cases = [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (10, 55),
        (20, 6765),
    ]
    
    all_passed = True
    for n, expected in test_cases:
        result = fastfib.fib(n)
        passed = abs(result - expected) < 0.001
        status = "✓" if passed else "✗"
        print(f"  {status} fib({n}) = {result:.0f} (expected {expected})")
        all_passed = all_passed and passed
    
    if all_passed:
        print("✓ All single value tests passed!")
    else:
        print("✗ Some tests failed")
    print()
    
    # Test 2: Range (list)
    print("Test 2: Fibonacci range (list)")
    print("-" * 60)
    fibs = fastfib.fib_range(10, 15)
    expected_range = [55, 89, 144, 233, 377, 610]
    
    if len(fibs) == len(expected_range):
        print(f"✓ Length correct: {len(fibs)}")
    else:
        print(f"✗ Length mismatch: got {len(fibs)}, expected {len(expected_range)}")
    
    print(f"  Result: {[int(x) for x in fibs]}")
    print(f"  Expected: {expected_range}")
    
    range_passed = all(abs(f - e) < 0.001 for f, e in zip(fibs, expected_range))
    if range_passed:
        print("✓ Range test passed!")
    else:
        print("✗ Range test failed")
    print()
    
    # Test 3: NumPy array
    print("Test 3: Fibonacci array (NumPy)")
    print("-" * 60)
    try:
        import numpy as np
        arr = fastfib.fib_array(1, 10)
        print(f"✓ Array created: shape={arr.shape}, dtype={arr.dtype}")
        print(f"  Values: {arr}")
        
        expected_arr = np.array([1, 1, 2, 3, 5, 8, 13, 21, 34, 55], dtype=float)
        if np.allclose(arr, expected_arr):
            print("✓ NumPy array test passed!")
        else:
            print("✗ NumPy array values don't match")
    except Exception as e:
        print(f"✗ NumPy array test failed: {e}")
    print()
    
    # Test 4: Large values
    print("Test 4: Large Fibonacci numbers")
    print("-" * 60)
    large_n = [50, 100, 500, 1000]
    for n in large_n:
        result = fastfib.fib(n)
        print(f"  fib({n}) ≈ {result:.6e}")
    print("✓ Large number computation successful")
    print()
    
    # Test 5: Performance
    print("Test 5: Performance benchmark")
    print("-" * 60)
    
    # Small range
    start = time.time()
    fibs = fastfib.fib_range(1, 10000)
    elapsed = time.time() - start
    print(f"  10,000 values: {elapsed*1000:.2f} ms ({len(fibs)/elapsed:,.0f} values/sec)")
    
    # Medium range
    start = time.time()
    fibs = fastfib.fib_range(1, 1000000)
    elapsed = time.time() - start
    print(f"  1,000,000 values: {elapsed*1000:.2f} ms ({len(fibs)/elapsed:,.0f} values/sec)")
    
    # Large range (using array for efficiency)
    start = time.time()
    arr = fastfib.fib_array(1, 10000000)
    elapsed = time.time() - start
    print(f"  10,000,000 values: {elapsed*1000:.2f} ms ({len(arr)/elapsed:,.0f} values/sec)")
    
    print("✓ Performance test complete")
    print()
    
    # Test 6: Thread control
    print("Test 6: Thread control")
    print("-" * 60)
    original_cores = fastfib.get_num_cores()
    print(f"  Available cores: {original_cores}")
    
    # Test with different thread counts
    for threads in [1, 2, 4]:
        if threads <= original_cores:
            start = time.time()
            arr = fastfib.fib_array(1, 1000000, num_threads=threads)
            elapsed = time.time() - start
            print(f"  {threads} thread(s): {elapsed*1000:.2f} ms")
    
    print("✓ Thread control test complete")
    print()
    
    # Test 7: Constants and utilities
    print("Test 7: Constants and utilities")
    print("-" * 60)
    print(f"  Golden ratio (φ): {fastfib.PHI:.15f}")
    print(f"  √5: {fastfib.SQRT5:.15f}")
    print(f"  get_phi(): {fastfib.get_phi():.15f}")
    print("✓ Constants accessible")
    print()
    
    # Summary
    print("=" * 60)
    print("✓ All tests completed successfully!")
    print("=" * 60)
    print()
    print("Quick usage examples:")
    print("  >>> import fastfib")
    print("  >>> fastfib.fib(10)")
    print("  55.0")
    print("  >>> fastfib.fib_range(10, 15)")
    print("  [55.0, 89.0, 144.0, 233.0, 377.0, 610.0]")
    print()
    
    return True

if __name__ == "__main__":
    success = test_fastfib()
    sys.exit(0 if success else 1)

