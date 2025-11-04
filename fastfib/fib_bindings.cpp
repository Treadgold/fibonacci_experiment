/*
 * Python bindings for ultra-fast Fibonacci computation
 * Using pybind11 to expose C++ functions to Python
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <cmath>
#include <vector>
#include <omp.h>

namespace py = pybind11;

// Constants
constexpr double SQRT5 = 2.2360679774997896964091736687312762;
constexpr double PHI = 1.6180339887498948482045868343656381;
constexpr double PSI = -0.61803398874989484820458683436563811;
constexpr double INV_SQRT5 = 0.44721359549995793928183473374625524;

// Fast Fibonacci using Binet's formula
inline double fib_binet(long long n) {
    if (n < 0) {
        throw std::invalid_argument("n must be non-negative");
    }
    if (n == 0) return 0.0;
    if (n == 1) return 1.0;
    
    // For large n, psi^n is negligible
    if (n > 20) {
        static const double LOG_PHI = std::log(PHI);
        return std::exp(n * LOG_PHI) * INV_SQRT5;
    } else {
        // Full formula for smaller n (more accurate)
        double phi_n = std::pow(PHI, n);
        double psi_n = std::pow(PSI, n);
        return std::round((phi_n - psi_n) * INV_SQRT5);
    }
}

// Compute single Fibonacci number
double fibonacci(long long n) {
    return fib_binet(n);
}

// Compute multiple Fibonacci numbers (returns Python list)
std::vector<double> fibonacci_range(long long start, long long end, int num_threads = -1) {
    if (start < 0 || end < 0) {
        throw std::invalid_argument("start and end must be non-negative");
    }
    if (start > end) {
        throw std::invalid_argument("start must be <= end");
    }
    
    // Set number of threads
    if (num_threads > 0) {
        omp_set_num_threads(num_threads);
    } else {
        omp_set_num_threads(omp_get_max_threads());
    }
    
    const long long total = end - start + 1;
    std::vector<double> results(total);
    
    static const double LOG_PHI = std::log(PHI);
    
    #pragma omp parallel for schedule(static)
    for (long long i = 0; i < total; ++i) {
        long long n = start + i;
        if (n == 0) {
            results[i] = 0.0;
        } else if (n == 1) {
            results[i] = 1.0;
        } else if (n > 20) {
            results[i] = std::exp(n * LOG_PHI) * INV_SQRT5;
        } else {
            double phi_n = std::pow(PHI, n);
            double psi_n = std::pow(PSI, n);
            results[i] = std::round((phi_n - psi_n) * INV_SQRT5);
        }
    }
    
    return results;
}

// Compute multiple Fibonacci numbers (returns NumPy array)
py::array_t<double> fibonacci_array(long long start, long long end, int num_threads = -1) {
    if (start < 0 || end < 0) {
        throw std::invalid_argument("start and end must be non-negative");
    }
    if (start > end) {
        throw std::invalid_argument("start must be <= end");
    }
    
    // Set number of threads
    if (num_threads > 0) {
        omp_set_num_threads(num_threads);
    } else {
        omp_set_num_threads(omp_get_max_threads());
    }
    
    const long long total = end - start + 1;
    
    // Create NumPy array
    py::array_t<double> result(total);
    py::buffer_info buf = result.request();
    double* ptr = static_cast<double*>(buf.ptr);
    
    static const double LOG_PHI = std::log(PHI);
    
    #pragma omp parallel for schedule(static)
    for (long long i = 0; i < total; ++i) {
        long long n = start + i;
        if (n == 0) {
            ptr[i] = 0.0;
        } else if (n == 1) {
            ptr[i] = 1.0;
        } else if (n > 20) {
            ptr[i] = std::exp(n * LOG_PHI) * INV_SQRT5;
        } else {
            double phi_n = std::pow(PHI, n);
            double psi_n = std::pow(PSI, n);
            ptr[i] = std::round((phi_n - psi_n) * INV_SQRT5);
        }
    }
    
    return result;
}

// Get number of available CPU cores
int get_num_cores() {
    return omp_get_max_threads();
}

// Set number of threads for computation
void set_num_threads(int n) {
    if (n <= 0) {
        throw std::invalid_argument("Number of threads must be positive");
    }
    omp_set_num_threads(n);
}

// Get golden ratio
double get_phi() {
    return PHI;
}

// Module definition
PYBIND11_MODULE(_fastfib, m) {
    m.doc() = "Ultra-fast Fibonacci computation using Binet's formula and parallel processing";
    
    // Single value function
    m.def("fibonacci", &fibonacci, 
          py::arg("n"),
          "Compute the nth Fibonacci number using Binet's formula.\n\n"
          "Args:\n"
          "    n: Non-negative integer index\n\n"
          "Returns:\n"
          "    The nth Fibonacci number (as float for large n)\n\n"
          "Example:\n"
          "    >>> fibonacci(10)\n"
          "    55.0\n"
          "    >>> fibonacci(100)\n"
          "    3.542248481792619e+20");
    
    // Range function returning list
    m.def("fibonacci_range", &fibonacci_range,
          py::arg("start"),
          py::arg("end"),
          py::arg("num_threads") = -1,
          "Compute Fibonacci numbers from start to end (inclusive).\n\n"
          "Args:\n"
          "    start: Starting index (non-negative)\n"
          "    end: Ending index (non-negative, >= start)\n"
          "    num_threads: Number of CPU cores to use (-1 for all)\n\n"
          "Returns:\n"
          "    List of Fibonacci numbers\n\n"
          "Example:\n"
          "    >>> fibonacci_range(10, 15)\n"
          "    [55.0, 89.0, 144.0, 233.0, 377.0, 610.0]");
    
    // Range function returning NumPy array
    m.def("fibonacci_array", &fibonacci_array,
          py::arg("start"),
          py::arg("end"),
          py::arg("num_threads") = -1,
          "Compute Fibonacci numbers from start to end (inclusive) as NumPy array.\n\n"
          "Args:\n"
          "    start: Starting index (non-negative)\n"
          "    end: Ending index (non-negative, >= start)\n"
          "    num_threads: Number of CPU cores to use (-1 for all)\n\n"
          "Returns:\n"
          "    NumPy array of Fibonacci numbers\n\n"
          "Example:\n"
          "    >>> import numpy as np\n"
          "    >>> arr = fibonacci_array(10, 15)\n"
          "    >>> arr\n"
          "    array([55., 89., 144., 233., 377., 610.])");
    
    // Utility functions
    m.def("get_num_cores", &get_num_cores,
          "Get the number of available CPU cores.");
    
    m.def("set_num_threads", &set_num_threads,
          py::arg("n"),
          "Set the number of threads to use for parallel computation.");
    
    m.def("get_phi", &get_phi,
          "Get the golden ratio (φ = (1 + √5) / 2).");
    
    // Constants
    m.attr("PHI") = PHI;
    m.attr("SQRT5") = SQRT5;
    m.attr("__version__") = "1.0.0";
}

