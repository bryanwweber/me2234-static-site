from datetime import datetime

from nikola.plugin_categories import ShortcodePlugin
from lxml import etree
from lxml.html import tostring


class QuizTableShortcode(ShortcodePlugin):

    name = 'quiz_table'

    def handler(self, site=None, data=None, lang=None, post=None):
        class_config = self.site.GLOBAL_CONTEXT['data']['class_config']

        table = etree.Element('table', attrib={'class': 'table table-striped'})
        thead = etree.SubElement(table, 'thead')
        thead_row = etree.SubElement(thead, 'tr')
        for text in ['Due Date', 'Quiz', 'Playlist', 'Slides']:
            elem = etree.SubElement(thead_row, 'th')
            elem.text = text
        quizzes = sorted(class_config['quizzes'],
                         key=lambda x: datetime.strptime(x['due-date'], '%d-%b-%Y'),
                         reverse=True)

        body = etree.SubElement(table, 'tbody')
        for quiz in quizzes:
            row = etree.SubElement(body, 'tr')

            td = etree.SubElement(row, 'td')
            td.text = datetime.strptime(quiz['due-date'], '%d-%b-%Y').strftime("%b. %d, %Y")

            td = etree.SubElement(row, 'td')
            a = etree.SubElement(td, 'a', href=quiz['quiz'])
            a.text = quiz.get('name', False) or 'Link'

            td = etree.SubElement(row, 'td')
            if quiz.get('playlist') is not None:
                a = etree.SubElement(td, 'a', href=quiz['playlist'])
                a.text = 'Link'
            else:
                td.text = 'N/A'

            td = etree.SubElement(row, 'td')
            if quiz.get('handout') is not None:
                a = etree.SubElement(td, 'a', href=f'/slides/{quiz["due-date"]}.zip')
                a.text = 'Link'
            else:
                td.text = 'N/A'

        return tostring(table).decode('utf-8'), ['data/class_config.yaml']
