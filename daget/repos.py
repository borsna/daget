import requests, urllib

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