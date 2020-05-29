import requests, json

class BugzillaComponent:

    def __init__(self, bugzilla_data):
        self.bugzilla_data = bugzilla_data

    """ Retrieve all components of a product
            @params:
                - product_id: product identifier
    """
    def get_components(self, product_id):
        # Get product who stores the components
        response = requests.get(self.bugzilla_data['products_uri'] + '/' + str(product_id))

        if response.status_code == requests.codes.ok:
            data = response.json()
            if len(data['products']) > 0:
                components = []
                for component in data['products'][0]['components']:
                    if component['name'] != "REGISTRATION":
                        component = {'id': component['id'], 'name': component['name'], 'description': component['description']}
                        components.append(component)
                return response.status_code, json.loads(json.dumps(components))
            else:
                return response.status_code, json.loads(json.dumps([]))

        return response.status_code, response.json()

    """ Retrieve all components of a product
            @params:
                - product_id: product identifier
    """
    def get_components_all_details(self, product_id):
        # Get product who stores the components
        response = requests.get(self.bugzilla_data['products_uri'] + '/' + str(product_id))

        if response.status_code == requests.codes.ok:
            data = response.json()
            if len(data['products']) > 0:
                print(data)
                return response.status_code, data['products'][0]['components']
            else:
                return response.status_code, json.loads(json.dumps([]))

        return response.status_code, response.json()        

        
