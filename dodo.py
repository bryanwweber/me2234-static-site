import pysftp
from pathlib import Path
from getpass import getpass

this_dir = Path(__file__).parent

DOIT_CONFIG = {
    'dep_file': '.build.db',
}

def deploy_site():
    password = getpass()
    with pysftp.Connection('weberb.engr.uconn.edu', username="bww09001", password=password) as sftp:
        sftp.put_r(str(this_dir / "output"), 'edu.uconn.engr.weberb/public_html/me2234')


def task_git_pull():
    """Pull changes from upstream before building."""
    return {
        'actions': ['git pull'],
    }


def task_build_site():
    """Build the site using Nikola."""
    return {
        'actions': ['nikola build'],
        'targets': [this_dir/'output'],
        'task_dep': ['git_pull'],
    }


def task_deploy_site():
    """Deploy the site using Nikola."""
    return {
        'actions': [deploy_site],
        'task_dep': ['build_site'],
        'verbosity': 2,
    }
