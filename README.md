# 🗃️ DaGet

S imple utility script to download datasets from data respositories.

## Usage

Download dataset via DOI or landing page url:

`python3 daget.py https://doi.org/10.5878/331q-3p13 ./destination`

## Suported data respositories (confirmed)
* Dataverse - https://dataverse.harvard.edu
* SND - https://snd.se/catalogue
* Zenodo - https://zenodo.org


## Improve the script

Adding suport for additional repositories requires test cases and investigation arround how to get file metadata from the landing page.

Please help by testing and reporting issues!

## TODO

- [ ] Add error handling
- [ ] Check empty destination directory
- [ ] Improve documentation
- [ ] Package script for pip