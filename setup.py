import setuptools
import os
from distutils.extension import Extension

import numpy as np

def is_source_release(path):
    return os.path.exists(os.path.join(path, "PKG-INFO"))

def setup_package():
    root = os.path.abspath(os.path.dirname(__file__))

    long_description = "file: README.md"
    long_description_content_type = "text/markdown"

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
        version="0.0.27",
        author="Explosion",
        author_email="contact@explosion.ai",
        description="A small package for Chinese word segmentation",
        long_description=long_description,
        long_description_content_type=long_description_content_type,
        url="https://github.com/explosion/spacy-pkuseg",
        packages=setuptools.find_packages(),
        package_data={"": ["*.txt*", "*.pkl", "*.npz", "*.pyx", "*.pxd"]},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: Other/Proprietary License",
            "Operating System :: OS Independent",
        ],
        install_requires=["cython", "numpy>=1.16.0", "srsly>=2.3.0,<3.0.0"],
        setup_requires=["cython", "numpy>=1.16.0"],
        ext_modules=extensions,
        zip_safe=False,
    )


if __name__ == "__main__":
    setup_package()
