from setuptools import setup, find_packages

setup(
    name="ai-research-agent",
    version="1.0.0",
    description="AI-Assisted Data Analysis Agent — a Python system that uses intelligent agents and tools for data analysis, conversion, and reporting.",
    author="Riga Technical University — Systems Analysis & Design",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-research-agent=src.main:main",
        ],
    },
)
