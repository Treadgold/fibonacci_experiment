#!/bin/bash
# Comprehensive benchmark script for Fibonacci computation

echo "=== Fibonacci Computation Benchmark Suite ==="
echo ""

# Check if programs are built
if [ ! -f "fib_stairs" ]; then
    echo "Building main program..."
    make
fi

if [ ! -f "verify" ]; then
    echo "Building verification program..."
    g++ -std=c++17 -O3 -march=native -ffast-math -o verify verify.cpp -lm
fi

echo ""
echo "=== System Information ==="
echo "CPU: $(lscpu | grep "Model name" | cut -d: -f2 | xargs)"
echo "CPU Cores: $(nproc)"
echo "Available Memory: $(free -h | awk '/^Mem:/ {print $7}')"
echo ""

# Run verification first
echo "=== Running Verification ==="
./verify
echo ""

# Test with different thread counts
echo "=== Thread Scaling Test ==="
echo "Testing performance with different thread counts..."
echo ""

for threads in 1 2 4 8 $(nproc); do
    if [ $threads -le $(nproc) ]; then
        echo "Testing with $threads thread(s)..."
        export OMP_NUM_THREADS=$threads
        ./fib_stairs 2>&1 | grep -E "(Using|Time elapsed|Speed)"
        echo ""
    fi
done

# Reset to use all threads
unset OMP_NUM_THREADS

echo "=== Benchmark Complete ==="

