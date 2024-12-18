from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="steel-langchain",
    version="0.1.0",
    author="Reza Jafar",
    author_email="admin@rezajafar.com",
    description="Steel integration for LangChain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rezapex/langchain/tree/add_steel_loader",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain-core",
        "langchain-community",
        "langchain-openai",
        "steel-sdk>=0.1.0b3",
        "playwright>=1.48.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=4.0",
        ],
    },
)
