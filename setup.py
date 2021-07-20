"""Setup titiler-application."""

from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    inst_reqs = f.readlines()

with open('requirements-dev.txt') as f:
    test_reqs = f.readlines()

with open('deployment/requirements.txt') as f:
    deploy_reqs = f.readlines()

extra_reqs = {
    "test": test_reqs,
    "server": ["uvicorn[standard]>=0.12.0,<0.14.0"],
    "deploy": deploy_reqs,
}


setup(
    name="cava-tiler",
    version="0.1.0",
    description=u"CAVA Tile Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    author=u"Landung Setiawan",
    author_email="landungs@uw.edu",
    url="https://github.com/cormorack/cava-tiler",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
