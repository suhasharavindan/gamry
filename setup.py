import setuptools

setuptools.setup(
    name='gamry',
    version='0.0.1',
    author='Suhash Aravindan',
    author_email='saravind@caltech.edu',
    description='Package to handle Gamry electrochemistry files',
    url='https://github.com/suhasharavindan/gamry',
    packages=['gamry'],
    install_requires=[
        'numpy',
        'pandas',
        'plotly',
        'scipy'
    ]
)