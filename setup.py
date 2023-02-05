from setuptools import  setup, find_packages

setup(
    name = 'VCA',
    version = '0.1.0',
    packages = find_packages(),
    install_requires = [
        'click',
        'pyInquirer',
        'pywin32',
        'rich',
        'colorama'
    ],
    entry_points = '''
    [console_scripts]
    VCA=VCA:VCA
    '''
)