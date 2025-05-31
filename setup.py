from setuptools import setup, find_packages
import os

def package_files(directories):
    paths = []
    for directory in directories:
        for (path, _, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join(path, filename))
    return paths

data_files = package_files(["pydash/fonts/", "pydash/icons/", "pydash/style/"])

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
        ],
    },
    include_package_data=True,
    install_requires=[
        'pyside6>=6.8.0.2',
        'pillow>=11.0.0',
        'pulsectl'
    ],
    entry_points={
        'gui_scripts': [
            'pydash = pydash.app:main',
        ],
    },
)
