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
        issues = jira.search_issues(
            'assignee = currentUser() AND status="TO DO"')
        for issue in issues:
            fields = jira.issue(issue.key).fields

            issue_string = '{}: {} - {}'.format(issue.key,
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
    user = config['user']
    server = config['server']
    apikey = config['apikey']
    app = JiraTodoApp()
    app.run()
