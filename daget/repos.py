import requests, urllib, json.decoder
from bs4 import BeautifulSoup

def get_file_list_from_repo(url):
  url_parsed = urllib.parse.urlparse(url)

  if url_parsed.hostname == 'zenodo.org':
    id = url_parsed.path.split('/')[-1]
    return get_file_list_zenodo(id)
  elif 'figshare' in url_parsed.hostname:
    id = url_parsed.path.split('/')[-2]
    version = url_parsed.path.split('/')[-1]
    return get_file_list_figshare(id, version)
  else:
    return get_file_list_schema_org(url)

def get_file_list_schema_org(url):
  daget_headers={'User-Agent' : 'daget', 'Accept' : 'application/ld+json'}
  
  result = requests.get(url, headers=daget_headers)
    
  # retry with host header 
  if not result.ok:
    daget_headers['Host'] = 'localhost'
    result = requests.get(url, headers=daget_headers)
  
  try:
    schema_org = result.json()
  except:
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    text = "".join(soup.find('script', {'type':'application/ld+json'}).contents)
    
    schema_org = json.loads(text)
  
  schema_files = schema_org['distribution']
  if not isinstance(schema_files, list):
    schema_files = [schema_files]
  
  files = []
  for f in schema_files:
    size = f.get('contentSize', None)
    if isinstance(size, str) and size.lower().endswith('b'):
      size = size.lower().replace('b', '').strip().trim()

    file={
      'url'  : f.get('contentUrl', None),
      'size' : int(size) if size else None,
      'name' : f.get('name', None)
    }
    files.append(file)
  
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