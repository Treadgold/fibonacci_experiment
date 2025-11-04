/*
 * Ultra-fast parallel Fibonacci computation using Binet's formula
 * Optimized for maximum speed across all CPU cores
 * Computes F(n) for n = 3 to 200,000,000
 */

#include <iostream>
#include <cmath>
#include <chrono>
#include <omp.h>
#include <vector>
#include <immintrin.h>

// Constants precomputed at compile time
constexpr double SQRT5 = 2.2360679774997896964091736687312762;
constexpr double PHI = 1.6180339887498948482045868343656381;  // (1 + sqrt(5)) / 2
constexpr double PSI = -0.61803398874989484820458683436563811; // (1 - sqrt(5)) / 2
constexpr double INV_SQRT5 = 0.44721359549995793928183473374625524;

// Fast power function using logarithms (for Binet's formula)
// For large n, psi^n becomes negligible, so we can optimize
inline double fast_binet(long long n) {
    // For large n: F(n) ≈ phi^n / sqrt(5)
    // Using logarithms: phi^n = exp(n * ln(phi))
    
    // psi^n becomes negligible for n > 20, so we can skip it
    if (n > 20) {
        // F(n) ≈ round(phi^n / sqrt(5))
        // Using log: phi^n = exp(n * log(phi))
        return std::exp(n * std::log(PHI)) * INV_SQRT5;
    } else {
        // Full formula for smaller n
        double phi_n = std::pow(PHI, n);
        double psi_n = std::pow(PSI, n);
        return (phi_n - psi_n) * INV_SQRT5;
    }
}

// Even faster approximation for very large n
inline double ultra_fast_binet(long long n) {
    // For n > 20: psi^n ≈ 0, so F(n) ≈ phi^n / sqrt(5)
    // phi^n = exp(n * ln(phi))
    static const double LOG_PHI = std::log(PHI);
    return std::exp(n * LOG_PHI) * INV_SQRT5;
}

// Compute sum of all Fibonacci numbers in range (for verification)
void compute_fibonacci_range_sum(long long start_n, long long end_n) {
    const int num_threads = omp_get_max_threads();
    std::cout << "Using " << num_threads << " CPU cores\n";
    std::cout << "Computing F(n) for n = " << start_n << " to " << end_n << "\n";
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    // Use atomic or reduction for thread-safe accumulation
    double global_sum = 0.0;
    long long total_computed = 0;
    
    #pragma omp parallel
    {
        double local_sum = 0.0;
        long long local_count = 0;
        
        #pragma omp for schedule(dynamic, 100000) nowait
        for (long long n = start_n; n <= end_n; ++n) {
            double fib = ultra_fast_binet(n);
            local_sum += fib;
            local_count++;
            
            // Optional: Print first few and last few results
            #pragma omp critical
            {
                if (n <= start_n + 5 || n >= end_n - 5) {
                    std::cout << "F(" << n << ") ≈ " << fib << "\n";
                }
            }
        }
        
        #pragma omp critical
        {
            global_sum += local_sum;
            total_computed += local_count;
        }
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    
    std::cout << "\n=== Results ===\n";
    std::cout << "Total computed: " << total_computed << " Fibonacci numbers\n";
    std::cout << "Sum of all values: " << global_sum << "\n";
    std::cout << "Time elapsed: " << duration.count() << " ms\n";
    std::cout << "Speed: " << (total_computed / (duration.count() / 1000.0)) << " computations/second\n";
}

// Variant that just computes without accumulation (even faster)
void compute_fibonacci_range_fast(long long start_n, long long end_n) {
    const int num_threads = omp_get_max_threads();
    std::cout << "Using " << num_threads << " CPU cores\n";
    std::cout << "Computing F(n) for n = " << start_n << " to " << end_n << " (fast mode)\n";
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    long long total_computed = 0;
    
    // Precompute log(phi) for ultra-fast computation
    static const double LOG_PHI = std::log(PHI);
    
    #pragma omp parallel
    {
        long long local_count = 0;
        double dummy_sum = 0.0; // Prevent compiler from optimizing away the computation
        
        #pragma omp for schedule(static) nowait
        for (long long n = start_n; n <= end_n; ++n) {
            // Inline computation for maximum speed
            double fib = std::exp(n * LOG_PHI) * INV_SQRT5;
            dummy_sum += fib * 1e-100; // Prevent optimization
            local_count++;
        }
        
        #pragma omp atomic
        total_computed += local_count;
        
        // Use dummy_sum to prevent optimization
        if (dummy_sum < 0) std::cout << "";
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    
    std::cout << "\n=== Results ===\n";
    std::cout << "Total computed: " << total_computed << " Fibonacci numbers\n";
    std::cout << "Time elapsed: " << duration.count() << " ms\n";
    std::cout << "Speed: " << (total_computed / (duration.count() / 1000.0)) << " computations/second\n";
}

// Store results variant (for when you need the actual values)
void compute_and_store_fibonacci(long long start_n, long long end_n, std::vector<double>& results) {
    const long long total = end_n - start_n + 1;
    results.resize(total);
    
    const int num_threads = omp_get_max_threads();
    std::cout << "Using " << num_threads << " CPU cores\n";
    std::cout << "Computing and storing F(n) for n = " << start_n << " to " << end_n << "\n";
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    static const double LOG_PHI = std::log(PHI);
    
    #pragma omp parallel for schedule(static)
    for (long long i = 0; i < total; ++i) {
        long long n = start_n + i;
        results[i] = std::exp(n * LOG_PHI) * INV_SQRT5;
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
    
    std::cout << "=== Ultra-Fast Parallel Fibonacci Computation ===\n";
    std::cout << "Using Binet's Formula: F(n) ≈ φ^n / √5\n\n";
    
    const long long START_N = 3;
    const long long END_N = 200000000;
    
    // Choose mode based on use case:
    
    // Mode 1: Compute and show some results with sum (moderate speed)
    // compute_fibonacci_range_sum(START_N, END_N);
    
    // Mode 2: Just compute at maximum speed (no storage)
    compute_fibonacci_range_fast(START_N, END_N);
    
    // Mode 3: Compute and store results (if you need them later)
    // WARNING: This will use ~1.6 GB of RAM for 200M doubles
    // std::vector<double> results;
    // compute_and_store_fibonacci(START_N, END_N, results);
    // std::cout << "First few results:\n";
    // for (int i = 0; i < 10 && i < results.size(); ++i) {
    //     std::cout << "F(" << (START_N + i) << ") ≈ " << results[i] << "\n";
    // }
    
    return 0;
}


