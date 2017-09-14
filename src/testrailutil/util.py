from testrail import TestRail

RESULT_PASS = 1
RESULT_BLOCKED = 2
RESULT_UNTEST = 3
RESULT_RETEST = 4
RESULT_FAIL = 5


class TestrailUtil(object):

    def __init__(self, email, key, url, project_name):
        self.testrail = TestRail(email=email, key=key, url=url)
        self.project = self.testrail.project(project_name)
        if not self.project:
            raise ValueError("Unalbe to find the project '{}'".format(project_name))
        self.testrail.set_project_id(self.project.id)
        self.plan = None
        self.run = None
        self.tests = None

    def has_plan(self, plan_name):
        plan = self.testrail.plan(plan_name)
        if plan:
            if plan.project.id == self.project.id:
                return True
        return False

    def has_run(self, run_name):
        run = self.testrail.run(run_name)
        if run:
            if run.project.id == self.project.id:
                return True
        return False

    def set_test_plan(self, plan_name):
        if not self.has_plan(plan_name):
            raise ValueError("Unable to find test plan '{}'".format(plan_name))
        self.plan = self.testrail.plan(plan_name)
        self.run = None
        self.tests = []
        for entry in self.plan.entries:
            for run in entry.runs:
                self.tests += self.testrail.tests(run)

    def set_in_plan_test_run(self, plan_name, run_name):
        if not self.has_plan(plan_name):
            raise ValueError("Unable to find test plan '{}'".format(plan_name))
        plan = self.testrail.plan(plan_name)
        for entry in plan.entries:
            for run in entry.runs:
                if run.name == run_name:
                    self.run = run
                    self.plan = None
                    self.tests = self.testrail.tests(run)
                    return
        raise ValueError("Unable to find test run '{}' in test plan '{}'".format(run_name, plan_name))

    def set_test_run(self, run_name):
        if not self.has_run(run_name):
            raise ValueError("Unable to find test run '{}'".format(run_name))
        self.run = self.testrail.run(run_name)
        self.plan = None
        self.tests = self.testrail.tests(self.run)

    def add_test_result(self, test_title, test_status, comment=""):
        if not self.plan and not self.run:
            raise ValueError("You must set test plan or test run before adding test result.")
        match_tests = filter(lambda x: x.title == test_title, self.tests)
        if len(match_tests) > 1:
            raise ValueError("Test title '{}' matches multiple tests.".format(test_title))
        elif len(match_tests) == 1:
            test = match_tests[0]
            status = self.testrail.status(test_status)
            result = self.testrail.result()
            result.test = test
            result.status = status
            result.comment = comment
            self.testrail.add(result)
            return True, None
        return False, "Unable to find test with title '{}'".format(test_title)
