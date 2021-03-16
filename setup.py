import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
print(HERE)
README = (HERE / "README.md").read_text()
print(README)
# This call to setup() does all the work
setup(
    name="simple_scheduler",
    version="1.0.0",
    description="Easily schedule multiple events and recurring tasks (simultaneously).",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Vernal-Inertia/simple_scheduler",
    author="Vernal Inertia",
    author_email="tanveer2407@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["simple_scheduler"],
    include_package_data=True,
    install_requires=["multiprocessing"],
    entry_points={
        "console_scripts": [
            "simple_scheduler=__main__:main",
        ]
    },
)
