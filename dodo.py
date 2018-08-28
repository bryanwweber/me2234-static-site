import shutil
from pathlib import Path

DOIT_CONFIG = {
    'dep_file': '.build.db',
}

def copy_file(src, dest, **kwargs):
    if shutil.copy2(src, dest, **kwargs) == dest:
        return None
    else:
        return False

def task_copy_syllabus():
    file_dep = Path.home()/'Dropbox/Classes/2018-Fall-ME-2233/syllabus/syllabus.pdf'
    targets = Path(__file__).parent/'files/syllabus/syllabus.pdf'

    return {
        'actions': [(copy_file, [file_dep, targets])],
        'file_dep': [file_dep],
        'targets': [targets],
    }

def task_copy_assignment():
    pass
