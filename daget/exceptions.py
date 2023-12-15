class ResolveError(ValueError):
    def __init__(self, message, http_response_code=None):
        super().__init__(message)
        self.http_response_code = http_response_code

class RepoError(ValueError):
    def __init__(self, message, url, supported_urls=None, http_response_code=None):
        super().__init__(message)
        self.url = url
        self.supported_urls = supported_urls or ["dataverse.harvard.edu", "dataverse.no", "snd.se/catalogue", "su.figshare.com", "figshare.scilifelab.se", "zenodo.org"]
        self.http_response_code = http_response_code

        if url not in self.supported_urls:
            raise self