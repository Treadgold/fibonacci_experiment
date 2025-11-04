"""
Setup script for fastfib - Ultra-fast Fibonacci computation
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os
import pybind11

class get_pybind_include:
    def __str__(self):
        return pybind11.get_include()

# Platform-specific compiler flags
if sys.platform == 'win32':  # Windows (MSVC)
    extra_compile_args = [
        '/std:c++17',
        '/O2',          # Maximum optimization
        '/openmp',      # OpenMP support
        '/GL',          # Whole program optimization
        '/favor:blend', # Optimize for mixed workload
    ]
    extra_link_args = [
        '/LTCG',        # Link-time code generation
    ]
    libraries = ['gmp']
elif sys.platform == 'darwin':  # macOS
    extra_compile_args = [
        '-std=c++17',
        '-O3',
        '-funroll-loops',
        '-fomit-frame-pointer',
        '-finline-functions',
    ]
    extra_link_args = []
    libraries = ['gmp', 'gmpxx']
    
    # Try to use libomp if available
    if os.path.exists('/usr/local/opt/libomp'):
        extra_compile_args.append('-Xpreprocessor')
        extra_compile_args.append('-fopenmp')
        extra_compile_args.append('-I/usr/local/opt/libomp/include')
        extra_link_args.append('-L/usr/local/opt/libomp/lib')
        extra_link_args.append('-lomp')
    elif os.path.exists('/opt/homebrew/opt/libomp'):  # Apple Silicon
        extra_compile_args.append('-Xpreprocessor')
        extra_compile_args.append('-fopenmp')
        extra_compile_args.append('-I/opt/homebrew/opt/libomp/include')
        extra_link_args.append('-L/opt/homebrew/opt/libomp/lib')
        extra_link_args.append('-lomp')
    
    # Add GMP paths for Homebrew
    if os.path.exists('/usr/local/opt/gmp'):
        extra_compile_args.append('-I/usr/local/opt/gmp/include')
        extra_link_args.append('-L/usr/local/opt/gmp/lib')
    elif os.path.exists('/opt/homebrew/opt/gmp'):  # Apple Silicon
        extra_compile_args.append('-I/opt/homebrew/opt/gmp/include')
        extra_link_args.append('-L/opt/homebrew/opt/gmp/lib')
else:  # Linux and other Unix-like (including WSL)
    extra_compile_args = [
        '-std=c++17',
        '-O3',
        '-march=native',
        '-mtune=native',
        '-fopenmp',
        '-funroll-loops',
        '-fomit-frame-pointer',
        '-finline-functions',
    ]
    extra_link_args = [
        '-fopenmp',
    ]
    libraries = ['gmp', 'gmpxx']

ext_modules = [
    Extension(
        'fastfib._fastfib',
        ['fib_bindings.cpp'],
        include_dirs=[
            get_pybind_include(),
            pybind11.get_include(),
        ],
        language='c++',
        libraries=libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    name='fastfib',
    version='2.0.0',
    author='FastFib Contributors',
    description='Ultra-fast EXACT Fibonacci computation using C++, GMP, and matrix exponentiation',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    ext_modules=ext_modules,
    packages=['fastfib'],
    install_requires=[
        'numpy>=1.19.0',
        'pybind11>=2.6.0',
    ],
    python_requires='>=3.7',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)

