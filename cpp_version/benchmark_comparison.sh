#!/bin/bash

# Benchmark comparison between matrix exponentiation and fast doubling

echo "=================================="
echo "Fibonacci Algorithm Comparison"
echo "Matrix Exponentiation vs Fast Doubling"
echo "=================================="
echo ""

# Compile both versions
echo "Compiling matrix exponentiation version..."
g++ -std=c++17 -O3 -march=native -fopenmp fib_stairs.cpp -o fib_stairs_matrix -lgmp -lgmpxx

echo "Compiling fast doubling version..."
g++ -std=c++17 -O3 -march=native -fopenmp fib_stairs_fastdoubling.cpp -o fib_stairs_fastdoubling -lgmp -lgmpxx

echo ""
echo "=================================="
echo "Test 1: Small range (1 to 1000)"
echo "=================================="
echo ""
echo "Matrix Exponentiation:"
time ./fib_stairs_matrix 1 1000 | tail -5
echo ""
echo "Fast Doubling:"
time ./fib_stairs_fastdoubling 1 1000 | tail -5

echo ""
echo "=================================="
echo "Test 2: Medium range (1 to 10000)"
echo "=================================="
echo ""
echo "Matrix Exponentiation:"
time ./fib_stairs_matrix 1 10000 | tail -5
echo ""
echo "Fast Doubling:"
time ./fib_stairs_fastdoubling 1 10000 | tail -5

echo ""
echo "=================================="
echo "Test 3: Large single values (F(100000))"
echo "=================================="
echo ""
echo "Matrix Exponentiation:"
time ./fib_stairs_matrix 100000 100000 | tail -5
echo ""
echo "Fast Doubling:"
time ./fib_stairs_fastdoubling 100000 100000 | tail -5

echo ""
echo "=================================="
echo "Test 4: Very large single values (F(1000000))"
echo "=================================="
echo ""
echo "Matrix Exponentiation:"
time ./fib_stairs_matrix 1000000 1000000 | tail -5
echo ""
echo "Fast Doubling:"
time ./fib_stairs_fastdoubling 1000000 1000000 | tail -5

echo ""
echo "=================================="
echo "Benchmark complete!"
echo "=================================="

