import json
import os
import subprocess
import sys
import webbrowser

import rumps
from jira import JIRA

config = json.load(open(os.path.expanduser("~") + '/todo-app.json'))
BOOTSTRAP = 'bootstrap'


class JiraTodoApp(object):
    def __init__(self):
        self.config = {
            "app_name": "My Todos",
        }
        self.app = rumps.App(self.config["app_name"])
        self.app.quit_button = None
        self.app.title = "💻"
        self.quit_button = rumps.MenuItem(title="Quit 👋🏻")
        self.refresh_button = rumps.MenuItem(
            title="Refresh ⚡️", callback=self.get_data)
        self.get_data(BOOTSTRAP)

    def get_data(self, callback):
        if callback is not BOOTSTRAP:
            rumps.notification("Just give me a second to get Issues from Jira",
                               "Fetching your amazing ToDos", "Thanks for being patient")
        self.prepare_list()

    def prepare_list(self):
        self.app.menu.clear()
        self.app.menu.update(self.refresh_button)
        self.get_issues()
        self.app.menu.update(self.quit_button)

    def open_url(self, item):
        id = item.title.split(':')[0]
        url = '{}/browse/{}'.format(server, id)
        if sys.platform == 'darwin':
            subprocess.Popen(['open', url])
        else:
            webbrowser.open_new_tab(url)

    def get_issues(self):
        options = {
            'server': server
        }

        jira = JIRA(options, basic_auth=(user, apikey))
        issue_status = status if status else 'TO DO' 
        role =  custom_role if custom_role else 'assignee'

        query = '{} = currentUser() AND status="{}"'.format(role, issue_status)
        
        issues = jira.search_issues(query)

        for issue in issues:
            fields = jira.issue(issue.key).fields
            issue_string = '{}: {} - {}'.format(issue.key,
                                                fields.summary, fields.reporter)
            if show_fix_versions:
                versions = '-'
                if len(fields.fixVersions) > 0:
                    versions = ":".join(
                        [version.name for version in fields.fixVersions])
                issue_string = '{} | {} | {} - {}'.format(issue.key, versions,
                                                          fields.summary, fields.reporter)
            button = rumps.MenuItem(
                title=issue_string, callback=self.open_url)
            self.app.menu.update(button)

    @rumps.clicked('Quit 👋🏻')
    def quit(_):
        rumps.quit_application()

    def run(self):
        self.app.run()


if __name__ == '__main__':
    user = config.get('user')
    server = config.get('server')
    apikey = config.get('apikey')
    show_fix_versions = config.get('showFixVersions')
    custom_role = config.get('customRole')
    status = config.get('status')

    app = JiraTodoApp()
    app.run()
