import requests, os, json, functools
from flask import jsonify
from .bugzilla_products import BugzillaProducts
from .bugzilla_components import BugzillaComponent
from .bugzilla_bugs import BugzillaBug
from .bugzilla_comments import BugzillaComment

class BugzillaClient:

    def __init__(self):
        with open(os.path.abspath(os.path.dirname(__file__))+'/bugzilla_data.json') as config:
            self.bugzilla_data = json.load(config)

        self.products = BugzillaProducts(self.bugzilla_data)
        self.components = BugzillaComponent(self.bugzilla_data)
        self.bugs = BugzillaBug(self.bugzilla_data)
        self.bug_comments = BugzillaComment(self.bugzilla_data)

    """ Method to create new users at bugzilla
            @params:
                - email
                - full_name
                - password
            @return: HTTP code + details message
    """
    def create_user(self, user_data):
        url = self.bugzilla_data['users_uri'] + "?api_key=" + self.bugzilla_data['admin_key']
        response = requests.post(url, data=user_data)

        return response.status_code, response.json()

    """ Login method
            @params: email + password
            @return:
                - HTTP code
                - Details message: if success, it will include an access token that belongs to the authenticated user
    """
    def login(self, user_data):
        url = self.bugzilla_data['login_uri'] + "?login=" + user_data['email'] + "&password=" + user_data['password']
        response = requests.get(url)
        
        if response.status_code != 200:
            return response.status_code, "User not found"
        
        return response.status_code, response.json()
    
    """ Logout method
            @params: user session token
            @return: HTTP code + details message
    """
    def logout(self, token):
        url = self.bugzilla_data['logout_uri'] + "?token='*'" + token
        response = requests.get(url)
        return response.status_code, response.json()        


    def get_admin_users(self):
        url = self.bugzilla_data['users_uri'] + "?api_key=" + self.bugzilla_data['admin_key'] + '&match=*@*'
        response = requests.get(url)

        if response.status_code != requests.codes.ok:
            return response.status_code, response.json()        
        else:
            data = response.json()
            admin_users = []
            for user in data['users']:
                for group in user['groups']:
                    if group['name'] == 'admin':
                        admin_users.append(user['email'])
                        break
            
            return response.status_code, json.loads(json.dumps({'users': admin_users}))

    #### PRODUCTS MANAGEMENT ####
    def get_products(self):
        return self.products.get_products()

    #### COMPONENTS MANAGEMENT ####
    def get_components(self, product_id, detailed):
        if detailed:
            return self.components.get_components_all_details(product_id)
        else:
            return self.components.get_components(product_id)

    #### BUGS MANAGEMENT ####
    def get_bug(self, requester_email, requester_token, bug_id, is_admin):
        return self.bugs.get_bugs_by_id(requester_email, requester_token, bug_id, is_admin)

    def get_bugs(self, requester_email, requester_token, is_admin, page):
        return self.bugs.get_bugs_by_creator(requester_email, requester_token, is_admin, page)

    def create_bug(self, reporter_token, bug_data):
        return self.bugs.create_bug(reporter_token, bug_data)

    def update_bug(self, reporter_email, reporter_token, bug_data, bug_id, is_admin):
        return self.bugs.update_bug(reporter_email, reporter_token, bug_data, bug_id, is_admin)

    def get_bug_comments(self, requester_token, bug_id, is_admin):
        return self.bug_comments.get_comments(requester_token, bug_id, is_admin)

    def create_bug_comment(self, user_token, bug_id, comment_data):
        return self.bug_comments.create_comment(user_token, bug_id, comment_data)
