# 🗃️ DaGet

Simple utility script to download datasets from data respositories.

⚠️ __script is in early development and needs testing__ ⚠️ 

## Usage

Download dataset via DOI or landing page url:

`python3 daget.py https://doi.org/10.5878/331q-3p13 ./destination`

## Suported data respositories (confirmed)
* Dataverse - https://dataverse.harvard.edu
* SND - https://snd.se/catalogue
* Zenodo - https://zenodo.org

## Semi-suported respositories 
* Figshare - https://su.figshare.com & https://figshare.scilifelab.se (more testing needed)

## Improve the script

Adding suport for additional repositories requires test cases and investigation arround how to get file metadata from the landing page.

Please help by testing and reporting issues!

## TODO

- [ ] Add error handling
- [ ] Check empty destination directory
- [ ] Improve documentation
- [ ] Package script for pip