from setuptools import setup, find_packages

setup(
    name='daget',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/borsna/daget',
    license='MIT',
    author='Olof Olsson',
    author_email='borsna@gmail.com',
    python_requires='>=3.6',
    description='Download dataset via DOI or landing page url',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'daget=daget.daget:main',
        ],
    },
)