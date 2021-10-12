from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A CXL protocol parser'

# Setting up
setup(
    name="pyCXL",
    version=VERSION,
    author="svanotte (Sam Van Otterloo)",
    author_email="<sam.van.otterloo@intel.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'CXL', 'Protocol'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)