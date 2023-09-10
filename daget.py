#!/usr/bin/env python3
import urllib.request, requests, os, argparse, json, urllib.parse

# test dataset with subdirs: https://doi.org/10.5878/331q-3p13

def main():
  parser = argparse.ArgumentParser(
            prog='daget',
            description='Download dataset via DOI or landing page url',
            epilog='To improve or report a bug https://github.com/borsna/daget'
  )

  parser.add_argument('url', help="URL to the dataset (lanmding page or DOI)")
  parser.add_argument('destination', help="Full or relative path to destination directory") 

  args = parser.parse_args()

  desitnation = os.path.realpath(args.destination)

  if not os.path.exists(desitnation):
    os.makedirs(desitnation)

  print("📂",desitnation)

  url = get_redirect_url(args.url)
  print("🔗 landing page: ", url)
  files = get_file_list(url)

  total_size = 0

  for file in files:
    total_size += file['size']
    print("📄", bcolors.OKBLUE, sizeof_fmt(file['size']), bcolors.ENDC, "\t", file['name'])
    file_path = os.path.join(desitnation, file['name'])
    file_dir = os.path.dirname(file_path)
    
    if not os.path.exists(file_dir):
      os.makedirs(file_dir)

    download_file(file['url'], file_path)

  print("🗃️ ", bcolors.OKGREEN, sizeof_fmt(total_size), bcolors.ENDC, " downloaded ")

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
  opener = urllib.request.build_opener()
  opener.addheaders = [('User-Agent', 'daget')]
  urllib.request.install_opener(opener)
  r = urllib.request.urlopen(url)
  return r.geturl()

def get_file_list(url):
  url_parsed = urllib.parse.urlparse(url)

  if url_parsed.hostname == 'zenodo.org':
    id = url_parsed.path.split('/')[-1]
    return get_file_list_zenodo(id)
  elif 'figshare' in url_parsed.hostname:
    id = url_parsed.path.split('/')[-2]
    version = url_parsed.path.split('/')[-1]
    print("FÄGSJ*RS")
    return get_file_list_figshare(id, version)
  else:
    return get_file_list_schema_org(url)
    
def get_file_list_schema_org(url):
  try:
    r=requests.get(url, headers={'User-Agent' : 'daget', 'Accept' : 'application/ld+json'})
    schema_org = r.json()
  except:
    r=requests.get(url, headers={'Host': 'daget', 'User-Agent' : 'daget', 'Accept' : 'application/ld+json'})
    schema_org = r.json()
  
  files = []
  for file in schema_org['distribution']:
    files.append({
      'url'  : file['contentUrl'],
      'size' : file['contentSize'],
      'name' : file['name']
    })
  
  return files

def get_file_list_zenodo(id):
  url = "https://zenodo.org/api/records/{id}".format(id = id)
  r = requests.get(url, headers={'Host': 'localhost', 'User-Agent' : 'daget', 'Accept' : '*/*'})
  meta = r.json()
  
  files = []

  for file in meta['files']:
    files.append({
      'url'  : file['links']['self'],
      'size' : file['size'],
      'name' : file['key']
    })
  return files

def get_file_list_figshare(id, version):
  url = "https://api.figshare.com/v2/articles/{id}/versions/{version}".format(id = id, version = version)
  r = requests.get(url, headers={'Host': 'localhost', 'User-Agent' : 'daget', 'Accept' : '*/*'})
  meta = r.json()
  files = []

  for file in meta['files']:
    files.append({
      'url'  : file['download_url'],
      'size' : file['size'],
      'name' : file['name']
    })
  return files

def show_progress(block_num, block_size, total_size):
  print(bcolors.OKGREEN, "⬇️", round(block_num * block_size / total_size *100, 1), "%", bcolors.ENDC, end="\r")

def download_file(url, target):
  #url = url + "&noLog=true"  # for test only, disable logging when dowloading
  opener = urllib.request.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept', '*/*')]
  urllib.request.install_opener(opener)
  urllib.request.urlretrieve(url, target, show_progress)

def sizeof_fmt(num, suffix="B"):
  for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
    if abs(num) < 1024.0:
      return f"{num:3.1f}{unit}{suffix}"
    num /= 1024.0
  return f"{num:.1f}Yi{suffix}"

if __name__ == "__main__":
    main()