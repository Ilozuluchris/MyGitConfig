import os 

from setuptools import setup

setup (
        name='mygitconfig',
        version='0.1',
        py_modules=['mygitconfig'],
        description = 'Reduce the number of lines required to config your git repos with their right credentials',
        author = "Ilozulu Chris",
        author_email = 'ilozuluchidiuso@gmail.com',
        url = "",
        license = "MIT License",
        platform = "",
        install_requires=[
            'Click'
        ],
        entry_points='''
		[console_scripts]
		mygitconfig=mygitconfig:cli
		''',
)

#so script can be called anywhere 
os.system('chmod a+x mygitconfig.py')
os.system('export PATH=mygitconfig.py:$PATH')