from setuptools import setup

setup(
    name="PyOS",
    version='0.11',
    options = {
        'build_apps': {
            'include_modules': [
                'pypresence'
            ],
            'platforms': ['win_amd64'
            ],
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
    }
)