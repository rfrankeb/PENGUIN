"""
Setup script for PENGUIN
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="penguin",
    version="0.1.0",
    author="PENGUIN Team",
    description="AI-Powered Stock Analysis Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "praw>=7.7.1",
        "yfinance>=0.2.40",
        "sqlalchemy>=2.0.31",
        "psycopg2-binary>=2.9.9",
        "alembic>=1.13.2",
        "aiohttp>=3.9.5",
        "click>=8.1.7",
        "pandas>=2.2.2",
        "numpy>=1.26.4",
        "python-dotenv>=1.0.1",
        "requests>=2.32.3",
    ],
    entry_points={
        'console_scripts': [
            'penguin=penguin.cli.main:cli',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
