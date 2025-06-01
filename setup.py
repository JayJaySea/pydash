from setuptools import setup, find_packages
import os

setup(
    name='PyDash',
    version='0.1.0',
    packages=[
        "pydash", 
        "pydash.widgets",
        "pydash.scripts"
    ],
    package_data={
        'pydash': [
            'fonts/*.ttf',
            'icons/*.png',
            'style/*.scss',
            'sounds/*.wav'
        ],
    },
    include_package_data=True,
    install_requires=[
        'pyside6>=6.8.0.2',
        'pillow>=11.0.0',
        'pulsectl'
        'python-vlc'
    ],
    entry_points={
        'gui_scripts': [
            'pydash = pydash.app:main',
        ],
    },
)
