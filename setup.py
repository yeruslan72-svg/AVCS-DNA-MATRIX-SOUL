# setup.py - Package installation for AVCS DNA Matrix Soul
from setuptools import setup, find_packages
import os

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="avcs-dna-matrix-soul",
    version="6.0.0",
    author="Yeruslan Technologies",
    author_email="contact@yeruslan.tech",
    description="AVCS DNA Industrial Monitor with AI-Powered Predictive Maintenance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yeruslan/avcs-dna-matrix-soul",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Monitoring",
    ],
    keywords="industrial, monitoring, predictive-maintenance, ai, vibration, thermal",
    install_requires=[
        "streamlit>=1.28.0,<2.0.0",
        "numpy>=1.24.0,<2.0.0",
        "pandas>=2.0.0,<3.0.0", 
        "scikit-learn>=1.3.0,<2.0.0",
        "plotly>=5.15.0,<6.0.0",
        "joblib>=1.3.0",
        "python-dateutil>=2.8.0",
        "pytz>=2023.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "avcs-dna=thermal_dna_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "avcs_dna": ["config/*.json", "models/*.pkl"],
    },
    project_urls={
        "Documentation": "https://github.com/yeruslan/avcs-dna-matrix-soul/docs",
        "Source": "https://github.com/yeruslan/avcs-dna-matrix-soul",
        "Tracker": "https://github.com/yeruslan/avcs-dna-matrix-soul/issues",
    },
)
