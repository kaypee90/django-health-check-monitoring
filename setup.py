from setuptools import setup, find_packages

setup(
    name="django-health-check-job",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Django>=2.2",
    ],
)