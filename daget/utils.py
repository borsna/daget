import re
import socket
import urllib, urllib.error
from daget.exceptions import RepoError, ResolveError


def get_redirect_url(url):
  # if url provided is a shorthand doi (TODO: check with regex)
  if not re.match(r'^https?://', url):
    url = 'https://doi.org/' + url

  opener = urllib.request.build_opener()
  opener.addheaders = [('User-Agent', 'daget')]
  urllib.request.install_opener(opener)
  
  try:
    response = urllib.request.urlopen(url)
    return response.geturl()

  except urllib.error.HTTPError as e:
      # Catch HTTP errors and extract relevant information
      error_message = f"HTTPError: {e.code} - {e.reason}"
      raise ResolveError(f"{url} not found. {error_message}")

  except urllib.error.URLError as e:
      # Catch URL errors (e.g., network issues) and provide relevant information
      if isinstance(e.reason, str):
          error_message = f"URLError: {e.reason}"
      else:
          error_message = f"URLError: {str(e.reason)}"

      # Additional handling for socket.gaierror
      if isinstance(e.reason, socket.gaierror):
          error_message += f", errno: {e.reason.errno}, strerror: {e.reason.strerror}"

      raise ResolveError(f"Error connecting to {url}. {error_message}")
  
def download_file(url, target):
  opener = urllib.request.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept', '*/*')]
  urllib.request.install_opener(opener)
  urllib.request.urlretrieve(url, target, show_progress)

def size_as_string(bytes, suffix="B"):
  for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
    if abs(bytes) < 1024.0:
      return f"{bytes:3.1f}{unit}{suffix}"
    bytes /= 1024.0
  return f"{bytes:.1f}Yi{suffix}"

def show_progress(block_num, block_size, total_size):
  print(bcolors.OKGREEN, round(block_num * block_size / total_size *100, 1), "%", bcolors.ENDC, end="\r")

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