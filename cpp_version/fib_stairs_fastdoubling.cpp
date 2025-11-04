/*
 * Ultra-fast parallel Fibonacci computation using GMP (arbitrary precision)
 * Using FAST DOUBLING algorithm instead of matrix exponentiation
 * 
 * Fast Doubling formulas:
 *   F(2k) = F(k) * [2*F(k+1) - F(k)]
 *   F(2k+1) = F(k+1)^2 + F(k)^2
 * 
 * Time complexity: O(log n) per computation with fewer multiplications than matrix method
 */

#include <iostream>
#include <chrono>
#include <omp.h>
#include <vector>
#include <string>
#include <gmp.h>
#include <gmpxx.h>
#include <utility>

// Fast doubling implementation for Fibonacci
// Returns pair (F(n), F(n+1))
std::pair<mpz_class, mpz_class> fibonacci_fast_doubling_helper(long long n) {
    if (n == 0) {
        return {mpz_class(0), mpz_class(1)};
    }
    
    // Recursively compute F(n/2) and F(n/2 + 1)
    auto [fk, fk1] = fibonacci_fast_doubling_helper(n / 2);
    
    // F(2k) = F(k) * [2*F(k+1) - F(k)]
    mpz_class c = fk * (2 * fk1 - fk);
    
    // F(2k+1) = F(k+1)^2 + F(k)^2
    mpz_class d = fk1 * fk1 + fk * fk;
    
    if (n % 2 == 0) {
        return {c, d};
    } else {
        return {d, c + d};
    }
}

// Iterative fast doubling (more efficient, avoids recursion overhead)
std::pair<mpz_class, mpz_class> fibonacci_fast_doubling_iterative(long long n) {
    if (n == 0) {
        return {mpz_class(0), mpz_class(1)};
    }
    
    // Find the highest bit position
    int bit_length = 0;
    long long temp = n;
    while (temp > 0) {
        bit_length++;
        temp >>= 1;
    }
    
    // Start from the highest bit and work down
    mpz_class fk(0);
    mpz_class fk1(1);
    
    for (int i = bit_length - 1; i >= 0; --i) {
        // F(2k) = F(k) * [2*F(k+1) - F(k)]
        mpz_class f2k = fk * (2 * fk1 - fk);
        
        // F(2k+1) = F(k+1)^2 + F(k)^2
        mpz_class f2k1 = fk1 * fk1 + fk * fk;
        
        if ((n >> i) & 1) {
            // Bit is 1, so we want F(2k+1) and F(2k+2)
            fk = f2k1;
            fk1 = f2k + f2k1;
        } else {
            // Bit is 0, so we want F(2k) and F(2k+1)
            fk = f2k;
            fk1 = f2k1;
        }
    }
    
    return {fk, fk1};
}

// Compute exact Fibonacci number using fast doubling
inline mpz_class fibonacci_exact(long long n) {
    if (n < 0) {
        throw std::invalid_argument("n must be non-negative");
    }
    
    auto [fn, fn1] = fibonacci_fast_doubling_iterative(n);
    return fn;
}

// Compute Fibonacci numbers in range and show samples (with digit counts)
void compute_fibonacci_range_sum(long long start_n, long long end_n) {
    const int num_threads = omp_get_max_threads();
    std::cout << "Using " << num_threads << " CPU cores\n";
    std::cout << "Computing EXACT F(n) for n = " << start_n << " to " << end_n << "\n";
    std::cout << "Using FAST DOUBLING O(log n) per value\n\n";
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    long long total_computed = 0;
    
    #pragma omp parallel
    {
        long long local_count = 0;
        
        #pragma omp for schedule(dynamic, 100) nowait
        for (long long n = start_n; n <= end_n; ++n) {
            mpz_class fib = fibonacci_exact(n);
            local_count++;
            
            // Print first few and last few results
            #pragma omp critical
            {
                if (n <= start_n + 5 || n >= end_n - 5) {
                    std::string fib_str = fib.get_str();
                    size_t num_digits = fib_str.length();
                    
                    if (num_digits <= 100) {
                        std::cout << "F(" << n << ") = " << fib_str << "\n";
                    } else {
                        // Show first 50 and last 50 digits for very large numbers
                        std::cout << "F(" << n << ") = " 
                                  << fib_str.substr(0, 50) << "..."
                                  << fib_str.substr(num_digits - 50) 
                                  << " (" << num_digits << " digits)\n";
                    }
                }
            }
        }
        
        #pragma omp atomic
        total_computed += local_count;
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    
    std::cout << "\n=== Results ===\n";
    std::cout << "Total computed: " << total_computed << " Fibonacci numbers\n";
    std::cout << "Time elapsed: " << duration.count() << " ms\n";
    std::cout << "Speed: " << (total_computed / (duration.count() / 1000.0)) << " computations/second\n";
}

// Fast computation mode (no output, just benchmark)
void compute_fibonacci_range_fast(long long start_n, long long end_n) {
    const int num_threads = omp_get_max_threads();
    std::cout << "Using " << num_threads << " CPU cores\n";
    std::cout << "Computing EXACT F(n) for n = " << start_n << " to " << end_n << " (fast mode)\n";
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    long long total_computed = 0;
    
    #pragma omp parallel
    {
        long long local_count = 0;
        volatile long long dummy = 0; // Prevent compiler optimization
        
        #pragma omp for schedule(dynamic, 100) nowait
        for (long long n = start_n; n <= end_n; ++n) {
            mpz_class fib = fibonacci_exact(n);
            dummy += mpz_sizeinbase(fib.get_mpz_t(), 10); // Get digit count
            local_count++;
        }
        
        #pragma omp atomic
        total_computed += local_count;
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    
    std::cout << "\n=== Results ===\n";
    std::cout << "Total computed: " << total_computed << " Fibonacci numbers\n";
    std::cout << "Time elapsed: " << duration.count() << " ms\n";
    std::cout << "Speed: " << (total_computed / (duration.count() / 1000.0)) << " computations/second\n";
}

// Store results variant (stores as strings for exact values)
void compute_and_store_fibonacci(long long start_n, long long end_n, std::vector<std::string>& results) {
    const long long total = end_n - start_n + 1;
    results.resize(total);
    
    const int num_threads = omp_get_max_threads();
    std::cout << "Using " << num_threads << " CPU cores\n";
    std::cout << "Computing and storing EXACT F(n) for n = " << start_n << " to " << end_n << "\n";
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    #pragma omp parallel for schedule(dynamic, 100)
    for (long long i = 0; i < total; ++i) {
        long long n = start_n + i;
        mpz_class fib = fibonacci_exact(n);
        results[i] = fib.get_str();
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    
    std::cout << "\n=== Results ===\n";
    std::cout << "Total computed and stored: " << total << " Fibonacci numbers\n";
    std::cout << "Time elapsed: " << duration.count() << " ms\n";
    std::cout << "Speed: " << (total / (duration.count() / 1000.0)) << " computations/second\n";
}

int main(int argc, char* argv[]) {
    // Enable all available CPU cores
    omp_set_num_threads(omp_get_max_threads());
    
    std::cout << "=== Ultra-Fast Parallel EXACT Fibonacci Computation ===\n";
    std::cout << "Using FAST DOUBLING with GMP (arbitrary precision)\n";
    std::cout << "Method: Fast doubling in O(log n) time per value\n\n";
    
    // Parse command-line arguments or use defaults
    long long START_N = 3;
    long long END_N = 10000;  // Default to smaller range for testing
    
    if (argc >= 3) {
        START_N = std::stoll(argv[1]);
        END_N = std::stoll(argv[2]);
    } else if (argc == 2) {
        END_N = std::stoll(argv[1]);
    }
    
    std::cout << "Range: F(" << START_N << ") to F(" << END_N << ")\n\n";
    
    // Choose mode based on use case:
    
    // Mode 1: Compute and show some results (recommended for verification)
    compute_fibonacci_range_sum(START_N, END_N);
    
    // Mode 2: Just compute at maximum speed (no output, pure benchmark)
    // compute_fibonacci_range_fast(START_N, END_N);
    
    // Mode 3: Compute and store results as strings (if you need them later)
    // WARNING: Large ranges will use significant RAM
    // std::vector<std::string> results;
    // compute_and_store_fibonacci(START_N, END_N, results);
    
    return 0;
}

