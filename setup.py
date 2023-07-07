import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.txt").read_text()

# This call to setup() does all the work
setup(
    name="lisp_emulator",
    version="1.0.3",
    description="Emulate basic Lisp environment in python for educational reasons.",
    long_description=README,
    long_description_content_type="text/plain",
    author="jonas",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["lisp_emulator"],
    include_package_data=True,
    install_requires=["pyfiglet"],
)