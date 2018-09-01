from pathlib import Path
from datetime import datetime, timedelta

from nikola.plugin_categories import Task
from nikola import utils


class CopyHomework(Task):

    name = 'copy_homework'

    def gen_tasks(self):
        kw = {
            'root': Path(self.site.GLOBAL_CONTEXT['data']['class_config']['root']).expanduser(),
            'homework': self.site.GLOBAL_CONTEXT['data']['class_config']['homework'],
            'output_folder': Path(self.site.config['OUTPUT_FOLDER']),
            'filters': self.site.config['FILTERS'],
        }
        yield self.group_task()

        filters = kw['filters']
        for homework in kw['homework']:
            hw_num = homework['number']
            src = kw['root']/f'homework/homework-{hw_num}/output'
            dest_dir = kw['output_folder']/f'homework/homework-{hw_num}'
            due_date = datetime.strptime(homework['due-date'], '%d-%b-%Y').replace(hour=12)
            late_date = due_date + timedelta(days=3)
            if datetime.today() < late_date or homework.get('no-solution', False):
                ignored = set([f'homework-{hw_num}-soln.zip', f'homework-{hw_num}-soln.pdf'])
            else:
                ignored = []

            for file in src.iterdir():
                if file.name in ignored:
                    continue
                real_dest = dest_dir/file.name
                yield utils.apply_filters({
                    'basename': self.name,
                    'name': str(real_dest),
                    'file_dep': [file],
                    'targets': [real_dest],
                    'actions': [(utils.copy_file, (file, real_dest))],
                    'uptodate': [utils.config_changed(kw, self.name)],
                }, filters)
