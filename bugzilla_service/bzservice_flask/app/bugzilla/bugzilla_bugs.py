import requests, json
from datetime import datetime
import numpy as np

class BugzillaBug:

    def __init__(self, bugzilla_data):
        self.bugzilla_data = bugzilla_data

    """ Method to get a specific bug. The requested bug is only provided if:
            - requester has admin role, we wil reply with all the tickets
            - requester is not admin but is requesting 5G-EVE_PORTAL tickets (which are public)
            @params:
                - requester: email address of the user who is requesting data
                - bug_id: bug identifier
            @return:
                - HTTP code: 200, 401 UNAUTHORIZED
                - message: it will include a bug or details about the error
    """
    def get_bugs_by_id(self, requester, requester_token, bug_id, is_admin):
        if is_admin:
            url = self.bugzilla_data['bugs_uri'] + '/' + bug_id + "?api_key=" + self.bugzilla_data['admin_key']
        else:
            url = self.bugzilla_data['bugs_uri'] + '/' + bug_id + "?token=" + requester_token
        response = requests.get(url)

        if response.status_code == requests.codes.ok:
            data = response.json()
            if is_admin:
                return response.status_code, data
            if len(data['bugs']) > 0:
                
                if data['bugs'][0]['product'] == "5G-EVE_PORTAL":
                    return response.status_code, data
                else:
                    return requests.codes.unauthorized, json.loads('{"details": "User unauthorized for retrieving ticket"}')
            else:
                return requests.status_codes, json.loads(json.dumps([]))

        return response.status_code, response.json()

    """ Method to collect bugs from bugzilla (all for admin and 5G-EVE_PORTAL related for regular users)
            @params:
                - requester: email address of the user requesting bugs
            @return:
                - HTTP code
                - message: it will include a bug list or details about the error
    """
    def get_bugs_by_creator(self, requester, requester_token, is_admin, page):
        if page == None:
            page = 1

        if is_admin:
            url = self.bugzilla_data['bugs_uri'] + "?api_key=" + self.bugzilla_data['admin_key'] + "&status=CONFIRMED"
        else:    
            #url = self.bugzilla_data['bugs_uri'] + "?reporter=" + requester + "&token=" + requester_token + "&status=CONFIRMED"
            url = self.bugzilla_data['bugs_uri'] + "?api_key=" + self.bugzilla_data['admin_key'] + "&status=CONFIRMED&product=5G-EVE_PORTAL"

        response = requests.get(url)

        if response.status_code == 200:
            sorted_bugs = sorted(response.json()['bugs'], key=lambda k: datetime.strptime(k['creation_time'],'%Y-%m-%dT%H:%M:%SZ'), reverse=True)
            if not is_admin:
                non_admin_bugs = []
                for b in sorted_bugs:
                    if b['component'] == "VNF_UPLOADS" and b['creator_detail']['email'] == requester:
                        non_admin_bugs.append(b)
                    elif b['component'] not in ["REGISTRATION", "VNF_UPLOADS"]:
                        non_admin_bugs.append(b)
                sorted_bugs = non_admin_bugs

            if int(page) > np.ceil(len(sorted_bugs)/10):
                return 404, "Tickets page not found"

            bugs = []
            start = (page*10)
            end = (page*10) + 10
            if end > len(sorted_bugs):
                end = len(sorted_bugs)

            for i in range(start, end):
                bugs.append(sorted_bugs[i])
            data = {}
            data['tickets'] = bugs
            data['totalTickets'] = len(sorted_bugs)
            data['numTickets'] = len(bugs)
            return response.status_code, data

        return response.status_code, response.content

    """ Method to create a bug
            @params: 
                - reporter_token: user token
                - bug_data: data provided to create a bug
                    - product: Name of the product where the bug is being created
                    - component: Name of the component inside the product where the bug is being created
                    - version: unspecified by default
                    - summary: summary of the bug
                    - description: description
                    - assigned_to: by default it will be the component owner
                - reporter: email of the admin reporter in case it is a ticket creation from a trusted service
    """
    def create_bug(self, reporter_token, bug_data, reporter):
        if reporter_token != None:
            url = self.bugzilla_data['bugs_uri'] + "?token=" + reporter_token
        elif reporter_token == None and reporter != None and reporter == self.bugzilla_data['username']:
            url = self.bugzilla_data['bugs_uri'] + "?api_key=" + self.bugzilla_data['admin_key']

        #TODO: hardcoded values not defaulted at bugzilla
        bug_data['version'] = "unspecified"
        bug_data['op_sys'] = "other"
        bug_data['platform'] = "pc"

        response = requests.post(url, data=bug_data)
        return response.status_code, response.json()

    """ Method to update a specific bug
            @params:
                - reporter_token
                - bug_data
                    - summary: new summary of the bug
                    - description: new description of the bug
                    - groups: group names to be added/removed
                        > "groups": {"add/remove": ["group1", "group2"]}
                    - assigned_to: email of the user to assign the bug
                    - status: new status of the bug. When changing to closed, resolution should be provided
                - bug_id
                - is_admin
            @return:
                status: HTTP code
                msg: information returned from bugzilla REST API
    """
    def update_bug(self, reporter, reporter_token, bug_data, bug_id, is_admin):
        if is_admin:
            url = self.bugzilla_data['bugs_uri'] + "/" + bug_id + "?token=" + reporter_token
            response = requests.put(url, data=bug_data)
        else:
            code, msg = self.get_bugs_by_id(requester=reporter, requester_token=reporter_token, bug_id=bug_id, is_admin=False)
            if code == requests.codes.ok:
                url = self.bugzilla_data['bugs_uri'] + "/" + bug_id + "?token=" + reporter_token
                response = requests.put(url, data=bug_data)
            else:
                return 401, json.loads(json.dumps({"error": "User not allowed to update bug #{}".format(bug_id)}))

        return response.status_code, response.json()
        
