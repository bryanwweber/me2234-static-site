from pathlib import Path
from datetime import datetime, timedelta

from nikola.plugin_categories import Task
from nikola import utils

import yaml

dropbox = Path.home()/'Dropbox/Classes/2018-Fall-ME-2233'


class CopyHomework(Task):

    name = 'copy_homework'

    def set_site(self, site):
        self.site = site

        with open('class_config.yaml', 'r') as conf_file:
            self.site.class_config = yaml.load(conf_file)
        return super().set_site(site)

    def gen_tasks(self):
        kw = {
            'homework': self.site.class_config['homework'],
            'output_folder': Path(self.site.config['OUTPUT_FOLDER']),
            'filters': self.site.config['FILTERS'],
        }
        yield self.group_task()

        dest = kw['output_folder']/'homework'
        filters = kw['filters']
        for homework in kw['homework']:
            hw_num = homework['number']
            src = (dropbox/f'homework-{hw_num}/output').resolve()
            real_dest = (dest/f'homework-{hw_num}').resolve()
            due_date = datetime.strptime(homework['due-date'], '%d-%b-%Y').replace(hour=12)
            late_date = due_date + timedelta(days=3)
            if datetime.today() < late_date or homework.get('no-solution', False):
                ignored = [src/f'homework-{hw_num}-soln.zip', src/f'homework-{hw_num}-soln.zip']
                ignored = set(map(str, ignored))
            else:
                ignored = set()
            for task in utils.copy_tree(str(src), str(real_dest), ignored_filenames=ignored):
                task['basename'] = self.name
                task['uptodate'] = [utils.config_changed(kw, self.name)]
                yield utils.apply_filters(task, filters)
