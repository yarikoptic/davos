# TODO: add module docstring
from pathlib import Path


DAVOS_CONFIG_DIR = Path.home().joinpath('.davos')
DAVOS_PROJECT_DIR = DAVOS_CONFIG_DIR.joinpath('projects')


class Project:
    """
    A pseudo-environment associated with a particular (set of)
    davos-enhanced notebook(s)
    """

    def __new__(cls, name):
        # TODO: add docstring explaining subclass customization
        """
        if name is a file path
            ((decided based on having a '/' in it))
                ((means that relative path to file in CWD must be prefixed with ./))
            ((use case: user wants notebook to use same environment as existing notebook))
            convert to pathlib.Path, resolve, sub variables, expanduser, etc.
            if path points to real, existing *.ipynb* file
                OK, sure
            else
                raise error
        else
            treat name as just a name
        """
        if isinstance(name, Path):
            # convert Paths to strings so they can be properly expanded,
            # substituted, resolved, etc. below
            name = str(name)
        # convert safe dirname replacement to os.sep (to handle reading
        # project directory names from DAVOS_PROJECT_DIR)
        name = name.replace(PATHSEP_REPLACEMENT, PATHSEP)
        child_cls_to_init = ConcreteProject
        if PATHSEP in name:
            # name is a file path
            name_path = Path(expandvars(name)).expanduser().resolve()
            if name_path.suffix != '.ipynb':
                raise DavosProjectError('')


        if isinstance(name, str):
            name = name.replace(PATHSEP, PATHSEP_REPLACEMENT)


    def __init__(self, name):
        self.name = name
        self.path = Path.home().joinpath

    @property
    def installed_packages(self):
        """pip-freeze-like list of installed packages"""

    def update_name(self):
        """update the project's name to the current notebook name"""


def get_notebook_path():
    # TODO: add docstring
    """get the absolute path to the current notebook"""
    kernel_filepath = ipykernel.connect.get_connection_file()
    kernel_id = kernel_filepath.split('/kernel-')[-1].split('.json')[0]

    running_nbservers_stdout = run_shell_command('jupyter notebook list',
                                                 live_stdout=False)
    for line in running_nbservers_stdout.splitlines():
        # should only need to exclude first line ("Currently running
        # servers:"), but handle safely in case output format changes in
        # the future
        if not line.strip().startswith('http'):
            continue

        nbserver_url, nbserver_root_dir = line.split('::')
        nbserver_url = nbserver_url.strip()
        nbserver_root_dir = nbserver_root_dir.strip()

        notebook_api_url = urljoin(nbserver_url, '/api/sessions')
        parsed_url = urlparse(nbserver_url)
        if parsed_url.query:
            params = {'token': parsed_url.query.removeprefix('token=')}
        else:
            params = None

        # TODO: add exception handling, 403 handling, etc.
        response = requests.get(notebook_api_url, params=params)
        for session in response.json():
            if session['kernel']['id'] == kernel_id:
                if config.environment == 'Colaboratory':
                    # Colab notebooks don't actually live on Colab VM
                    # filesystem, so just use notebook name
                    return session['notebook']['name']
                else:
                    notebook_relpath = session['notebook']['path']
                    return Path(nbserver_root_dir, notebook_relpath)


def prune_projects():
    """delete (auto-named) projects for which a notebook doesn't exist"""


def prune_project(proj):
    """delete a single project by its name"""
