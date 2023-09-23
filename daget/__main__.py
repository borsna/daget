#!/usr/bin/env python3
import os, argparse
from daget.utils import *
from daget.repos import get_file_list_from_repo
from daget.exceptions import ResolveError, RepoError

# test dataset with subdirs: https://doi.org/10.5878/331q-3p13

def main():
  parser = argparse.ArgumentParser(
            prog='daget',
            description='Download dataset via DOI or landing page url',
            epilog='To improve or report a bug https://github.com/borsna/daget'
  )

  parser.add_argument('url', help="URL/DOI to the dataset")
  parser.add_argument('destination', help="Full or relative path to destination directory") 
  parser.add_argument("-l", "--list-only", action="store_true", help="Skip download")

  args = parser.parse_args()

  # get doi/url and resolve to landing page
  try:
    url = get_redirect_url(args.url)
  except ResolveError as err:
    print(bcolors.FAIL, f'error resolving {args.url}', bcolors.ENDC)
    exit(1)
  
  print(f'landing page: {url}')

  # get desitnation directory and create directory
  desitnation = os.path.realpath(args.destination)

  if not os.path.exists(desitnation):
    os.makedirs(desitnation)
  else:
    if len(os.listdir(desitnation)) != 0:
      print(bcolors.FAIL, f'{desitnation} must be a empty directory or new directory path', bcolors.ENDC)
      exit(1)

  print(f'destination: {desitnation}')

  files = get_file_list_from_repo(url)

  total_size = 0

  for file in files:
    total_size += file['size']
    print(bcolors.OKBLUE, size_as_string(file['size']).strip(), bcolors.ENDC, file['name'])
    file_path = os.path.join(desitnation, file['name'])
    file_dir = os.path.dirname(file_path)
    
    if not os.path.exists(file_dir):
      os.makedirs(file_dir)
    if(not args.list_only):
      download_file(file['url'], file_path)

  print(bcolors.OKGREEN, bcolors.BOLD, size_as_string(total_size), bcolors.ENDC, "downloaded ")

if __name__ == "__main__":
    main()