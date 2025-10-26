# setup.py - Package installation
from setuptools import setup, find_packages

setup(
    name="avcs-dna-matrix-soul",
    version="6.0.0",
    description="AVCS DNA Industrial Monitor with AI-Powered Predictive Maintenance",
    author="Yeruslan Technologies",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "plotly>=5.15.0",
        "joblib>=1.3.0",
        "python-dateutil>=2.8.0",
        "pytz>=2023.0",
        "pyttsx3>=2.90"
    ],
    python_requires=">=3.8",
)
