import setuptools
import os
from distutils.extension import Extension

import numpy as np

def is_source_release(path):
    return os.path.exists(os.path.join(path, "PKG-INFO"))

def setup_package():
    root = os.path.abspath(os.path.dirname(__file__))
    extensions = [
        Extension(
            "spacy_pkuseg.inference",
            ["spacy_pkuseg/inference.pyx"],
            include_dirs=[np.get_include()],
            language="c++"
        ),
        Extension(
            "spacy_pkuseg.feature_extractor",
            ["spacy_pkuseg/feature_extractor.pyx"],
            include_dirs=[np.get_include()],
        ),
        Extension(
            "spacy_pkuseg.postag.feature_extractor",
            ["spacy_pkuseg/postag/feature_extractor.pyx"],
            include_dirs=[np.get_include()],
        ),
    ]

    if not is_source_release(root):
        from Cython.Build import cythonize
        extensions = cythonize(extensions, annotate=True)


    setuptools.setup(
        name="spacy_pkuseg",
        packages=setuptools.find_packages(),
        package_data={"": ["*.txt*", "*.pkl", "*.npz", "*.pyx", "*.pxd"]},
        ext_modules=extensions,
    )


if __name__ == "__main__":
    setup_package()
