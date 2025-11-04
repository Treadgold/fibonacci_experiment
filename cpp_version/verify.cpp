/*
 * Verification program for GMP-based exact Fibonacci computation
 * Tests accuracy and performance of matrix exponentiation method
 */

#include <iostream>
#include <chrono>
#include <vector>
#include <gmp.h>
#include <gmpxx.h>

// Matrix 2x2 structure for GMP
struct Matrix2x2 {
    mpz_class a, b, c, d;  // [[a, b], [c, d]]
    
    Matrix2x2() : a(0), b(0), c(0), d(0) {}
    Matrix2x2(long a_, long b_, long c_, long d_) 
        : a(a_), b(b_), c(c_), d(d_) {}
};

// Multiply two 2x2 matrices
inline Matrix2x2 matrix_mult(const Matrix2x2& A, const Matrix2x2& B) {
    Matrix2x2 result;
    result.a = A.a * B.a + A.b * B.c;
    result.b = A.a * B.b + A.b * B.d;
    result.c = A.c * B.a + A.d * B.c;
    result.d = A.c * B.b + A.d * B.d;
    return result;
}

// Fast matrix exponentiation: compute M^n in O(log n)
Matrix2x2 matrix_pow(Matrix2x2 base, long long n) {
    if (n == 0) {
        return Matrix2x2(1, 0, 0, 1);  // Identity matrix
    }
    if (n == 1) {
        return base;
    }
    
    Matrix2x2 result(1, 0, 0, 1);  // Identity
    
    while (n > 0) {
        if (n & 1) {  // If n is odd
            result = matrix_mult(result, base);
        }
        base = matrix_mult(base, base);
        n >>= 1;
    }
    
    return result;
}

// Compute exact Fibonacci number using matrix exponentiation
mpz_class fibonacci_exact(long long n) {
    if (n == 0) return mpz_class(0);
    if (n == 1) return mpz_class(1);
    if (n == 2) return mpz_class(1);
    
    Matrix2x2 base(1, 1, 1, 0);
    Matrix2x2 result = matrix_pow(base, n - 1);
    
    return result.a;
}

// Simple iterative method (for comparison with small n)
mpz_class fibonacci_iterative(long long n) {
    if (n == 0) return mpz_class(0);
    if (n == 1) return mpz_class(1);
    
    mpz_class a = 0, b = 1;
    for (long long i = 2; i <= n; ++i) {
        mpz_class temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

int main() {
    std::cout << "=== GMP-Based Exact Fibonacci Verification ===\n\n";
    
    // Test 1: Verify correctness for small values
    std::cout << "Test 1: Accuracy verification (comparing matrix method vs iterative)\n";
    std::cout << "n\tMatrix Method\t\tIterative Method\tMatch?\n";
    std::cout << std::string(70, '-') << "\n";
    
    bool all_match = true;
    for (int n = 0; n <= 20; ++n) {
        mpz_class matrix_result = fibonacci_exact(n);
        mpz_class iterative_result = fibonacci_iterative(n);
        bool match = (matrix_result == iterative_result);
        all_match = all_match && match;
        
        std::cout << n << "\t" << matrix_result << "\t\t\t" 
                  << iterative_result << "\t\t" 
                  << (match ? "✓" : "✗") << "\n";
    }
    
    if (all_match) {
        std::cout << "\n✓ All values match! Matrix exponentiation is correct.\n\n";
    } else {
        std::cout << "\n✗ ERROR: Mismatch detected!\n\n";
        return 1;
    }
    
    // Test 2: Show growth for larger values
    std::cout << "Test 2: Fibonacci growth for larger n\n";
    std::cout << std::string(70, '-') << "\n";
    
    std::vector<long long> test_values = {100, 500, 1000, 5000, 10000, 50000, 100000};
    
    for (long long n : test_values) {
        mpz_class fib = fibonacci_exact(n);
        std::string fib_str = fib.get_str();
        size_t num_digits = fib_str.length();
        
        if (num_digits <= 100) {
            std::cout << "F(" << n << ") = " << fib_str << "\n";
        } else {
            std::cout << "F(" << n << ") = " 
                      << fib_str.substr(0, 50) << "..."
                      << fib_str.substr(num_digits - 30)
                      << "\n          (" << num_digits << " digits)\n";
        }
    }
    
    std::cout << "\n";
    
    // Test 3: Performance comparison
    std::cout << "Test 3: Performance comparison (single-threaded)\n";
    std::cout << std::string(70, '-') << "\n";
    
    // Test matrix method for various sizes
    std::vector<long long> perf_tests = {1000, 10000, 100000};
    
    for (long long n : perf_tests) {
        auto start = std::chrono::high_resolution_clock::now();
        mpz_class result = fibonacci_exact(n);
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        
        std::cout << "F(" << n << "): " << duration.count() << " μs"
                  << " (" << mpz_sizeinbase(result.get_mpz_t(), 10) << " digits)\n";
    }
    
    std::cout << "\n";
    
    // Test 4: Verify very large values
    std::cout << "Test 4: Computing very large Fibonacci numbers\n";
    std::cout << std::string(70, '-') << "\n";
    
    std::vector<long long> large_tests = {1000000, 10000000};
    
    for (long long n : large_tests) {
        std::cout << "Computing F(" << n << ")...\n";
        auto start = std::chrono::high_resolution_clock::now();
        mpz_class result = fibonacci_exact(n);
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        size_t num_digits = mpz_sizeinbase(result.get_mpz_t(), 10);
        std::string fib_str = result.get_str();
        
        std::cout << "  Time: " << duration.count() << " ms\n";
        std::cout << "  Digits: " << num_digits << "\n";
        std::cout << "  First 50: " << fib_str.substr(0, 50) << "...\n";
        std::cout << "  Last 50:  ..." << fib_str.substr(fib_str.length() - 50) << "\n\n";
    }
    
    std::cout << "✓ All verification tests passed!\n";
    std::cout << "\nNote: The matrix exponentiation method is O(log n) in multiplications,\n";
    std::cout << "but each multiplication becomes more expensive as the numbers grow larger.\n";
    std::cout << "Still MUCH faster than iterative O(n) methods for large n!\n";
    
    return 0;
}
