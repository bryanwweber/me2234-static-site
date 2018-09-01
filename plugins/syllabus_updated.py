from datetime import datetime
from pathlib import Path

from nikola.plugin_categories import ShortcodePlugin

from pdfrw import PdfReader


class SyllabusUpdatedShortcode(ShortcodePlugin):

    name = 'syllabus_updated'

    def handler(self, site=None, data=None, lang=None, post=None):
        dropbox = Path(self.site.GLOBAL_CONTEXT['data']['class_config']['root']).expanduser()
        syllabus_file = dropbox/'syllabus/syllabus.pdf'
        syllabus = PdfReader(syllabus_file)
        mod_date = datetime.strptime(syllabus.Info.ModDate.replace("'", ''), '(D:%Y%m%d%H%M%S%z)')
        return mod_date.strftime('%b. %d, %Y'), ['data/class_config.yaml', str(syllabus_file)]
