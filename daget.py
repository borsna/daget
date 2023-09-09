#!/usr/bin/env python3
import urllib.request, os, argparse, json

# test dataset with subdirs: https://doi.org/10.5878/331q-3p13

def main():
  parser = argparse.ArgumentParser(
              prog='dget',
              description='download dataset via doi or landing page url',
              epilog='To improve or report a bug goto github.com/bla/bla'
  )

  parser.add_argument('url')
  parser.add_argument('destination') 

  args = parser.parse_args()

  desitnation = os.path.realpath(args.destination)

  if not os.path.exists(desitnation):
    os.makedirs(desitnation)

  print("📂",desitnation)

  url = get_redirect_url(args.url)
  json = get_schema_org(url)

  total_size = 0

  for file in json['distribution']:
    total_size += file['contentSize']
    print("📄",file['name'], bcolors.OKBLUE, sizeof_fmt(file['contentSize']), bcolors.ENDC)
    file_path = os.path.join(desitnation, file['name'])
    file_dir = os.path.dirname(file_path)
    
    if not os.path.exists(file_dir):
      os.makedirs(file_dir)

    download_file(file['contentUrl'], file_path)

  print("🗃️ total downloaded: ", bcolors.OKGREEN, sizeof_fmt(total_size), bcolors.ENDC)

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def get_redirect_url(url):
  r = urllib.request.urlopen(url)
  return r.geturl()

def get_schema_org(url):
  opener = urllib.request.build_opener()
  opener.addheaders = [('Accept', 'application/ld+json')]
  urllib.request.install_opener(opener)
  r = urllib.request.urlopen(url)
  return json.loads(r.read())

def show_progress(block_num, block_size, total_size):
  print(bcolors.OKGREEN, "⬇️", round(block_num * block_size / total_size *100, 1), "%", bcolors.ENDC, end="\r")

def download_file(url, target):
  url = url + "&noLog=true"
  urllib.request.urlretrieve(url, target, show_progress)

def sizeof_fmt(num, suffix="B"):
  for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
    if abs(num) < 1024.0:
      return f"{num:3.1f}{unit}{suffix}"
    num /= 1024.0
  return f"{num:.1f}Yi{suffix}"

if __name__ == "__main__":
    main()