"""setuptools based setup.py module to accommodate setuptools build system

See:
    Emerging pattern to follow:
        https://github.com/pypa/sampleproject
    Transition towards pyproject.toml centric build/setup config:
        https://www.python.org/dev/peps/pep-0621/
            - Implies that much of the "packaging core metadata" in setup(...) may move to pyproject.toml
        https://snarky.ca/what-the-heck-is-pyproject-toml/
    Following a "src/" Python Package Layout:
        https://github.com/pypa/packaging.python.org/issues/320
        https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
        https://bskinn.github.io/My-How-Why-Pyproject-Src/
    Detailed overview of setuptools packaging:
        https://packaging.python.org/guides/distributing-packages-using-setuptools/

Testing:
    A local editabale install with dependent packages can be tested with a command like:
    pip install --editable git+file://<LOCAL_PATH>@<BRANCH>#egg=usaspending-api --src .
    - <LOCAL_PATH> replaced with e.g.: /Users/devmcdev/Development/myapps/thisrepo
    - <BRANCH> replaced with whatever branch or tag name in the repo you want to pull code from

"""
import pathlib

from setuptools import setup, find_packages

_PROJECT_NAME = "usaspending-api"
_SRC_ROOT_DIR = pathlib.Path(__file__).parent.resolve() / _PROJECT_NAME.replace("-", "_")
_PROJECT_ROOT_DIR = _SRC_ROOT_DIR.parent.resolve()

# Requirements
# Packages will be installed from these well-known files (if they exist) when installing this package
_install_requires = open(_PROJECT_ROOT_DIR / "requirements" / "requirements-app.txt").read().strip().split("\n")
_dev_requires = (
    open(_PROJECT_ROOT_DIR / "requirements" / "requirements-dev.txt").read().strip().split("\n")
    if (_PROJECT_ROOT_DIR / "requirements" / "requirements-dev.txt").exists()
    else []
)
_test_requires = (
    open(_PROJECT_ROOT_DIR / "requirements" / "requirements-test.txt").read().strip().split("\n")
    if (_PROJECT_ROOT_DIR / "requirements" / "requirements-test.txt").exists()
    else []
)
_extras = {"dev": _dev_requires + _test_requires}

setup(
    name=_PROJECT_NAME,
    version="0.0.0",
    description=(
        "This API is utilized by USAspending.gov to obtain all federal spending data which is open source "
        "and provided to the public as part of the DATA Act."
    ),
    long_description=(_PROJECT_ROOT_DIR / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    python_requires="==3.7.*",
    license=(_PROJECT_ROOT_DIR / "LICENSE").read_text(encoding="utf-8"),
    packages=find_packages(),
    install_requires=_install_requires,
    extras_require=_extras,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
)

if __name__ == "__main__":
    print("Running setup.__main__ from setup.py to invoke function setuptools.setup(...)")
    # NOTE: The below setup() will be called when this is invoked from a pyproject.toml build backend.
    #       But until all the packaging core metadata is moved over to the pyproject.toml file, it will remain
    #       commented out
#     setup()