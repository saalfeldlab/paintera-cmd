from distutils.core import setup
from distutils.command.build_py import build_py

import os

install_requires=[
    'jgo>=0.4.0',
    'paintera-conversion-helper>=0.7.0'
]
entry_points={
    'console_scripts': [
        'paintera=paintera:launch_paintera',
        'paintera-show-container=paintera:launch_paintera_show_container'
    ]
}

name = 'paintera'
here = os.path.abspath(os.path.dirname(__file__))
version_info = {}
with open(os.path.join(here, name, 'version.py')) as fp:
    exec(fp.read(), version_info)
version = version_info['_paintera_version']

# https://stackoverflow.com/a/14159430/1725687
# need to add package_data... WHY???
completion_segments = ['share', 'bash-completion', 'completions', 'paintera']
data_files = [(os.path.join(*completion_segments[:-1]), [os.path.join(*completion_segments)])]

setup(
    name=name,
    version=version.python_version(),
    author='Philipp Hanslovsky',
    author_email='hanslovskyp@janelia.hhmi.org',
    description='paintera',
    url='https://github.com/saalfeldlab/paintera',
    packages=['paintera'],
    entry_points=entry_points,
    install_requires=install_requires,
    data_files=data_files
)
