import json


class BaseModel(object):
    def __init__(self, kwargs):
        for k, v in kwargs.items():
            if k != "self":
                setattr(self, k, v)

    def to_json(self):
        return json.dumps(self.to_dict())


class ListModel(list):
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return [i.to_dict() for i in self]

    @classmethod
    def from_sqlalchemy(cls, obj_list, model):
        ret_val = cls()
        for obj in obj_list:
            ret_val.append(model.from_sqlalchemy(obj))
        return ret_val


class RunModel(BaseModel):
    def __init__(
        self, id=None, skips=None, fails=None, passes=None, run_at=None,
            metadata=None):
        super(RunModel, self).__init__(locals())

    def to_dict(self):
        try:
            time = self.run_at.strftime(self.TIME_FORMAT)
        except:
            time = str(self.run_at)

        dic = {
            "id": self.id,
            "skips": self.skips,
            "fails": self.fails,
            "passes": self.passes,
            "run_at": time}
        if self.metadata is not None:
            dic["metadata"] = self.metadata
        return dic

    @classmethod
    def from_sqlalchemy(cls, obj):
        return cls(
            id=obj.id,
            skips=obj.skips,
            fails=obj.fails,
            passes=obj.passes,
            run_at=obj.run_at)


class TestModel(BaseModel):
    def __init__(
        self, id=None, test_id=None, run_id=None, status=None, start_time=None,
        stop_time=None, start_time_microsecond=None,
            stop_time_microsecond=None, metadata=None):
        super(TestModel, self).__init__(locals())

    def to_dict(self):
        try:
            start = self.start_time.strftime(self.TIME_FORMAT)
        except:
            start = str(self.start_time)

        try:
            stop = self.stop_time.strftime(self.TIME_FORMAT)
        except:
            stop = str(self.stop_time)

        dic = {
            "id": self.id,
            "test_id": self.test_id,
            "run_id": self.run_id,
            "status": self.status,
            "start_time": start,
            "stop_time": stop,
            "start_time_microsecond": self.start_time_microsecond,
            "stop_time_microsecond": self.stop_time_microsecond}
        if self.metadata is not None:
            dic["metadata"] = self.metadata
        return dic

    @classmethod
    def from_sqlalchemy(cls, obj):
        return cls(
            id=obj.id,
            test_id=obj.test_id,
            run_id=obj.run_id,
            status=obj.status,
            start_time=obj.start_time,
            stop_time=obj.stop_time,
            start_time_microsecond=obj.start_time_microsecond,
            stop_time_microsecond=obj.stop_time_microsecond)
