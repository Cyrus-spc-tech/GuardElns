"""
GuardELNS Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="guardelns",
    version="1.0.0",
    author="GuardELNS Team",
    author_email="guardelns@cecj.edu",
    description="AI-Powered Enterprise-Level Network Security Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/guardelns",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.31.0",
        "pandas>=2.1.4",
        "numpy>=1.26.3",
        "scikit-learn>=1.4.0",
        "pyod>=1.1.3",
        "scapy>=2.5.0",
        "plotly>=5.18.0",
        "matplotlib>=3.8.2",
        "seaborn>=0.13.1",
        "networkx>=3.2.1",
        "paho-mqtt>=1.6.1",
        "pyyaml>=6.0.1",
        "sqlalchemy>=2.0.25",
        "psutil>=5.9.8",
        "requests>=2.31.0",
        "python-dotenv>=1.0.1",
    ],
)
