import requests, json

class BugzillaProducts:

    def __init__(self, bugzilla_data):
        self.bugzilla_data = bugzilla_data

    """ Retrieve all product identifiers that a user can enter a bug against
    """
    def get_products(self):
        url = self.bugzilla_data['products_uri'] + '_enterable'
        response = requests.get(url)

        if response.status_code == requests.codes.ok:
            data = response.json()
            products = []
            for product_id in data['ids']:

                response = requests.get(self.bugzilla_data['products_uri'] + '/' + str(product_id))
                if response.status_code == requests.codes.ok:
                    product_data = response.json()
                    product = {'id': product_id, 'name': product_data['products'][0]['name'], 'description': product_data['products'][0]['description']}
                    products.append(product)
            return response.status_code, json.loads(json.dumps(products))

        return response.status_code, response.json()

        
