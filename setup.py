"""
    reference: https://pythonhosted.org/an_example_pypi_project/setuptools.html
"""

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
print(HERE)
README = (HERE / "README.md").read_text()
# This call to setup() does all the work
setup(
    name="simple_scheduler",
    version="1.0.2",
    description="Easily schedule multiple events and recurring tasks (simultaneously).",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Vernal-Inertia/simple_scheduler",
    author="Vernal Inertia",
    author_email="tanveer2407@gmail.com",
    license="MIT",
    keywords='python, schedule, simple',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha"
    ],
    packages=["simple_scheduler"],
    include_package_data=True,
    install_requires=["pytz"],
    python_requires='>=3',
    project_urls={
        'Issues': 'https://github.com/Vernal-Inertia/simple_scheduler/issues',
        'Documentation': 'https://github.com/Vernal-Inertia/simple_scheduler/blob/main/README.md',
        'Source': 'https://github.com/Vernal-Inertia/simple_scheduler'}
)
