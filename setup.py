"""
Setup script for CSV to Dashboard package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="csv2dashboard",
    version="1.0.0",
    author="CSV Dashboard Team",
    author_email="team@csvdashboard.com",
    description="Convert CSV/Excel files into interactive web dashboards and static HTML reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soroush-thr/csv2dashboard",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "csv2dashboard=csvdash.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
