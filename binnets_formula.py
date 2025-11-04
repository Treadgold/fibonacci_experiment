#!/usr/bin/env python3
"""
Binet's Formula Calculator - Solving the Staircase Problem & Fibonacci Numbers

THE STAIRCASE PROBLEM:
----------------------
Given n stairs, how many different ways can you climb them if you can take
either 1 step or 2 steps at a time?

Example with 4 stairs:
    1. (1+1+1+1) - four single steps
    2. (1+1+2)   - two singles, then a double
    3. (1+2+1)   - single, double, single
    4. (2+1+1)   - double, then two singles  
    5. (2+2)     - two double steps
    Answer: 5 ways!

WHY THIS IS FIBONACCI:
----------------------
To reach stair n, you must arrive from either:
  • stair (n-1) with a 1-step, OR
  • stair (n-2) with a 2-step

Therefore: ways(n) = ways(n-1) + ways(n-2)  ← Fibonacci recurrence!

Base cases:
  • 1 stair → 1 way:  (1)
  • 2 stairs → 2 ways: (1+1) or (2)
  • 3 stairs → 3 ways: (1+1+1), (1+2), (2+1)
  • 4 stairs → 5 ways: (shown above)

The staircase sequence: 1, 2, 3, 5, 8, 13, 21, ...
Standard Fibonacci:     0, 1, 1, 2, 3, 5,  8,  13, 21, ...

Connection: ways(n) = F(n+1) where F is standard Fibonacci!

BINET'S FORMULA - The Mathematical Shortcut:
--------------------------------------------
Instead of computing recursively, we use the closed-form expression:
    F(n) = (φⁿ - ψⁿ) / √5

Where:
    φ (phi) = (1 + √5) / 2 ≈ 1.618... (golden ratio)
    ψ (psi) = (1 - √5) / 2 ≈ -0.618... (conjugate of phi)

For the staircase problem: ways(n) = F(n+1) = (φⁿ⁺¹ - ψⁿ⁺¹) / √5

Time Complexity: O(1) - constant time, no loops or recursion!
Space Complexity: O(1) - constant space!
"""

import math
import argparse
import sys


def fibonacci_binet(n):
    """
    Calculate the nth Fibonacci number using Binet's formula.
    
    Mathematical Explanation:
    -------------------------
    Binet's formula is derived from the characteristic equation of the 
    Fibonacci recurrence relation. The formula leverages the fact that:
    
    1. φ = (1 + √5) / 2 is the golden ratio (~1.618), which satisfies φ² = φ + 1
    2. ψ = (1 - √5) / 2 is the conjugate root (~-0.618), satisfying ψ² = ψ + 1
    3. Both are roots of: x² = x + 1
    
    The general solution to F(n) = F(n-1) + F(n-2) is a linear combination:
        F(n) = A·φⁿ + B·ψⁿ
    
    Using initial conditions F(0)=0 and F(1)=1, we solve for A and B:
        A = 1/√5, B = -1/√5
    
    Therefore: F(n) = (φⁿ - ψⁿ) / √5
    
    Why does this work?
    -------------------
    - As n grows, ψⁿ approaches 0 (since |ψ| < 1)
    - So F(n) ≈ φⁿ / √5 for large n
    - The formula gives exact integer results when rounded!
    
    Args:
        n (int): The position in the Fibonacci sequence (n >= 0)
    
    Returns:
        int: The nth Fibonacci number
    
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Special case: F(0) = 0
    if n == 0:
        return 0
    
    # Calculate the mathematical constants
    sqrt5 = math.sqrt(5)
    
    # φ (phi): The golden ratio - fundamental constant in mathematics
    # Appears in nature (spirals, plant growth), art, and architecture
    phi = (1 + sqrt5) / 2
    
    # ψ (psi): The conjugate of phi
    # As n increases, this term vanishes (|psi| < 1 means psi^n → 0)
    psi = (1 - sqrt5) / 2
    
    # Apply Binet's formula
    # The division by √5 normalizes the result to give exact Fibonacci numbers
    result = (phi**n - psi**n) / sqrt5

    # Round to nearest integer (floating point precision may cause tiny errors)
    return round(result)


def staircase_ways(n):
    """
    Calculate how many ways to climb n stairs taking 1 or 2 steps at a time.
    
    The Staircase Problem Logic:
    ----------------------------
    Imagine you're at the bottom of a staircase with n stairs.
    At each step, you can choose to:
      - Take 1 stair (single step)
      - Take 2 stairs (double step)
    
    Question: How many different sequences of steps can get you to the top?
    
    Recursive Thinking:
    -------------------
    To get to stair n, you must have just come from either:
      1. Stair (n-1): then take a 1-step to reach n
      2. Stair (n-2): then take a 2-step to reach n
    
    Therefore, the number of ways to reach stair n is:
        ways(n) = ways(n-1) + ways(n-2)
    
    This is the Fibonacci recurrence!
    
    Base Cases (building the sequence):
    -----------------------------------
    • n=1: Only 1 way → (1)
    • n=2: Two ways → (1+1) or (2)
    • n=3: Three ways → (1+1+1), (1+2), (2+1)
    • n=4: Five ways → (1+1+1+1), (1+1+2), (1+2+1), (2+1+1), (2+2)
    
    Pattern: 1, 2, 3, 5, 8, 13, 21, 34...
    This is F(n+1) where F is the standard Fibonacci sequence!
    
    Using Binet's Formula:
    ---------------------
    Instead of recursion, we compute: ways(n) = F(n+1) = (φⁿ⁺¹ - ψⁿ⁺¹) / √5
    This gives us O(1) constant time computation!
    
    Args:
        n (int): Number of stairs (n >= 1)
    
    Returns:
        int: Number of different ways to climb the stairs
    
    Raises:
        ValueError: If n is less than 1
    """
    if n < 1:
        raise ValueError("Number of stairs must be at least 1")
    
    # The staircase problem is equivalent to F(n+1) in standard Fibonacci
    # We use the same Binet's formula but with (n+1)
    return fibonacci_binet(n + 1)


def display_sequence(start, end):
    """
    Display Fibonacci sequence from index start to end using Binet's formula.
    
    Args:
        start (int): Starting index (inclusive)
        end (int): Ending index (inclusive)
    """
    print(f"\nFibonacci Sequence (using Binet's Formula)")
    print("=" * 50)
    print(f"{'Index':<10} {'F(n)':<20} {'Ratio to F(n-1)'}")
    print("-" * 50)
    
    prev_value = None
    for i in range(start, end + 1):
        value = fibonacci_binet(i)
        ratio_str = f"{value / prev_value:.10f}" if prev_value and prev_value != 0 else "N/A"
        print(f"{i:<10} {value:<20} {ratio_str}")
        prev_value = value
    
    print("\nNote: The ratio converges to φ (phi) ≈ 1.618033988749...")


def display_staircase_sequence(start, end):
    """
    Display staircase problem solutions showing the connection to Fibonacci.
    
    Args:
        start (int): Starting number of stairs (inclusive)
        end (int): Ending number of stairs (inclusive)
    """
    print(f"\nStaircase Problem Solutions (using Binet's Formula)")
    print("=" * 70)
    print(f"{'Stairs':<10} {'Ways':<10} {'= F(n)':<15} {'Ratio to prev'}")
    print("-" * 70)
    
    prev_value = None
    for i in range(start, end + 1):
        ways = staircase_ways(i)
        fib_equiv = f"F({i+1})"
        ratio_str = f"{ways / prev_value:.10f}" if prev_value and prev_value != 0 else "N/A"
        print(f"{i:<10} {ways:<10} {fib_equiv:<15} {ratio_str}")
        prev_value = ways
    
    print("\nNote: ways(n) = F(n+1) in standard Fibonacci sequence")
    print("The ratio converges to φ (phi) ≈ 1.618033988749...")


def main():
    """Main CLI interface for Binet's formula calculator."""
    parser = argparse.ArgumentParser(
        description="Calculate Fibonacci numbers and solve staircase problems using Binet's formula (O(1) time)",
        epilog="""
Examples:
  Fibonacci mode:
    %(prog)s 10                        # Calculate F(10)
    %(prog)s --range 0 15              # Show F(0) through F(15)
    %(prog)s 10 -v                     # Detailed math for F(10)
  
  Staircase mode (how many ways to climb n stairs):
    %(prog)s --stairs 4                # Ways to climb 4 stairs
    %(prog)s --stairs 10 -v            # Detailed math for 10 stairs
    %(prog)s --stairs-range 1 10       # Show solutions for 1-10 stairs
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'n',
        type=int,
        nargs='?',
        help='Calculate the nth Fibonacci number (Fibonacci mode)'
    )
    
    parser.add_argument(
        '-r', '--range',
        type=int,
        nargs=2,
        metavar=('START', 'END'),
        help='Display Fibonacci sequence from START to END (inclusive)'
    )
    
    parser.add_argument(
        '-s', '--stairs',
        type=int,
        metavar='N',
        help='Solve staircase problem: ways to climb N stairs with 1 or 2 steps'
    )
    
    parser.add_argument(
        '--stairs-range',
        type=int,
        nargs=2,
        metavar=('START', 'END'),
        help='Show staircase solutions from START to END stairs (inclusive)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed mathematical breakdown'
    )
    
    args = parser.parse_args()
    
    # Handle staircase range mode
    if args.stairs_range:
        start, end = args.stairs_range
        if start < 1 or end < 1:
            print("Error: Number of stairs must be at least 1", file=sys.stderr)
            sys.exit(1)
        if start > end:
            print("Error: START must be less than or equal to END", file=sys.stderr)
            sys.exit(1)
        display_staircase_sequence(start, end)
        return
    
    # Handle single staircase problem
    if args.stairs is not None:
        if args.stairs < 1:
            print("Error: Number of stairs must be at least 1", file=sys.stderr)
            sys.exit(1)
        
        try:
            ways = staircase_ways(args.stairs)
            print(f"\n🪜 Staircase Problem: {args.stairs} stairs")
            print("=" * 50)
            print(f"Number of ways to climb: {ways}")
            print(f"Equivalent to: F({args.stairs + 1}) in Fibonacci sequence")
            
            if args.verbose:
                sqrt5 = math.sqrt(5)
                phi = (1 + sqrt5) / 2
                psi = (1 - sqrt5) / 2
                n_fib = args.stairs + 1
                
                print("\nHow the Staircase Problem Works:")
                print("-" * 50)
                print(f"To reach stair {args.stairs}, you can arrive from:")
                print(f"  • Stair {args.stairs - 1} (then take 1 step)")
                print(f"  • Stair {args.stairs - 2} (then take 2 steps)")
                print(f"\nThis gives: ways({args.stairs}) = ways({args.stairs - 1}) + ways({args.stairs - 2})")
                print("This is the Fibonacci recurrence relation!")
                
                print("\nDetailed Calculation using Binet's Formula:")
                print("=" * 50)
                print(f"We compute F({n_fib}) = (φ^{n_fib} - ψ^{n_fib}) / √5")
                print(f"\n√5           = {sqrt5}")
                print(f"φ (phi)      = {phi}")
                print(f"ψ (psi)      = {psi}")
                print(f"φ^{n_fib}         = {phi**n_fib}")
                print(f"ψ^{n_fib}         = {psi**n_fib}")
                print(f"(φ^{n_fib} - ψ^{n_fib}) = {phi**n_fib - psi**n_fib}")
                print(f"Result/√5    = {(phi**n_fib - psi**n_fib) / sqrt5}")
                print(f"Rounded      = {ways}")
                
                if args.stairs >= 2:
                    print("\nBuilding up from base cases:")
                    print("-" * 50)
                    for i in range(1, min(args.stairs + 1, 6)):
                        w = staircase_ways(i)
                        print(f"  {i} stairs → {w} way{'s' if w > 1 else ''}")
                    if args.stairs > 5:
                        print(f"  ...")
                        print(f"  {args.stairs} stairs → {ways} ways")
        
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return
    
    # Handle Fibonacci range mode
    if args.range:
        start, end = args.range
        if start < 0 or end < 0:
            print("Error: Range values must be non-negative", file=sys.stderr)
            sys.exit(1)
        if start > end:
            print("Error: START must be less than or equal to END", file=sys.stderr)
            sys.exit(1)
        display_sequence(start, end)
        return
    
    # Handle single Fibonacci value mode
    if args.n is None:
        parser.print_help()
        sys.exit(1)
    
    if args.n < 0:
        print("Error: n must be non-negative", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = fibonacci_binet(args.n)
        print(f"\nF({args.n}) = {result}")
        
        if args.verbose and args.n > 0:
            sqrt5 = math.sqrt(5)
            phi = (1 + sqrt5) / 2
            psi = (1 - sqrt5) / 2
            
            print("\nDetailed Calculation:")
            print("=" * 50)
            print(f"√5           = {sqrt5}")
            print(f"φ (phi)      = {phi}")
            print(f"ψ (psi)      = {psi}")
            print(f"φ^{args.n}         = {phi**args.n}")
            print(f"ψ^{args.n}         = {psi**args.n}")
            print(f"(φ^{args.n} - ψ^{args.n}) = {phi**args.n - psi**args.n}")
            print(f"Result/√5    = {(phi**args.n - psi**args.n) / sqrt5}")
            print(f"Rounded      = {result}")
            
            if args.n > 1:
                prev = fibonacci_binet(args.n - 1)
                print(f"\nRatio F({args.n})/F({args.n-1}) = {result/prev:.10f}")
                print(f"Golden ratio φ = {phi:.10f}")
                print(f"Difference from φ: {abs(result/prev - phi):.2e}")
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
