/*
 * Ultra-fast parallel Fibonacci computation using GMP (arbitrary precision)
 * Optimized for maximum speed across all CPU cores
 * Computes EXACT F(n) for n = 3 to 200,000,000 using matrix exponentiation
 * 
 * Matrix formula: [F(n+1), F(n)] = [[1,1],[1,0]]^n * [1, 0]
 * Time complexity: O(log n) per computation
 */

#include <iostream>
#include <chrono>
#include <omp.h>
#include <vector>
#include <string>
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
inline mpz_class fibonacci_exact(long long n) {
    if (n == 0) return mpz_class(0);
    if (n == 1) return mpz_class(1);
    if (n == 2) return mpz_class(1);
    
    // Base matrix: [[1, 1], [1, 0]]
    Matrix2x2 base(1, 1, 1, 0);
    
    // Compute base^(n-1)
    Matrix2x2 result = matrix_pow(base, n - 1);
    
    // F(n) = result.a * 1 + result.b * 0 = result.a
    return result.a;
}

// Compute Fibonacci numbers in range and show samples (with digit counts)
void compute_fibonacci_range_sum(long long start_n, long long end_n) {
    const int num_threads = omp_get_max_threads();
    std::cout << "Using " << num_threads << " CPU cores\n";
    std::cout << "Computing EXACT F(n) for n = " << start_n << " to " << end_n << "\n";
    std::cout << "Using matrix exponentiation O(log n) per value\n\n";
    
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
    std::cout << "Using Matrix Exponentiation with GMP (arbitrary precision)\n";
    std::cout << "Method: Fast matrix power in O(log n) time per value\n\n";
    
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
    // std::cout << "\nFirst few stored results:\n";
    // for (int i = 0; i < 10 && i < results.size(); ++i) {
    //     std::string val = results[i];
    //     if (val.length() <= 100) {
    //         std::cout << "F(" << (START_N + i) << ") = " << val << "\n";
    //     } else {
    //         std::cout << "F(" << (START_N + i) << ") = " << val.substr(0, 50) 
    //                   << "..." << val.substr(val.length()-20) 
    //                   << " (" << val.length() << " digits)\n";
    //     }
    // }
    
    return 0;
}


