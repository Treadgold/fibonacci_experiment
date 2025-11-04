#!/usr/bin/env python3
"""
Generate a LibreOffice Calc spreadsheet demonstrating Binet's formula
for both Fibonacci numbers and the staircase problem.
"""

import csv

def generate_calc_data(max_n=20):
    """Generate data for the spreadsheet."""
    data = []
    
    # Header row
    data.append([
        'n',
        'Stairs Ways',
        'Formula (ways)',
        'Fibonacci F(n)',
        'Formula (fib)',
        'phi^n',
        'psi^n'
    ])
    
    # Instructions row
    data.append([
        'Enter numbers 1,2,3...',
        '=ROUND((POWER((1+SQRT(5))/2,A2+1)-POWER((1-SQRT(5))/2,A2+1))/SQRT(5),0)',
        'Copy formula shown →',
        '=ROUND((POWER((1+SQRT(5))/2,A2)-POWER((1-SQRT(5))/2,A2))/SQRT(5),0)',
        'Copy formula shown →',
        '=POWER((1+SQRT(5))/2,A2)',
        '=POWER((1-SQRT(5))/2,A2)'
    ])
    
    # Empty row for separation
    data.append(['', '', '', '', '', '', ''])
    
    # Column headers for actual data
    data.append([
        'n',
        'Ways(n)',
        '= F(n+1)',
        'F(n)',
        'Ratio F(n)/F(n-1)',
        'φ^n',
        'ψ^n'
    ])
    
    # Generate data
    import math
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    
    prev_fib = 0
    for n in range(0, max_n + 1):
        if n == 0:
            fib = 0
            ways = ''  # No staircase for 0 stairs
            ratio = ''
        elif n == 1:
            fib = 1
            ways = 1
            ratio = ''
        else:
            fib = round((phi**n - psi**n) / sqrt5)
            ways = round((phi**(n+1) - psi**(n+1)) / sqrt5)
            ratio = f"{fib / prev_fib:.6f}" if prev_fib != 0 else ''
        
        data.append([
            n,
            ways if ways != '' else '',
            f"F({n+1})" if n > 0 else '',
            fib,
            ratio,
            f"{phi**n:.6f}",
            f"{psi**n:.6f}"
        ])
        prev_fib = fib if fib != 0 else prev_fib
    
    return data

def main():
    print("Generating LibreOffice Calc spreadsheet data...")
    data = generate_calc_data(30)
    
    # Write to CSV
    csv_file = 'fibonacci_staircase.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print(f"✓ Created {csv_file}")
    print("\nTo use in LibreOffice Calc:")
    print("1. Open the CSV file in LibreOffice Calc")
    print("2. Row 2 shows the formulas you can use")
    print("3. The rest of the sheet has pre-calculated values")
    print("\nFormulas for LibreOffice Calc:")
    print("-" * 60)
    print("Staircase Ways (column B):")
    print("  =ROUND((POWER((1+SQRT(5))/2,A5+1)-POWER((1-SQRT(5))/2,A5+1))/SQRT(5),0)")
    print("\nFibonacci F(n) (column D):")
    print("  =ROUND((POWER((1+SQRT(5))/2,A5)-POWER((1-SQRT(5))/2,A5))/SQRT(5),0)")
    print("\nNote: Adjust cell references (A5) to match your starting row")

if __name__ == "__main__":
    main()


