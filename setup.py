from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="trainalert",
    version="0.1.0",
    author="Darshan Rajopadhye",
    author_email="therrshan@gmail.com",
    description="Smart notification system for ML training workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/therrshan/trainalert",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "pillow>=9.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
)