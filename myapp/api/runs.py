import falcon


class Runs(object):
    route = "/runs"

    def __init__(self, client):
        self.client = client

    def on_get(self, req, resp):
        resp.data = self.client.get_runs(**req.params).to_json()
        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_200


class Run(object):
    route = "/run/{id}"

    def __init__(self, client):
        self.client = client

    def on_get(self, req, resp, id):
        run = self.client.get_run_by_id(id)
        resp.content_type = 'application/json'
        if run is not None:
            resp.status = falcon.HTTP_200
            resp.data = run.to_json()
        else:
            raise falcon.HTTPNotFound(
                description="The requested resource does not exist",
                code=falcon.HTTP_404)
