from setuptools import setup


setup(
    name             = 'DUNE_py',
    version          = '1.0.0',    
    description      = 'Work describing the tau neutrino in DUNE and the inclusion of NSI',
    url              = 'https://github.com/EdsonSSouza',
    author           = 'Edson Souza',
    author_email     = 'e235632@dac.unicamp.br',
    packages         = ['Init_00_tau', 'SM_01_Prob', 'NSI_01_Prob'],
    install_requires = [
                       'numpy',
                       'scipy',
                       'pandas',
                       'matplotlib'
                       ],

    classifiers=[
        'Intended Audience :: Science/Research', 
        'Operating System :: POSIX :: Linux',      
        'Programming Language :: Python :: 3.8',
    ],
)

