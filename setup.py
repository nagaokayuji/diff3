import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="diff3",
    version="0.1.0",
    author="Yuji Nagaoka",
    author_email="yvay5cqe@gmail.com",
    description="A simple diff and diff3 implementation in Python",
    url="https://github.com/nagaokayuji/diff3",
    long_description=long_description,
        long_description_content_type="text/markdown",
    license="MIT",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
