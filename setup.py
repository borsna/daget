from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='daget',
    version='0.2',
    packages=find_packages(),
    url='https://github.com/borsna/daget',
    license='MIT',
    author='Olof Olsson',
    author_email='borsna@gmail.com',
    python_requires='>=3.6',
    description='Download dataset via DOI or landing page url',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'daget=daget.daget:main',
        ],
    },
)