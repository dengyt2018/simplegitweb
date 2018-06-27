from pathlib import Path
import json
import copy
import os

from dulwich.repo import Repo
from dulwich.web import *

from jinja2 import Environment, PackageLoader, select_autoescape, Template

env = Environment(
    loader=PackageLoader('gitserver', 'templates'),
    autoescape=select_autoescape(['html'])
)

CONFIG_NAME = 'gitserver.json'

def get_root_index(req, backen, mat):
    req.respond(HTTP_OK, 'text/html')
    repos = ";".join([c for c in backen.repos.keys()])
    yield env.get_template("index.html").render(repos_list=repos).encode()

    
class InitRepoPath():
    def __init__(self, CONFIG_NAME=None):
        self.CONFIG_NAME = CONFIG_NAME
        if self.CONFIG_NAME:
            self.CONFIG = self.get_CONFIG() 
    
    def get_CONFIG(self):
        if Path(self.CONFIG_NAME).exists():
            with open(self.CONFIG_NAME, 'r') as fp:
                CONFIG = copy.deepcopy(json.loads(fp.read()))
            if CONFIG:
                return CONFIG

    def __call__(self):
        return self.CONFIG if self.CONFIG else None
    
    def get_scanpath(self):
        if self.CONFIG and self.CONFIG.get('scanpath'):
            SCANPATH = self.CONFIG['scanpath']
            return SCANPATH
        
    def get_backends(self):
        path = os.path.abspath(self.get_scanpath())
        try:
            reposdir = os.listdir(path)
        except FileNotFoundError:
            return None

        backends = dict()
        for i in reposdir:
            repo_path = os.path.join(path, i)
            try:
                repo = Repo(repo_path)
            except:
                continue
            backends[str('/'+i)] = repo
            del repo
        return backends

    def __repr__(self):
        return str(self.CONFIG)
        
HTTPGitApplication.services[('GET', re.compile('^/$'))] = get_root_index

def main():
    """Entry point for starting an HTTP git server."""
    listen_address, port = "127.0.0.5", 3000

    backend = DictBackend(InitRepoPath(CONFIG_NAME).get_backends())
        
    app = make_wsgi_chain(backend)
    server = make_server(listen_address, port, app,
                         handler_class=WSGIRequestHandlerLogger,
                         server_class=WSGIServerLogger)
    logger.info('Listening for HTTP connections on %s:%d',
                listen_address, port)
    server.serve_forever()


if __name__ == '__main__':
    main()
    

