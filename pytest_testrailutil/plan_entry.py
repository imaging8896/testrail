class PlanEntry(object):

    def __init__(self):
        self._content = {}

    @property
    def plan_id(self):
        return self._content.get('plan_id')

    @plan_id.setter
    def plan_id(self, value):
        if not isinstance(value, int):
            raise ValueError('input must be a integer')
        self._content['plan_id'] = value

    @property
    def suite_id(self):
        return self._content.get('suite_id')

    @suite_id.setter
    def suite_id(self, value):
        if not isinstance(value, int):
            raise ValueError('input must be a integer')
        self._content['suite_id'] = value

    @property
    def name(self):
        return self._content.get('name')

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError('input must be a string')
        self._content['name'] = value

    @property
    def description(self):
        return self._content.get('description')

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError('input must be a string')
        self._content['description'] = value

    @property
    def assignedto_id(self):
        return self._content.get('assignedto_id')

    @assignedto_id.setter
    def assignedto_id(self, value):
        if not isinstance(value, int):
            raise ValueError('input must be a integer')
        self._content['assignedto_id'] = value

    @property
    def include_all(self):
        return self._content.get('include_all')

    @include_all.setter
    def include_all(self, value):
        if not isinstance(value, bool):
            raise ValueError('input must be a boolean')
        self._content['include_all'] = value

    @property
    def cases(self):
        return self._content.get('case_ids')

    @cases.setter
    def cases(self, case_ids):
        if case_ids is None:
            raise ValueError("'case_ids' should not be None")
        if not isinstance(case_ids, list):
            raise ValueError("'case_ids' should be list")
        if not all([isinstance(x, int) for x in case_ids]):
            raise ValueError("'case_ids' should be integer list")
        self._content['case_ids'] = case_ids

    @property
    def config_ids(self):
        return self._content.get('config_ids')

    @config_ids.setter
    def config_ids(self, config_ids):
        if config_ids is None:
            self._content['config_ids'] = None
            return
        if not isinstance(config_ids, list):
            raise ValueError("'config_ids' should be a list")
        if any([not isinstance(x, int) for x in config_ids]):
            raise ValueError("'config_ids' should be all integer list")
        self._content['config_ids'] = config_ids

    @property
    def runs(self):
        return self._content.get('runs')

    @runs.setter
    def runs(self, runs):
        # [ {"include_all": True} ]
        if runs is None:
            self._content['runs'] = None
            return
        if not isinstance(runs, list):
            raise ValueError("'config_ids' should be a list")
        if any([not isinstance(x, dict) for x in runs]):
            raise ValueError("'config_ids' should be all dictionary list")
        self._content['runs'] = runs

    def raw_data(self):
        return self._content
