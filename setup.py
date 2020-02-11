from setuptools import setup

APP = ['app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'todo.icns',
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps', 'jira'],
    'includes': ['json', 'subproccess', 'sys', 'os', 'webbrowser', 'jira']
}

setup(
    app=APP,
    name='Jira ToDo',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps', 'jira']
)