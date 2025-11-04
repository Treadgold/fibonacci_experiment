from setuptools import setup, Extension
import pybind11
import sys

# Get compiler flags
extra_compile_args = [
    '-std=c++17',
    '-O3',
    '-march=native',
    '-fopenmp',
]

extra_link_args = ['-fopenmp', '-lgmp', '-lgmpxx']

# For macOS, might need to adjust OpenMP flags
if sys.platform == 'darwin':
    # On macOS with Homebrew, OpenMP is from libomp
    extra_compile_args = [
        '-std=c++17',
        '-O3',
        '-march=native',
        '-Xpreprocessor', '-fopenmp',
    ]
    extra_link_args = ['-lomp', '-lgmp', '-lgmpxx']

ext_modules = [
    Extension(
        '_fastfib_fd',
        ['fib_bindings_fastdoubling.cpp'],
        include_dirs=[
            pybind11.get_include(),
            pybind11.get_include(user=True),
        ],
        language='c++',
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    name='fastfib_fd',
    version='2.1.0',
    author='Mike',
    description='Ultra-fast Fibonacci computation using GMP and Fast Doubling',
    ext_modules=ext_modules,
    install_requires=['pybind11>=2.6.0', 'numpy'],
    zip_safe=False,
    python_requires='>=3.7',
)

