# :coding: utf-8

import os.path
import setuptools

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(ROOT_PATH, "source")
README_PATH = os.path.join(ROOT_PATH, "README.rst")

long_description = "Placeholder"

# Compute dependencies.
INSTALL_REQUIRES = [
    "click >= 7, < 8",
    "Pillow >= 8, < 9",
    "flask >= 1, < 2",
    "python-dotenv >= 0.1.0, < 1",
    "gunicorn >= 20, < 21",
]

TEST_REQUIRES = [
    "pytest >= 4, < 5",
    "pytest-benchmark >= 3.2.3, < 4",
    "pytest-cov >= 2, < 3",
    "pytest-mock >= 2, < 3",
    "pytest-runner >= 2.7, < 3",
    "pytest-xdist >= 1.18, < 2"
]


setuptools.setup(
    name="synes",
    version="0.1.0",
    author="Zephyr Mann",
    author_email="zephmann@gmail.com",
    description="Translate image to audio and vice versa.",
    long_description="Translate image to audio and vice versa.",
    url="https://github.com/zephmann/synes",
    packages=setuptools.find_packages(SOURCE_PATH),
    package_dir={
        "": "source"
    },
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    extras_require={
        "test": TEST_REQUIRES,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "synes = synes.command_line:main"
        ]
    },
)
