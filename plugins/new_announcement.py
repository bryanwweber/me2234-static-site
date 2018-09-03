from nikola.plugins.command.new_post import CommandNewPost


class CommandNewAnnouncement(CommandNewPost):

    name = 'new_announcement'

    def _execute(self, options, args):
        if options['tags']:
            options['tags'] += ',announcements'
        else:
            options['tags'] = 'announcements'
        options['content_format'] = 'markdown'

        return super()._execute(options, args)
