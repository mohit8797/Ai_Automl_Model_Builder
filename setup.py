#!/usr/bin/env python
"""
Setup configuration for AutoML Model Builder package distribution.
Enables: pip install -e . for development mode
         pip install . for normal installation
         pip install -r requirements.txt for dependencies
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="automl-model-builder",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Professional AutoML platform for rapid model prototyping and deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/automl-model-builder",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/automl-model-builder/issues",
        "Documentation": "https://github.com/yourusername/automl-model-builder/wiki",
        "Source Code": "https://github.com/yourusername/automl-model-builder",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "automl-builder=app.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "automl", "machine-learning", "deep-learning", "neural-networks",
        "tensorflow", "keras", "data-science", "ai", "ml-ops"
    ],
)
