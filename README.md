# pytest testrail reporter plugin
Report including fixture error on Setup and Teardown

Auto create test run under test plan specified on xxx.cfg

Test run name example `2017-10-18 17:45:59 trigger by jenkins`

Failure type will be comment on result comment, here are failure types :

```
Both setup and teardown are failed
Setup failed
Both test and teardown are failed
Test failed
Teardown failed
```

# Installation
`pip install pytest-testrail-reporter`

# Usage
## Load plugin
Put the following into conftest.py

`pytest_plugins = ["testrail"]`

or

`pytest -p testrail ...`

## Mark test as report target
Example:

```
@pytest.mark.testrail("C31877")
    def test_setup_failed(f_a):
        assert True


# Report as 'Blocked' with comment you specify(reason) in mark
@pytest.mark.testrail("C31877")
@pytest.mark.skip(reason="skippppppppppp~")
    def test_skipped(f_a):
        assert True
```

## Execute command
`pytest --testrail=xxx.cfg --user=AAA`


File (xxx.cfg) content example:

```
[API]
url=https://yoyo.testrail.net
email=imaging8896@gmail.com
key=kkkk

[Test Config]
project=project 1
plan=plan1
suite=suite1
```

# Developement
## Testing plugin : 
1. Prepare testrail.cfg under project root dir
2. Set test case ids in tests/test_testrail.py
3. Run command below on project root dir:

```
sudo pip uninstall pytest-testrail-reporter
pytest tests
```
