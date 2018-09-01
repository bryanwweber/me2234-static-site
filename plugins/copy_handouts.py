from pathlib import Path

from nikola.plugin_categories import Task
from nikola import utils


class CopyHandouts(Task):

    name = 'copy_handouts'

    def gen_tasks(self):
        kw = {
            'root': Path(self.site.GLOBAL_CONTEXT['data']['class_config']['root']).expanduser(),
            'quizzes': self.site.GLOBAL_CONTEXT['data']['class_config']['quizzes'],
            'output_folder': Path(self.site.config['OUTPUT_FOLDER']),
            'filters': self.site.config['FILTERS'],
        }
        yield self.group_task()

        handouts = [q['due-date'] for q in kw['quizzes'] if q.get('handout', False)]
        dest = kw['output_folder']/'slides'
        filters = kw['filters']
        for handout in handouts:
            handout_file = kw['root']/f'topic-slides/{handout}.zip'
            real_dest = dest/handout_file.name
            yield utils.apply_filters({
                'basename': self.name,
                'name': str(real_dest),
                'file_dep': [handout_file],
                'targets': [real_dest],
                'actions': [(utils.copy_file, (handout_file, real_dest))],
                'uptodate': [utils.config_changed(kw, self.name)],
            }, filters)
