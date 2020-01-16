  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# 5G-EVE Portal Components
This repository contains part of the back-end modules implementing the functionality provided by 5G-EVE portal. It contains modules for authentication/authorization relying on Keycloak and a ticketing system which basically relies on bugzilla.

# Packages included

## bugzilla_service and bugzilla-docker
Bugzilla docker is basically a dockerized version of bugzilla based on [FullMetalGeo](https://github.com/FullMetalGeo/bugzilla-docker) work. with bugzilla_service, we provide another plain REST API allowing users authenticated through RBAC to interact directly with bugzilla without using its web interface.

# Running and configuring components
## Dockerized bugzilla
First, go to bugzilla_docker/answers.txt and modify the default values for the admin account. Then, run: 
```{bash}
cd bugzilla_docker
docker-compose up
```
Now, It's time to configure bugzilla in order for bugzilla service to be able to manage everything. In order to do so, follow the steps below:
* Configure smtp server: go to ```administration > Email``` and change the ```email_delivery_method``` parameter (Test to disable smtp).
* bugzilla_service user account creation: Create an admin user in order for bugzilla_service to manage users/bugs CRUD operations (```administration > Users > add a new user```)
* Create an API Key for bugzilla_user: In order to authenticate our service against bugzilla, go to ```Preferences > API Keys``` and generate a new API Key.

## Dockerized Flask bugzilla_service
Right before running the service, go to ```bugzilla_service/bugzilla/``` and modify ```bugzilla_data.json``` with the user acount and API Key generated in the previous steps.
Then, we also need to create a client account at keycloak in order to make our service trusted. At Keycloak, perform the following actions:
* ```Clients > Create```:Create a new client.
* ```Clients > Access Type = confidential```
* ```Clients > Valid Redirect URIs```: place a valid URI (or * to accept all)

Now, at ```Clients > "new_client" > Credentials``` we have the secret that will be used in our service to make it trusted. Moreover, to be able to manage roles and groups from our service, we also need a user account for our service:
* ```Users > Add user```
* (Optional) ```Users > new_user > Role Mappings```: add roles to the user that will be used by the service.

Let's now add all the information at ```bugzilla_service/bz_service_flask/keycloak.json``` (client_id, client_secret, admin_username, admin_password).

Finally, run:

```{bash}
cd bugzilla_service
docker-compose up
```

At this point, our service will be reachable at 0.0.0.0:9090

## Authors
Ginés García Avilés [Gitlab](https://gitlab.com/GinesGarcia) [Github](https://github.com/GinesGarcia) [website](https://www.it.uc3m.es/gigarcia/index.html)

## Acknowledgments
* [5G EVE](https://www.5g-eve.eu/)