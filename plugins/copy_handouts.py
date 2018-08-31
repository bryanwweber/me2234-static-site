from pathlib import Path

from nikola.plugin_categories import Task
from nikola import utils

import yaml

dropbox = Path.home()/'Dropbox/Classes/2018-Fall-ME-2233'


class CopyHandouts(Task):

    name = 'copy_handouts'

    def set_site(self, site):
        self.site = site

        with open('class_config.yaml', 'r') as conf_file:
            self.site.class_config = yaml.load(conf_file)
        return super().set_site(site)

    def gen_tasks(self):
        kw = {
            'quizzes': self.site.class_config['quizzes'],
            'output_folder': Path(self.site.config['OUTPUT_FOLDER']),
            'filters': self.site.config['FILTERS'],
        }
        yield self.group_task()

        handouts = [q['due-date'] for q in kw['quizzes'] if q.get('handout', False)]
        dest = kw['output_folder']/'slides'
        filters = kw['filters']
        for handout in handouts:
            handout_file = dropbox/f'topic-slides/{handout}.zip'
            for task in utils.copy_tree(str(handout_file.resolve()), str(dest.resolve())):
                task['basename'] = self.name
                task['uptodate'] = [utils.config_changed(kw, self.name)]
                yield utils.apply_filters(task, filters)
