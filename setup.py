import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmdshow-anihm136",
    version="0.1.0",
    author="Example Author",
    author_email="anihm136@gmail.com",
    description="A library and tool to create slideshows from images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anihm136/cmdshow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop"
    ],
    python_requires=">=3.8",
)
