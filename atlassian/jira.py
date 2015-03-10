import logging
from atlassian import AtlassianRestAPI


logging.basicConfig(level=logging.INFO, format="[%(asctime).19s] [%(levelname)s] %(message)s")
logging.getLogger("requests").setLevel(logging.WARNING)
log = logging.getLogger("atlassian.jira")


class Jira(AtlassianRestAPI):

    def reindex_status(self):
        return self.get("/rest/api/2/reindex")

    def reindex(self):
        return self.post("/rest/api/2/reindex")

    def jql(self, jql):
        return self.get("/rest/api/2/search?jql={0}&maxResults=999999".format(jql))

    def projects(self):
        return self.get("/rest/api/2/project")

    def user(self, username):
        return self.get("/rest/api/2/user?username=%s" % username)

    def project(self, key):
        return self.get("/rest/api/2/project/{0}".format(key))

    def issue(self, key):
        return self.get("/rest/api/2/issue/{0}".format(key))

    def update_issue_field(self, key, fields):
        return self.put("/rest/api/2/issue/{0}".format(key), data={"fields": fields})

    def project_leaders(self):
        for project in self.projects():
            key = project["key"]
            project_data = self.project(key)
            lead = self.user(project_data["lead"]["key"])
            yield {
                "project_key": key,
                "project_name": project["name"],
                "lead_name": lead["displayName"],
                "lead_key": lead["key"],
                "lead_email": lead["emailAddress"]}

    def rename_sprint(self, sprint_id, name, start_date, end_date):
        return self.put("/rest/greenhopper/1.0/sprint/{0}".format(sprint_id), data={
            "name": name,
            "startDate": start_date,
            "endDate": end_date})