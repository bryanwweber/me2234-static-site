from pathlib import Path

this_dir = Path(__file__).parent

DOIT_CONFIG = {
    'dep_file': '.build.db',
}


def task_build_site():
    """Build the site using Nikola."""
    return {
        'actions': ['nikola build'],
        'targets': [this_dir/'output'],
    }


def task_deploy_site():
    """Deploy the site using Nikola."""
    return {
        'actions': ['nikola deploy'],
        'task_dep': ['build_site'],
        'verbosity': 2,
    }
