"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['pyExamScan_v2.py']
DATA_FILES = []
OPTIONS = {'excludes': "jupyter, jupyterlab, jupyter_console, statsmodels, ipython"}#{'argv_emulation': True}#,
        #'excludes': "PyQt5, scipy, jupyter, jupyterlab,numpy,pandas,jupyter_console,matplotlib,statsmodels,ipython"}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
