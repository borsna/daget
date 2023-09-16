# 🗃️ DaGet

Simple utility to download datasets from data respositories.

⚠️ __script is in early development and needs testing__ ⚠️ 

## Installation

![PyPI](https://img.shields.io/pypi/v/daget)

to install daget using pip: 

```
pip install daget
```

## Usage

Download dataset via DOI or landing page url:

`daget https://doi.org/10.5878/331q-3p13 ./destination`

or short form doi:

`daget 10.5878/331q-3p13 ./destination`

## Suported data respositories (confirmed)
* Dataverse - https://dataverse.harvard.edu
* SND - https://snd.se/catalogue
* Zenodo - https://zenodo.org

## Semi-suported respositories 
* Figshare - https://su.figshare.com & https://figshare.scilifelab.se (more testing needed)

## Improve the script

Adding suport for additional repositories requires test cases and investigation arround how to get file metadata from the landing page.

Please help by testing and reporting [issues](https://github.com/borsna/daget/issues)!!

## TODO

- [ ] Add error handling
- [ ] Check empty destination directory
- [ ] Improve documentation
- [x] Package script for pip
