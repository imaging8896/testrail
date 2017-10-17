from testrail import TestRail
from testrail.run import Run

from plan_entry import PlanEntry


class Client(TestRail):

    def __init__(self, email, key, url, project_name):
        super(Client, self).__init__(email=email, key=key, url=url)
        project = self.project(project_name)
        if not project:
            raise ValueError("Unalbe to find the project '{}'".format(project_name))
        self.project_id = project.id
        self.set_project_id(project.id)

    def add_plan_entry(self, plan_name, entry_name, suite_name, description, case_ids=None):
        suite = self.suite(suite_name)

        obj = PlanEntry()
        obj.plan_id = self.plan(plan_name).id
        obj.suite_id = suite.id
        obj.name = entry_name
        obj.description = description

        if case_ids:
            obj.cases = case_ids

        obj.include_all = True
        entries = self.api.add_plan_entry(obj.raw_data())
        return Run(entries["runs"][0])

    def add_test_result(self, run, test_criteria, test_status, comment=""):
        test = self._find_test(run, test_criteria)
        if test:
            self._add_my_result(test, test_status, comment)
            return True, ""
        else:
            return False, "Unable to find test with id '{}'".format(test_criteria)

    def _find_test(self, run, test_criteria):
        if isinstance(test_criteria, int):
            # match_tests = filter(lambda x: x.case.id == test_id, self.tests)  # There is BUG !!!
            match_tests = filter(lambda x: x._content.get("case_id") == test_criteria, self.tests(run))
        elif isinstance(test_criteria, str):
            match_tests = filter(lambda x: x.title == test_criteria, self.tests(run))
        else:
            raise ValueError("'test' should be either test title or case id")
        if len(match_tests) > 1:
            raise ValueError("Test criteria '{}' matches multiple tests.".format(test_criteria))
        elif len(match_tests) == 0:
            return None
        return match_tests[0]

    def _add_my_result(self, test, test_status, comment):
        status = self.status(test_status)
        result = self.result()
        result.test = test
        result.status = status
        result.comment = comment
        self.add(result)
