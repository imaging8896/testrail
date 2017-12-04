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


# @pytest.fixture(scope="session", autouse=True)
# def before_after_all(request):
#     print("[Hook] Before all.")
#     yield
#     print("[Hook] After all.")
#
#
# @pytest.fixture(scope="function", autouse=True)
# def before_after_function(request):
#     print("\n[Hook] Before function")
#     print("[Log]")
#     yield
#     print("[Hook] After function.")


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    test_name = item.name.split("[")[0]

    case_id = get_testrail_case_id(item)
    outcome = yield
    rep = outcome.get_result()
    if case_id:
        testrail_results = item.funcargs["testrail_results"]
        testrail_results_add(testrail_results, case_id, test_name, rep.when, rep.passed)


@pytest.fixture(scope="session", autouse=True)
def testrail_client(request):
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
        return {"client": client, "run": run}
    else:
        return None


@pytest.fixture(scope="session", autouse=True)
def testrail_results(request, testrail_client):
    print("[Testrail] All results prepare")
    results = {}
    yield results
    print("[Testrail] All results '{}'".format(results))
    if testrail_client:
        client = testrail_client["client"]
        run = testrail_client["run"]
        for case_id, result in results.iteritems():
            print("[Testrail] Report test '{}' with case id {}".format(result["name"], case_id))
            if not result["setup"]:
                if not result["teardown"]:
                    client.add_test_result(run, case_id, "failed", "Both setup and teardown are failed")
                else:
                    client.add_test_result(run, case_id, "failed", "Setup failed")
            else:
                if not result["call"]:
                    if not result["teardown"]:
                        client.add_test_result(run, case_id, "failed", "Both test and teardown are failed")
                    else:
                        client.add_test_result(run, case_id, "failed", "Test failed")
                else:
                    if "teardown" in result and not result["teardown"]:
                        client.add_test_result(run, case_id, "failed", "Teardown failed")
                    else:
                        client.add_test_result(run, case_id, "passed", "Auto report")


def testrail_results_add(testrail_results, case_id, test_name, when, result):
    if case_id not in testrail_results:
        testrail_results[case_id] = {
            "name": test_name,
            when: result
        }
    else:
        if when not in testrail_results[case_id]:
            testrail_results[case_id][when] = result
        else:
            testrail_results[case_id][when] = (testrail_results[case_id][when] and result)


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
