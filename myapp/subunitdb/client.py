from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from myapp.subunitdb.models import ListModel, RunModel, TestModel


class SubunitClient(object):
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, connection_string):
        Base = automap_base()
        engine = create_engine(connection_string)
        Base.prepare(engine, reflect=True)
        self.session = Session(engine)
        # self.alembic_version = Base.classes.alembic_version
        self.attachments = Base.classes.attachments
        self.run_metadata = Base.classes.run_metadata
        self.runs = Base.classes.runs
        self.test_metadata = Base.classes.test_metadata
        self.test_run_metadata = Base.classes.test_run_metadata
        self.test_runs = Base.classes.test_runs
        self.tests = Base.classes.tests

    def get_runs(self, run_after=None, run_before=None, limit=100, **metadata):
        main_query = self.session.query(self.runs)
        if metadata:
            for k, v in metadata.items():
                sub_query = self.session.query(self.run_metadata.run_id)
                main_query = main_query.filter(self.runs.id.in_(
                    sub_query.filter_by(key=str(k), value=str(v))))

        if run_after is not None:
            main_query = main_query.filter(self.runs.run_at > run_after)

        if run_before is not None:
            main_query = main_query.filter(self.runs.run_at < run_before)

        main_query = main_query.limit(limit)
        return ListModel.from_sqlalchemy(main_query.all(), RunModel)

    def get_run_by_id(self, id_):
        main_query = self.session.query(self.runs)
        main_query = main_query.filter(self.runs.id == id_)
        for result in main_query.all():
            model = RunModel.from_sqlalchemy(result)
            sub_query = self.session.query(self.run_metadata)
            sub_query = sub_query.filter_by(run_id=id_)
            setattr(model, "metadata", {
                obj.key: obj.value for obj in sub_query.all()})
            return model
        return None

    def get_tests(
            self, run_after=None, run_before=None, limit=100, **metadata):
        main_query = self.session.query(self.test_runs)
        if metadata:
            for k, v in metadata.items():
                sub_query = self.session.query(
                    self.test_run_metadata.test_run_id)
                main_query = main_query.filter(self.test_runs.id.in_(
                    sub_query.filter_by(key=str(k), value=str(v))))

        if run_after is not None:
            main_query = main_query.filter(
                self.test_runs.start_time > run_after)

        if run_before is not None:
            main_query = main_query.filter(
                self.test_runs.start_time < run_before)

        main_query = main_query.limit(limit)
        return ListModel.from_sqlalchemy(main_query.all(), TestModel)

    def get_test_by_id(self, id_):
        main_query = self.session.query(self.test_runs)
        main_query = main_query.filter(self.test_runs.id == id_)
        for result in main_query.all():
            model = TestModel.from_sqlalchemy(result)
            sub_query = self.session.query(self.test_run_metadata)
            sub_query = sub_query.filter_by(test_run_id=id_)
            setattr(model, "metadata", {
                obj.key: obj.value for obj in sub_query.all()})
            return model
        return None

    def get_tests_by_run_id(self, run_id):
        main_query = self.session.query(self.test_runs).filter_by(
            run_id=run_id)
        return ListModel.from_sqlalchemy(main_query.all(), TestModel)
