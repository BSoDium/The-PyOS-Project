from setuptools import setup

setup(
    name="PyOS",
    version='0.10a',
    options = {
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.ptf',
                '**/*.mp3'
            ],
            'gui_apps': {
                'PyOS': 'main.py',
            },
            'log_filename': '$USER_APPDATA/.PyOS/output.log',
            'log_append': False,
            'plugins': [
                'pandagl',
                'p3openal_audio',
                'p3ffmpeg',
                'p3ptloader',
            ],
        }
    },
    packages=['pypresence']
)