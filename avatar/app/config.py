import os
from pathlib import Path


# For API communications between dev instances
# Replace https://localhost:port with respective codespaces url for codespaces
os.environ['CREDEX_CORE_API_URL'] = 'https://stunning-garbanzo-v766w6pwjw53p6q4-8080.app.github.dev/api/v1/ '
os.environ['VIMBISO_PAY_API_URL'] = 'https://stunning-garbanzo-v766w6pwjw53p6q4-8080.app.github.dev/ '

# GitHub configuration
GH_USERNAME = os.environ.get('GH_USERNAME')
GH_PAT = os.environ.get('GH_PAT')
GH_ORGANIZATION = 'Great-Sun-Group'

# Repository structure
ROOT_REPO = 'greatsun-dev'
MODULE_FOLDER = 'credex-ecosystem'
SUBMODULES = ['credex-core', 'vimbiso-pay']

# Paths and home
BASE_DIR = Path('/workspaces/greatsun-dev')
ROOT_PATH = os.getcwd()
MODULE_PATH = os.path.join(ROOT_PATH, MODULE_FOLDER)
