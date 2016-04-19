import falcon


class Tests(object):
    route = "/tests"

    def __init__(self, client):
        self.client = client

    def on_get(self, req, resp):
        resp.data = self.client.get_tests(**req.params).to_json()
        resp.content_type = 'application/json'
        resp.status = falcon.HTTP_200


class Test(object):
    route = "/test/{id}"

    def __init__(self, client):
        self.client = client

    def on_get(self, req, resp, id):
        test = self.client.get_test_by_id(id)
        resp.content_type = 'application/json'
        if test is not None:
            resp.status = falcon.HTTP_200
            resp.data = test.to_json()
        else:
            raise falcon.HTTPNotFound(
                description="The requested resource does not exist",
                code=falcon.HTTP_404)
