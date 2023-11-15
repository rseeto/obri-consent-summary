from setuptools import find_packages, setup

setup(
    name="obri_consent_summary",
    packages=find_packages(exclude=["obri_consent_summary_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
