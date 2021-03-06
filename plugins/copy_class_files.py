from pathlib import Path
from datetime import datetime, timedelta

from nikola.plugin_categories import Task
from nikola import utils
import pypandoc as ppd


class CopyClassFiles(Task):

    name = 'copy_class_files'

    def gen_tasks(self):
        kw = {
            'root': Path(self.site.GLOBAL_CONTEXT['data']['class_config']['root']).expanduser(),
            'homework': self.site.GLOBAL_CONTEXT['data']['class_config'].get('homework', []),
            'quizzes': self.site.GLOBAL_CONTEXT['data']['class_config']['quizzes'],
            'course-material': self.site.GLOBAL_CONTEXT['data']['class_config']['course-materials'],
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
                'clean': True,
            }, filters)

        syllabus_file = kw['root']/'syllabus/syllabus.pdf'
        real_dest = kw['output_folder']/'syllabus/syllabus.pdf'
        yield utils.apply_filters({
            'basename': self.name,
            'name': str(real_dest),
            'file_dep': [syllabus_file],
            'targets': [real_dest],
            'actions': [(utils.copy_file, (syllabus_file, real_dest))],
            'uptodate': [utils.config_changed(kw, self.name)],
            'clean': True,
        }, filters)

        for homework in kw['homework']:
            hw_num = homework['number']
            src = kw['root']/f'homework/homework-{hw_num}/output'
            dest_dir = kw['output_folder']/f'homework/homework-{hw_num}'
            due_date = datetime.strptime(homework['due-date'], '%d-%b-%Y').replace(hour=12)
            late_date = due_date + timedelta(days=3)
            no_solution = homework.get('no-solution', False)
            force_solution = homework.get('force-solution', False)
            if (datetime.today() < late_date or no_solution) and not force_solution:
                ignored = set([f'homework-{hw_num}-soln.zip', f'homework-{hw_num}-soln.pdf'])
            else:
                ignored = []

            for hw_file in src.iterdir():
                if hw_file.name in ignored or hw_file.name == '.DS_Store':
                    continue
                real_dest = dest_dir/hw_file.name
                yield utils.apply_filters({
                    'basename': self.name,
                    'name': str(real_dest),
                    'file_dep': [hw_file],
                    'targets': [real_dest],
                    'actions': [(utils.copy_file, (hw_file, real_dest))],
                    'uptodate': [utils.config_changed(kw, self.name)],
                    'clean': True,
                }, filters)

        for quiz in kw["quizzes"]:
            src = kw["root"]/"quizzes"/"online"
            due_date = datetime.strptime(quiz['due-date'], '%d-%b-%Y').replace(hour=12)
            file_stem = src.joinpath(due_date.strftime("%b. %-d, %Y"))
            file_name = file_stem.with_suffix(file_stem.suffix + " Lectures.md")
            if quiz.get("no_solution", False) or not file_name.exists():
                continue
            output_file = file_stem.with_suffix(file_stem.suffix + " Lectures.pdf")
            if not output_file.exists():
                yield {
                    "basename": self.name,
                    "name": file_name.name,
                    "file_dep": [file_name],
                    "targets": [output_file],
                    "actions": [(ppd.convert_file, (str(file_name), "latex"), {"format": "markdown", "outputfile": str(output_file), "extra_args": ["-V", "geometry:margin=1in"]})],
                    "uptodate": [utils.config_changed(kw, self.name)],
                    "clean": True,
                }
            real_dest = kw["output_folder"]/"quiz-solutions"/output_file.name
            if datetime.today() > due_date:
                yield utils.apply_filters({
                    "basename": self.name,
                    "name": real_dest.name,
                    "file_dep": [output_file],
                    "targets": [real_dest],
                    "actions": [(utils.copy_file, (output_file, real_dest))],
                    "uptodate": [utils.config_changed(kw, self.name)],
                    "clean": True,
                }, filters)

        for item in kw['course-material']:
            src = kw['root']/item['source']
            dest = kw['output_folder']/'course-materials'/item.get('dest', item['source'])
            yield utils.apply_filters({
                'basename': self.name,
                'name': str(dest),
                'file_dep': [src],
                'targets': [dest],
                'actions': [(utils.copy_file, (src, dest))],
                'uptodate': [utils.config_changed(kw, self.name)],
                'clean': True,
            }, filters)
