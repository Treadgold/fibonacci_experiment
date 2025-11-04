# Makefile for ultra-fast Fibonacci computation
# Optimized for maximum performance

CXX = g++
CXXFLAGS = -std=c++17 -O3 -march=native -mtune=native -ffast-math -fopenmp
LDFLAGS = -fopenmp -lm

# Additional aggressive optimizations
OPT_FLAGS = -funroll-loops -fomit-frame-pointer -finline-functions -flto

TARGET = fib_stairs
VERIFY = verify
SOURCE = fib_stairs.cpp
VERIFY_SOURCE = verify.cpp

# Default target - build both programs
all: $(TARGET) $(VERIFY)

# Build main program with maximum optimizations
$(TARGET): $(SOURCE)
	$(CXX) $(CXXFLAGS) $(OPT_FLAGS) -o $(TARGET) $(SOURCE) $(LDFLAGS)
	@echo "✓ Main program built: ./$(TARGET)"

# Build verification program
$(VERIFY): $(VERIFY_SOURCE)
	$(CXX) -std=c++17 -O3 -march=native -ffast-math -o $(VERIFY) $(VERIFY_SOURCE) -lm
	@echo "✓ Verification program built: ./$(VERIFY)"

# Build for debugging
debug: CXXFLAGS = -std=c++17 -g -fopenmp -Wall -Wextra
debug: OPT_FLAGS =
debug: $(TARGET)

# Clean build artifacts
clean:
	rm -f $(TARGET) $(VERIFY)

# Run the main program
run: $(TARGET)
	./$(TARGET)

# Run verification tests
test: $(VERIFY)
	./$(VERIFY)

# Run comprehensive benchmark suite
benchmark: all
	@chmod +x benchmark.sh
	./benchmark.sh

# Show compiler version and flags
info:
	@echo "Compiler: $(CXX)"
	@$(CXX) --version | head -n 1
	@echo "Flags: $(CXXFLAGS) $(OPT_FLAGS)"
	@echo "OpenMP max threads: $$(getconf _NPROCESSORS_ONLN)"
	@echo "Current OMP_NUM_THREADS: $(OMP_NUM_THREADS)"

.PHONY: all debug clean run test benchmark info


