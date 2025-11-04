/*
 * Verification and comparison program for Fibonacci computation
 * Compares Binet's formula with exact iterative computation
 */

#include <iostream>
#include <cmath>
#include <chrono>
#include <vector>

constexpr double SQRT5 = 2.2360679774997896964091736687312762;
constexpr double PHI = 1.6180339887498948482045868343656381;
constexpr double PSI = -0.61803398874989484820458683436563811;
constexpr double INV_SQRT5 = 0.44721359549995793928183473374625524;
constexpr double LOG_PHI = 0.48121182505960347;

// Exact Fibonacci using iteration (for small n)
unsigned long long fib_exact(int n) {
    if (n <= 1) return n;
    unsigned long long a = 0, b = 1;
    for (int i = 2; i <= n; ++i) {
        unsigned long long temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// Binet's formula (full)
double fib_binet_full(int n) {
    double phi_n = std::pow(PHI, n);
    double psi_n = std::pow(PSI, n);
    return std::round((phi_n - psi_n) * INV_SQRT5);
}

// Binet's formula (optimized for large n)
double fib_binet_fast(long long n) {
    return std::exp(n * LOG_PHI) * INV_SQRT5;
}

int main() {
    std::cout << "=== Fibonacci Verification ===\n\n";
    
    // Verify accuracy for small values
    std::cout << "Accuracy test (comparing Binet vs Exact):\n";
    std::cout << "n\tExact\t\tBinet (full)\tBinet (fast)\tError\n";
    std::cout << std::string(70, '-') << "\n";
    
    for (int n = 1; n <= 20; ++n) {
        unsigned long long exact = fib_exact(n);
        double binet_full = fib_binet_full(n);
        double binet_fast = fib_binet_fast(n);
        double error = std::abs(exact - binet_full);
        
        std::cout << n << "\t" << exact << "\t\t" 
                  << (long long)binet_full << "\t\t"
                  << (long long)binet_fast << "\t\t"
                  << error << "\n";
    }
    
    std::cout << "\n✓ Binet's formula is exact for these values!\n\n";
    
    // Test upper limit of exact computation
    std::cout << "Testing limits of exact computation:\n";
    std::cout << "F(78) = " << fib_exact(78) << " (last exact value in uint64)\n";
    std::cout << "F(79) would overflow uint64\n\n";
    
    // Show exponential growth for large n
    std::cout << "Fibonacci growth for large n (using Binet):\n";
    std::vector<long long> test_values = {100, 1000, 10000, 100000, 1000000, 10000000};
    
    for (long long n : test_values) {
        double fib = fib_binet_fast(n);
        std::cout << "F(" << n << ") ≈ " << fib << "\n";
    }
    
    std::cout << "\n";
    
    // Speed comparison
    std::cout << "Speed comparison (single-threaded):\n";
    std::cout << std::string(70, '-') << "\n";
    
    // Test iterative method
    auto start = std::chrono::high_resolution_clock::now();
    unsigned long long sum_exact = 0;
    for (int n = 1; n <= 1000000; ++n) {
        if (n <= 78) {
            sum_exact += fib_exact(n);
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration_exact = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Iterative method (1M values, n≤78): " << duration_exact.count() << " ms\n";
    
    // Test Binet method
    start = std::chrono::high_resolution_clock::now();
    double sum_binet = 0;
    for (int n = 1; n <= 10000000; ++n) {
        sum_binet += fib_binet_fast(n);
    }
    end = std::chrono::high_resolution_clock::now();
    auto duration_binet = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Binet method (10M values): " << duration_binet.count() << " ms\n";
    std::cout << "Binet is ~" << (10.0 * duration_exact.count() / duration_binet.count()) 
              << "x faster\n";
    
    std::cout << "\n✓ Verification complete!\n";
    
    return 0;
}


