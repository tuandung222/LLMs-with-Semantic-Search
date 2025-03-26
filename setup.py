from setuptools import setup, find_packages

setup(
    name="semantic_search",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "openai",
        "weaviate-client",
        "numpy",
        "pandas",
    ],
) 