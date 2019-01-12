from datetime import datetime, timedelta

from nikola.plugin_categories import ShortcodePlugin
from lxml import etree
from lxml.html import tostring


class HomeworkTableShortcode(ShortcodePlugin):

    name = 'homework_table'

    def handler(self, site=None, data=None, lang=None, post=None):
        class_config = self.site.GLOBAL_CONTEXT['data']['class_config']

        table = etree.Element('table', attrib={'class': 'table table-striped'})
        thead = etree.SubElement(table, 'thead')
        thead_row = etree.SubElement(thead, 'tr')
        for text in ['Homework #', 'Due Date']:
            elem = etree.SubElement(thead_row, 'th')
            elem.text = text
        for text in ['Assignment', 'Solution']:
            elem = etree.SubElement(thead_row, 'th', colspan='2')
            elem.text = text
        homeworks = sorted(class_config.get('homework', []),
                           key=lambda x: datetime.strptime(x['due-date'], '%d-%b-%Y'),
                           reverse=True)

        body = etree.SubElement(table, 'tbody')
        for homework in homeworks:
            hw_num = homework['number']
            folder = f'/homework/homework-{hw_num}/homework-{hw_num}'
            row = etree.SubElement(body, 'tr')

            td = etree.SubElement(row, 'td')
            td.text = str(hw_num)

            td = etree.SubElement(row, 'td')
            due_date = datetime.strptime(homework['due-date'], '%d-%b-%Y').replace(hour=12)
            td.text = due_date.strftime("%b. %d, %Y")

            td = etree.SubElement(row, 'td')
            a = etree.SubElement(td, 'a', href=folder + '.pdf')
            a.text = 'PDF'

            td = etree.SubElement(row, 'td')
            a = etree.SubElement(td, 'a', href=folder + '.zip')
            a.text = 'ipynb'

            late_date = due_date + timedelta(days=3)
            no_solution = homework.get('no-solution', False)
            force_solution = homework.get('force-solution', False)
            if (datetime.today() < late_date or no_solution) and not force_solution:
                # Add blank cells if the solution is not to be distributed yet
                etree.SubElement(row, 'td')
                etree.SubElement(row, 'td')
            else:
                td = etree.SubElement(row, 'td')
                a = etree.SubElement(td, 'a', href=folder + '-soln.pdf')
                a.text = 'PDF'

                td = etree.SubElement(row, 'td')
                a = etree.SubElement(td, 'a', href=folder + '-soln.zip')
                a.text = 'ipynb'

        return tostring(table).decode('utf-8'), ['data/class_config.yaml']
