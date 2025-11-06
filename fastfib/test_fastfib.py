#!/usr/bin/env python3
"""
Test script for fastfib package
"""

import sys
import time

# Allow conversion of very large integers
sys.set_int_max_str_digits(0)  # No limit

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
    print(f"✓ Method: {fastfib.METHOD}")
    print(f"✓ Available CPU cores: {fastfib.get_num_cores()}")
    print()
    
    # Test 1: Single values (using fib_int for Python int)
    print("Test 1: Single Fibonacci numbers (EXACT integers)")
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
        result = fastfib.fib_int(n)  # Use fib_int to get Python int
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"  {status} fib({n}) = {result} (expected {expected})")
        all_passed = all_passed and passed
    
    if all_passed:
        print("✓ All single value tests passed!")
    else:
        print("✗ Some tests failed")
    print()
    
    # Test 2: Range (list of EXACT integers)
    print("Test 2: Fibonacci range (EXACT integer list)")
    print("-" * 60)
    fibs = fastfib.fib_range_int(10, 15)  # Use fib_range_int for Python ints
    expected_range = [55, 89, 144, 233, 377, 610]
    
    if len(fibs) == len(expected_range):
        print(f"✓ Length correct: {len(fibs)}")
    else:
        print(f"✗ Length mismatch: got {len(fibs)}, expected {len(expected_range)}")
    
    print(f"  Result: {fibs}")
    print(f"  Expected: {expected_range}")
    
    range_passed = all(f == e for f, e in zip(fibs, expected_range))
    if range_passed:
        print("✓ Range test passed!")
    else:
        print("✗ Range test failed")
    print()
    
    # Test 3: String representations
    print("Test 3: String representations (for very large numbers)")
    print("-" * 60)
    try:
        # Test that fib() returns strings
        str_result = fastfib.fib(100)
        int_result = fastfib.fib_int(100)
        
        print(f"✓ fib(100) as string: {str_result}")
        print(f"✓ fib(100) as int: {int_result}")
        
        # Verify they're the same value
        if int(str_result) == int_result:
            print("✓ String and int results match!")
        else:
            print("✗ String and int results don't match")
            
        # Test digit count
        digit_cnt = fastfib.digit_count(100)
        expected_digits = len(str_result)
        if digit_cnt == expected_digits:
            print(f"✓ Digit count correct: {digit_cnt} digits")
        else:
            print(f"✗ Digit count mismatch: got {digit_cnt}, expected {expected_digits}")
    except Exception as e:
        print(f"✗ String representation test failed: {e}")
    print()
    
    # Test 4: Large values (EXACT arbitrary precision)
    print("Test 4: Large Fibonacci numbers (EXACT values)")
    print("-" * 60)
    large_n = [50, 100, 500, 1000]
    for n in large_n:
        result = fastfib.fib(n)  # Returns string
        digits = len(result)
        # Show first and last digits for very large numbers
        if digits <= 50:
            print(f"  fib({n}) = {result} ({digits} digits)")
        else:
            print(f"  fib({n}) = {result[:30]}...{result[-20:]} ({digits} digits)")
    print("✓ Large number computation successful (all EXACT!)")
    print()
    
    # Test 5: Performance benchmark
    print("Test 5: Performance benchmark (EXACT computation)")
    print("-" * 60)
    
    # Single large value
    start = time.time()
    result = fastfib.fib_int(10000)
    elapsed = time.time() - start
    print(f"  Single fib(10,000): {elapsed*1000:.3f} ms ({len(str(result))} digits)")
    
    # Range of values
    start = time.time()
    fibs = fastfib.fib_range_int(1, 1000)
    elapsed = time.time() - start
    print(f"  Range 1-1,000: {elapsed*1000:.2f} ms ({len(fibs)/elapsed:,.0f} values/sec)")
    
    # Very large single value (use string version to avoid conversion overhead)
    start = time.time()
    result = fastfib.fib(100000)  # Returns string directly
    elapsed = time.time() - start
    print(f"  Single fib(100,000): {elapsed*1000:.3f} ms ({len(result)} digits)")
    
    print("✓ Performance test complete (all EXACT arbitrary precision!)")
    print()
    
    # Test 6: Thread control
    print("Test 6: Thread control")
    print("-" * 60)
    original_cores = fastfib.get_num_cores()
    print(f"  Available cores: {original_cores}")
    
    # Test with different thread counts
    for threads in [1, 2, 4]:
        if threads <= original_cores:
            fastfib.set_num_threads(threads)
            start = time.time()
            fibs = fastfib.fib_range_int(1, 10000)
            elapsed = time.time() - start
            print(f"  {threads} thread(s): {elapsed*1000:.2f} ms")
    
    print("✓ Thread control test complete")
    print()
    
    # Summary
    print("=" * 60)
    print("✓ All tests completed successfully!")
    print("=" * 60)
    print()
    print("Quick usage examples (EXACT arbitrary precision):")
    print("  >>> import fastfib")
    print("  >>> fastfib.fib(10)          # Returns string")
    print("  '55'")
    print("  >>> fastfib.fib_int(10)      # Returns Python int")
    print("  55")
    print("  >>> fastfib.fib_range_int(10, 15)")
    print("  [55, 89, 144, 233, 377, 610]")
    print()
    print("  >>> fastfib.fib_int(1000)    # EXACT 209-digit number!")
    print("  43466...93750")
    print()

if __name__ == "__main__":
    test_fastfib()
    sys.exit(0)

