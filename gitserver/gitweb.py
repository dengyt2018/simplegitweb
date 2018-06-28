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
    params = parse_qs(req.environ['QUERY_STRING'])
    new_repository = params.get('add_new_repository', [None])[0]+".git"
    
    if new_repository and new_repository not in repos.split(";"):
        #Repo.init_bare(os.path.join(InitRepoPath(CONFIG_NAME).get_scanpath(), new_repository), mkdir=True)
        pass

    yield env.get_template("index.html").render(repos_list=repos).encode()


class InitRepoPath():
    def __init__(self, CONFIG_NAME=None):
        self.config_name = CONFIG_NAME
        if self.config_name:
            self.config = self.get_config() 
    
    def get_config(self):
        if Path(self.config_name).exists():
            with open(self.config_name, 'r') as fp:
                config = copy.deepcopy(json.loads(fp.read()))
            if config:
                return config

    def __call__(self):
        return self.config if self.config else None

    def get_scanpath(self):
        if self.config and self.config.get('scanpath'):
            scanpath = os.path.abspath(self.config['scanpath'])
            return scanpath
        
    def get_backends(self):
        path = self.get_scanpath()
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
        return str(self.config)
        
HTTPGitApplication.services[('GET', re.compile('^/$'))] = get_root_index
HTTPGitApplication.services[('GET', re.compile('^/repository'))] = get_root_index

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
    

