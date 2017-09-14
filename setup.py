from setuptools import setup, find_packages

setup(
    name='testrailutil',
    version='1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    provides=['testrailutil'],
    install_requires=['setuptools', 'testrail']
)