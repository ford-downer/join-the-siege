from setuptools import setup, find_packages

setup(
    name="document-classifier",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.2",
        "uvicorn>=0.27.1",
        "python-multipart>=0.0.6",
        "scikit-learn>=1.3.2",
        "joblib>=1.3.2",
        "PyPDF2>=3.0.1",
        "Pillow>=10.2.0",
        "numpy>=1.26.4",
        "pandas>=2.2.1",
        "pydantic>=2.6.1",
    ],
    python_requires=">=3.12",
) 