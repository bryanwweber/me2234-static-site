import shutil
from pathlib import Path
import yaml

with open('class_config.yaml', 'r') as config_file:
    config = yaml.load(config_file)
dropbox = Path.home()/'Dropbox/Classes/2018-Fall-ME-2233'
this_dir = Path(__file__).parent

DOIT_CONFIG = {
    'dep_file': '.build.db',
}


def copy_file(src, dest, **kwargs):
    """Munge the output of shutil.copy2 to match doit requirement.

    Returns `None` on success, or `False` on failure, to match the behavior
    expected by doit.
    """
    if shutil.copy2(src, dest, **kwargs) == dest:
        return None
    else:
        return False


def task_copy_syllabus():
    """Copy the syllabus from the Dropbox folder to the local files."""
    file_dep = dropbox/'syllabus/syllabus.pdf'
    targets = this_dir/'files/syllabus/syllabus.pdf'

    return {
        'actions': [(copy_file, [file_dep, targets])],
        'file_dep': [file_dep],
        'targets': [targets],
    }


def task_copy_assignments():
    """Copy a homework assignment from Dropbox to the local folder."""
    for assignment in config['assignments']:
        for ext in ['.pdf', '.zip']:
            hw_file = f'homework-{assignment}{ext}'
            file_dep = dropbox/f'homework/homework-{assignment}/output'/hw_file
            target = this_dir/f'files/homework/homework-{assignment}'/hw_file
            yield {
                'name': hw_file,
                'file_dep': [file_dep],
                'targets': [target],
                'actions': [(copy_file, [file_dep, target])],
            }


def task_copy_solutions():
    """Copy a homework solution from Dropbox to the local folder."""
    if config.get('solutions') is None:
        return None
    for solution in config['solutions']:
        for ext in ['.pdf', '.zip']:
            hw_file = f'homework-{solution}-soln{ext}'
            file_dep = dropbox/f'homework/homework-{solution}/output'/hw_file
            target = this_dir/f'files/homework/homework-{solution}'/hw_file
            yield {
                'name': hw_file,
                'file_dep': [file_dep],
                'targets': [target],
                'actions': [(copy_file, [file_dep, target])],
            }


def task_copy_handouts():
    """Copy a zip file of handout slides from Dropbox to the local folder."""
    for handout in config['handouts']:
        handout_file = dropbox/f'topic-slides/{handout}.zip'
        handout_target = this_dir/f'files/slides/{handout}.zip'
        yield {
            'name': handout_file.name,
            'file_dep': [handout_file],
            'targets': [handout_target],
            'actions': [(copy_file, [handout_file, handout_target])],
        }


def task_build_site():
    """Build the site using Nikola."""
    return {
        'actions': ['nikola build'],
        'targets': [this_dir/'output'],
        'task_dep': ['copy_syllabus', 'copy_solutions', 'copy_assignments', 'copy_handouts'],
    }


def task_deploy_site():
    """Deploy the site using Nikola."""
    return {
        'actions': ['nikola deploy'],
        'task_dep': ['build_site'],
        'verbosity': 2,
    }
