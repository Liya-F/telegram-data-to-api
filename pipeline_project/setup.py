from setuptools import find_packages, setup

setup(
    name="pipeline_project",
    packages=find_packages(exclude=["pipeline_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
