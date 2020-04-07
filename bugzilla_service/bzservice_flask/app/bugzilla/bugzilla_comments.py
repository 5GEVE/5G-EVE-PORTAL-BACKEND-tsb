import requests, json

class BugzillaComment:

    def __init__(self, bugzilla_data):
        self.bugzilla_data = bugzilla_data

    """ Retrieve all comments of a specific bug
            @params:
                - requester_token: token provided by the user who is asking for comments
                - bug_id: bug identifier
                - is_admin: flag that indicates whether the user is admin or not
            @return:
                - list of comments or error
    """
    def get_comments(self, requester_token, bug_id, is_admin):
        if is_admin:
            url = self.bugzilla_data['bugs_uri'] + '/' + str(bug_id) + '/comment' + "?api_key=" + self.bugzilla_data['admin_key']
        else:
            url = self.bugzilla_data['bugs_uri'] + '/' + str(bug_id) + '/comment' + "?token=" + requester_token
        response = requests.get(url)

        if response.status_code == requests.codes.ok:
            data = response.json()
            return response.status_code, json.loads(json.dumps(data['bugs'][bug_id]['comments']))

        return response.status_code, response.json()

    """ Method to create a comment inside a bug
            @params:
                - requester_token: token provided by the user who is asking for comments
                - bug_id: bug identifier
                - comment_data: data to generate the comment
                    - comment: comment to be added
                    - comment_tags: array of strings to be added as tags to the comment
            @return:
                - identifier of the already created comment or error
    """
    def create_comment(self, user_token, bug_id, comment_data):

        url = self.bugzilla_data['bugs_uri'] + '/' + str(bug_id) + '/comment?token=' + user_token
        
        response = requests.post(url, data=comment_data)

        return response.status_code, response.json()

    """ Retrieve details of a specific comment
            @params:
                - requester_email: email of the user requesting a specific comment
                - requester_token: token provided by the user who is asking for comments
                - comment_id: comment identifier
                - is_admin: flag that indicates whether the user is admin or not
            @return:
                - comment (inside a list of bugs) or error message
    """
    def get_comment(self, requester_email, requester_token, comment_id, is_admin):

        if is_admin:
            url = self.bugzilla_data['bugs_uri'] + '/comment/' + str(comment_id) + "?api_key=" + self.bugzilla_data['admin_key']
        else:
            url = self.bugzilla_data['bugs_uri'] + '/comment/' + str(comment_id) + "?token=" + requester_token
        response = requests.get(url)

        if response.status_code == requests.codes.ok:
            data = response.json()
            if data['bugs'][0]['comments'][0]['creator'] == requester_email:
                return response.status_code, json.loads(json.dumps(components))
            else:
                return 401, json.loads(json.dumps({'details': 'User {} not allowed to get comment details'.format(requester_email)}))

        return response.status_code, response.json()

    """ Method to update tags of a specific comment inside a bug
            @params:
                - reporter_token
                - comment_data
                    - comment_id: identifier of the comment where to modify tags
                    - add/remove: ['tag1', 'tag2']
                - comment_id
                - is_admin
            @return:
                status: HTTP code
                msg: information returned from bugzilla REST API
    """
    def update_bug(self, user_email, user_token, comment_data, comment_id, is_admin):
        if is_admin:
            url = self.bugzilla_data['bugs_uri'] + '/comment/' + str(comment_id) + '/tags' + '?token=' + reporter_token
            response = requests.put(url, data=comment_data)
        else:
            code, msg = self.get_comment(user_email, user_token, comment_id, is_admin)
            if code == requests.codes.ok:
                url = self.bugzilla_data['bugs_uri'] + '/comment/' + str(comment_id) + '/tags' + '?token=' + reporter_token
                response = requests.put(url, data=comment_data)
            else:
                return 401, json.loads(json.dumps({"error": "User not allowed to update comment #{} flags".format(comment_id)}))

        return response.status_code, response.json()
