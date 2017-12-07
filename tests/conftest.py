import pytest
import os
from os.path import join as path_join
from os.path import abspath, dirname

pytest_plugins = ["pytester"]
proj_root = abspath(path_join(dirname(__file__), os.pardir))


@pytest.fixture
def testdir(testdir):
    testdir.syspathinsert(proj_root)
    return testdir


@pytest.fixture
def test_cfg():
    return path_join(proj_root, "testrail.cfg")


@pytest.fixture
def test_wrong_cfg():
    return path_join(proj_root, "setup.cfg")
