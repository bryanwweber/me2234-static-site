from pathlib import Path

from nikola.plugin_categories import Task
from nikola import utils


class CopySyllabus(Task):

    name = 'copy_syllabus'

    def gen_tasks(self):
        kw = {
            'root': Path(self.site.GLOBAL_CONTEXT['data']['class_config']['root']).expanduser(),
            'output_folder': Path(self.site.config['OUTPUT_FOLDER']),
            'filters': self.site.config['FILTERS'],
        }

        filters = kw['filters']
        file = kw['root']/'syllabus/syllabus.pdf'
        real_dest = kw['output_folder']/'syllabus/syllabus.pdf'
        return utils.apply_filters({
            'basename': self.name,
            'name': str(real_dest),
            'file_dep': [file],
            'targets': [real_dest],
            'actions': [(utils.copy_file, (file, real_dest))],
            'uptodate': [utils.config_changed(kw, self.name)],
        }, filters)
