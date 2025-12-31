"""
项目安装配置文件

支持通过 pip install -e . 本地开发安装
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="recsys",
    version="1.0.0",
    author="RecSystem Developer",
    description="双智能体协作的推荐系统，支持智能体演化和持续学习",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/recsys",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "networkx>=3.0",
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "recsys-demo=examples.evolution_demo:main",
        ],
    },
)
