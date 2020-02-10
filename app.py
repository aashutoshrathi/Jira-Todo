import json
import os
import subprocess
import sys
import webbrowser

import rumps
from jira import JIRA

config = json.load(open(os.path.expanduser("~") + '/todo-app.json'))


class JiraTodoApp(object):
    def __init__(self):
        self.config = {
            "app_name": "My Todos",
        }
        self.app = rumps.App(self.config["app_name"])
        self.set_up_menu()
        self.refresh = rumps.MenuItem(title="Refresh", callback=self.get_issues)
        self.app.menu = [self.refresh]

    def set_up_menu(self):
        self.app.title = "💻"
        self.get_issues()

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

            issue_string = '{}:{} - {}'.format(issue.key,
                                               fields.summary, fields.reporter)
            button = rumps.MenuItem(
                title=issue_string, callback=self.open_url)
            self.app.menu.update(button)

    def run(self):
        self.app.run()


if __name__ == '__main__':
    user = config['user']
    server = config['server']
    apikey = config['apikey']
    app = JiraTodoApp()
    app.run()
