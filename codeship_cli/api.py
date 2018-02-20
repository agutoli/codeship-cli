import json
import requests
from requests.auth import HTTPBasicAuth

class CodeShipAPI(object):

    def __init__(self, username=None, password=None, organization_name=None):
        self.api_url = 'https://api.codeship.com/v2'
        self.username = username
        self.password = password
        self.organization_name = organization_name

        self.auth = self.auth()


    def get_project(self, project_uuid):
        try:
            return self.GET("/organizations/%s/projects/%s" % (self.organization_uuid, project_uuid))
        except Exception as e:
            return None

    def list_projects(self, page=1):
        try:
            return self.GET("/organizations/%s/projects?page=%s" % (self.organization_uuid, page))
        except Exception as e:
            return None

    def create_project(self,
        plan_type="basic",
        team_ids=None,
        test_pipelines=None,
        repository_url=None,
        setup_commands=None,
        environment_variables=None):
        try:
            body = {
                "type": plan_type,
                "team_ids": team_ids,
                "test_pipelines": test_pipelines,
                "repository_url": repository_url,
                "setup_commands": setup_commands,
                "environment_variables": environment_variables
            }
            return self.POST("/organizations/%s/projects" % self.organization_uuid, body=body)
        except Exception as e:
            return None

    def auth(self):
        headers = {"content-type": "application/json"}
        auth = HTTPBasicAuth(self.username, self.password)
        res = json.loads(requests.post("https://api.codeship.com/v2/auth", auth=auth, headers=headers).content)
        if ('errors' in res) and 'Unauthorized' in res['errors']:
            raise Exception("Unauthorized!")
        if 'error' in res:
            raise Exception(res['error'])
        return res

    def res(self, http_response):
        return json.loads(http_response.content)

    def POST(self, endpoint, body=None):
        return self.res(requests.post("%s%s" % (self.api_url, endpoint), json=body, headers=self.headers))

    def GET(self, endpoint):
        return self.res(requests.get("%s%s" % (self.api_url, endpoint), headers=self.headers))

    @property
    def organization_uuid(self):
        uuid = None
        for org in self.auth['organizations']:
            if org['name'] == self.organization_name:
                uuid = org['uuid']
                break
        if not uuid:
            raise Exception("Can not find project with name %s" % self.organization_name)
        return uuid

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": self.auth['access_token']
        }
