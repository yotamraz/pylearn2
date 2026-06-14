"""Minimal setup.py shim for Cython extension modules.

All project metadata is in pyproject.toml. This file exists only to declare
the Cython extensions that cannot be specified in pyproject.toml directly.
"""
import warnings

import numpy
from setuptools import Extension, setup

try:
    from Cython.Build import cythonize
    cython_available = True
except ImportError:
    warnings.warn(
        "Cython was not found. pylearn2.utils._window_flip, "
        "pylearn2.utils._video, and pylearn2.models._kmeans will not be "
        "available."
    )
    cython_available = False

if cython_available:
    try:
        ext_modules = cythonize([
            Extension(
                "pylearn2.utils._window_flip",
                ["pylearn2/utils/_window_flip.pyx"],
                include_dirs=[numpy.get_include()],
            ),
            Extension(
                "pylearn2.utils._video",
                ["pylearn2/utils/_video.pyx"],
                include_dirs=[numpy.get_include()],
            ),
            Extension(
                "pylearn2.models._kmeans",
                ["pylearn2/models/_kmeans.pyx"],
                include_dirs=[numpy.get_include()],
            ),
        ])
    except Exception as e:
        warnings.warn(
            f"Cython compilation failed ({e}). Extension modules "
            "pylearn2.utils._window_flip, pylearn2.utils._video, and "
            "pylearn2.models._kmeans will not be available. "
            "Fix the .pyx files in a future milestone to enable them."
        )
        ext_modules = []
else:
    ext_modules = []

setup(ext_modules=ext_modules)
