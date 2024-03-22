from setuptools import find_packages, setup

setup(
    name="obri_consent_summary",
    packages=find_packages(exclude=["obri_consent_summary_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "io",
        "requests",
        "datetime",
        "numpy",
        "pandas",
        "dropbox"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
