import pytest
import configparser
import datetime
from client import Client


def pytest_addoption(parser):
    group = parser.getgroup('testrail')
    group.addoption(
        '--testrail',
        action='store',
        help='Create and update testruns with TestRail'
    )
    group.addoption(
        '--user',
        action='store',
        default="local",
        help="Who trigger the test. Default is 'local'."
    )


testrail_client = None
testrail_run = None


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    global testrail_client, testrail_run

    case_id = get_testrail_case_id(item)
    outcome = yield
    rep = outcome.get_result()
    if testrail_client and testrail_run:
        if case_id:
            if rep.when == "setup":
                if rep.outcome == "skipped":
                    testrail_client.add_test_result(testrail_run, case_id, "blocked", str(call.excinfo.value))
                elif rep.outcome == "passed":
                    pass
                elif rep.outcome == "failed":
                    testrail_client.add_test_result(testrail_run, case_id, "failed", "Setup failed")
                else:
                    testrail_client.add_test_result(testrail_run, case_id, "failed", "Unknown outcome '{}'".format(rep.outcome))
            elif rep.when == "call":
                if rep.outcome == "passed":
                    testrail_client.add_test_result(testrail_run, case_id, "passed", "Test passed by automation")
                elif rep.outcome == "failed":
                    testrail_client.add_test_result(testrail_run, case_id, "failed", "Test failed")
                else:
                    testrail_client.add_test_result(testrail_run, case_id, "failed", "Unknown outcome '{}'".format(rep.outcome))
            elif rep.when == "teardown":
                if rep.outcome == "passed":
                    pass
                elif rep.outcome == "failed":
                    testrail_client.add_test_result(testrail_run, case_id, "failed", "Teardown failed")
                else:
                    testrail_client.add_test_result(testrail_run, case_id, "failed", "Unknown outcome '{}'".format(rep.outcome))
            else:
                testrail_client.add_test_result(testrail_run, case_id, "failed", "Unknown test stage '{}'".format(rep.when))


@pytest.fixture(scope="session", autouse=True)
def testrail_client_init(request):
    global testrail_client, testrail_run
    conf_file = request.config.getoption("--testrail", default=None, skip=True)
    if conf_file:
        cfg_file = read_config_file(conf_file)

        url = cfg_file.get('API', 'url')
        email = cfg_file.get('API', 'email')
        key = cfg_file.get('API', 'key')

        project_name = cfg_file.get('Test Config', 'project')
        plan_name = cfg_file.get('Test Config', 'plan')
        suite_name = cfg_file.get('Test Config', 'suite')
        user = request.config.getoption("--user", default="local", skip=True)

        description = "Test config : URL = '{}'\nemail = '{}'\nkey = '{}'\nproject = '{}'\nplan = '{}'\nsuite = '{}'\nuser = '{}'".format(
            url, email, key, project_name, plan_name, suite_name, user)
        print("\n[Testrail] " + description)
        client = Client(email, key, url, project_name)
        cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry_name = "{} trigger by {}".format(cur_time, user)
        run = client.add_plan_entry(plan_name, entry_name, suite_name, description)
        testrail_client = client
        testrail_run = run


def get_testrail_case_id(node):
    testrail_marker = node.get_marker("testrail")
    if not testrail_marker:
        return None
    if len(testrail_marker.args) == 0:
        raise ValueError("[Marker Error] tag 'testrail' should contain only one argument 'case id'")
    return int(testrail_marker.args[0][1:])


def read_config_file(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
    return config
