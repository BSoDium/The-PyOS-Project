from setuptools import setup

setup(
    name="PyOS",
    options = {
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
            ],
            'gui_apps': {
                'PyOS': 'main.py',
            },
            'log_filename': '$USER_APPDATA/.PyOS/output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)