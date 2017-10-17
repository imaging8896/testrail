from setuptools import setup, find_packages

setup(
    name='pytest-testrail',
    version='1.1',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'pytest11': [
            'testrailutil = pytest_testrailutil.plugin',
        ]
    },
    install_requires=['setuptools', 'testrail', 'configparser==3.5.0'],
    classifiers=[
        "Framework :: Pytest",
    ]
)