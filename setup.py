"""Setup script for Inoreader Intelligence"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="inoreader-intelligence",
    version="1.0.0",
    author="Joel Poah",
    author_email="joelpoah@gmail.com",
    description="Generate daily intelligence reports from Inoreader RSS feeds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joelpoah/inoreader-intelligence",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "python-dotenv>=1.0.0",
        "jinja2>=3.1.0",
        "weasyprint>=59.0",
        "apscheduler>=3.10.0",
        "openai>=1.0.0",
        "pydantic>=2.0.0",
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pytz>=2023.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "inoreader-intelligence=inoreader_intelligence.cli:main",
        ],
    },
)