import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synes",
    version="0.0.1",
    author="Zephyr Mann",
    author_email="zephmann@gmail.com",
    description="Translate image to audio and vice versa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zephmann/synes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
