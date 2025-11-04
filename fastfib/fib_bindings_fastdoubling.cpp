/*
 * Python bindings for ultra-fast EXACT Fibonacci computation
 * Using pybind11 to expose C++ functions with GMP arbitrary precision
 * FAST DOUBLING algorithm for better performance
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>
#include <utility>
#include <omp.h>
#include <gmp.h>
#include <gmpxx.h>

namespace py = pybind11;

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
inline mpz_class fibonacci_exact_gmp(long long n) {
    if (n < 0) {
        throw std::invalid_argument("n must be non-negative");
    }
    
    auto [fn, fn1] = fibonacci_fast_doubling_iterative(n);
    return fn;
}

// Compute single Fibonacci number (returns as string for arbitrary precision)
std::string fibonacci(long long n) {
    if (n < 0) {
        throw std::invalid_argument("n must be non-negative");
    }
    
    mpz_class result = fibonacci_exact_gmp(n);
    return result.get_str();
}

// Compute single Fibonacci number as Python int (arbitrary precision)
py::object fibonacci_int(long long n) {
    if (n < 0) {
        throw std::invalid_argument("n must be non-negative");
    }
    
    mpz_class result = fibonacci_exact_gmp(n);
    std::string result_str = result.get_str();
    
    // Convert string to Python int using Python C API
    PyObject* py_int = PyLong_FromString(result_str.c_str(), nullptr, 10);
    return py::reinterpret_steal<py::object>(py_int);
}

// Compute multiple Fibonacci numbers (returns list of strings)
std::vector<std::string> fibonacci_range(long long start, long long end, int num_threads = -1) {
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
    std::vector<std::string> results(total);
    
    #pragma omp parallel for schedule(dynamic, 10)
    for (long long i = 0; i < total; ++i) {
        long long n = start + i;
        mpz_class fib = fibonacci_exact_gmp(n);
        results[i] = fib.get_str();
    }
    
    return results;
}

// Compute multiple Fibonacci numbers (returns list of Python ints)
py::list fibonacci_range_int(long long start, long long end, int num_threads = -1) {
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
    std::vector<std::string> results(total);
    
    #pragma omp parallel for schedule(dynamic, 10)
    for (long long i = 0; i < total; ++i) {
        long long n = start + i;
        mpz_class fib = fibonacci_exact_gmp(n);
        results[i] = fib.get_str();
    }
    
    // Convert to Python list of ints
    py::list py_results;
    for (const auto& str : results) {
        // Convert string to Python int using Python C API
        PyObject* py_int = PyLong_FromString(str.c_str(), nullptr, 10);
        py_results.append(py::reinterpret_steal<py::object>(py_int));
    }
    
    return py_results;
}

// Compute multiple Fibonacci numbers (returns NumPy array of Python objects for arbitrary precision)
py::array fibonacci_array(long long start, long long end, int num_threads = -1) {
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
    std::vector<std::string> results(total);
    
    #pragma omp parallel for schedule(dynamic, 10)
    for (long long i = 0; i < total; ++i) {
        long long n = start + i;
        mpz_class fib = fibonacci_exact_gmp(n);
        results[i] = fib.get_str();
    }
    
    // Create NumPy array of Python object type for arbitrary precision
    py::array_t<py::object> result(total);
    auto buf = result.request();
    py::object* ptr = static_cast<py::object*>(buf.ptr);
    
    for (long long i = 0; i < total; ++i) {
        // Convert string to Python int using Python C API
        PyObject* py_int = PyLong_FromString(results[i].c_str(), nullptr, 10);
        ptr[i] = py::reinterpret_steal<py::object>(py_int);
    }
    
    return result;
}

// Get digit count for F(n) without computing the full value
long long fibonacci_digit_count(long long n) {
    if (n < 0) {
        throw std::invalid_argument("n must be non-negative");
    }
    if (n == 0) return 1;
    
    mpz_class result = fibonacci_exact_gmp(n);
    return mpz_sizeinbase(result.get_mpz_t(), 10);
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

// Module definition
PYBIND11_MODULE(_fastfib_fd, m) {
    m.doc() = "Ultra-fast EXACT Fibonacci computation using GMP arbitrary precision and FAST DOUBLING algorithm";
    
    // Single value function (returns string)
    m.def("fibonacci", 
          [](long long n) -> std::string { return fibonacci(n); },
          py::arg("n"),
          "Compute the nth Fibonacci number using fast doubling (GMP).\n\n"
          "Args:\n"
          "    n: Non-negative integer index\n\n"
          "Returns:\n"
          "    String representation of the exact nth Fibonacci number\n\n"
          "Example:\n"
          "    >>> fibonacci(10)\n"
          "    '55'\n"
          "    >>> fibonacci(100)\n"
          "    '354224848179261915075'");
    
    // Single value function (returns Python int with arbitrary precision)
    m.def("fibonacci_int",
          [](long long n) -> py::object { return fibonacci_int(n); },
          py::arg("n"),
          "Compute the nth Fibonacci number as Python int with arbitrary precision.\n\n"
          "Args:\n"
          "    n: Non-negative integer index\n\n"
          "Returns:\n"
          "    Python int with exact value\n\n"
          "Example:\n"
          "    >>> fibonacci_int(100)\n"
          "    354224848179261915075");
    
    // Range function returning list of strings
    m.def("fibonacci_range",
          [](long long start, long long end, int num_threads) -> std::vector<std::string> {
              return fibonacci_range(start, end, num_threads);
          },
          py::arg("start"),
          py::arg("end"),
          py::arg("num_threads") = -1,
          "Compute exact Fibonacci numbers from start to end (inclusive).\n\n"
          "Args:\n"
          "    start: Starting index (non-negative)\n"
          "    end: Ending index (non-negative, >= start)\n"
          "    num_threads: Number of CPU cores to use (-1 for all)\n\n"
          "Returns:\n"
          "    List of strings with exact Fibonacci values\n\n"
          "Example:\n"
          "    >>> fibonacci_range(10, 15)\n"
          "    ['55', '89', '144', '233', '377', '610']");
    
    // Range function returning list of Python ints
    m.def("fibonacci_range_int",
          [](long long start, long long end, int num_threads) -> py::list {
              return fibonacci_range_int(start, end, num_threads);
          },
          py::arg("start"),
          py::arg("end"),
          py::arg("num_threads") = -1,
          "Compute exact Fibonacci numbers from start to end as Python ints.\n\n"
          "Args:\n"
          "    start: Starting index (non-negative)\n"
          "    end: Ending index (non-negative, >= start)\n"
          "    num_threads: Number of CPU cores to use (-1 for all)\n\n"
          "Returns:\n"
          "    List of Python ints with exact values\n\n"
          "Example:\n"
          "    >>> fibonacci_range_int(10, 15)\n"
          "    [55, 89, 144, 233, 377, 610]");
    
    // Range function returning NumPy array
    m.def("fibonacci_array",
          [](long long start, long long end, int num_threads) -> py::array {
              return fibonacci_array(start, end, num_threads);
          },
          py::arg("start"),
          py::arg("end"),
          py::arg("num_threads") = -1,
          "Compute exact Fibonacci numbers from start to end as NumPy array.\n\n"
          "Args:\n"
          "    start: Starting index (non-negative)\n"
          "    end: Ending index (non-negative, >= start)\n"
          "    num_threads: Number of CPU cores to use (-1 for all)\n\n"
          "Returns:\n"
          "    NumPy array of Python object type with exact values\n\n"
          "Example:\n"
          "    >>> import numpy as np\n"
          "    >>> arr = fibonacci_array(10, 15)\n"
          "    >>> arr\n"
          "    array([55, 89, 144, 233, 377, 610], dtype=object)");
    
    // Digit count function
    m.def("fibonacci_digit_count",
          [](long long n) -> long long { return fibonacci_digit_count(n); },
          py::arg("n"),
          "Get the number of digits in F(n).\n\n"
          "Args:\n"
          "    n: Non-negative integer index\n\n"
          "Returns:\n"
          "    Number of digits in the nth Fibonacci number\n\n"
          "Example:\n"
          "    >>> fibonacci_digit_count(1000)\n"
          "    209");
    
    // Utility functions
    m.def("get_num_cores",
          []() -> int { return get_num_cores(); },
          "Get the number of available CPU cores.");
    
    m.def("set_num_threads",
          [](int n) { set_num_threads(n); },
          py::arg("n"),
          "Set the number of threads to use for parallel computation.");
    
    // Constants
    m.attr("__version__") = "2.1.0";
    m.attr("METHOD") = "Fast Doubling with GMP";
}

