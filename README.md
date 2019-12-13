  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# 5G-EVE Portal Components
This repository contains part of the back-end modules implementing the functionality provided by 5G-EVE portal. It contains modules for authentication/authorization relying on Keycloak and a ticketing system which basically relies on bugzilla.

# Packages included

## bugzilla_service and bugzilla-docker
Bugzilla docker is basically a dockerized version of bugzilla based on [FullMetalGeo](https://github.com/FullMetalGeo/bugzilla-docker) work. with bugzilla_service, we provide another plain REST API allowing users authenticated through RBAC to interact directly with bugzilla without using its web interface.

## Authors
Ginés García Avilés [Gitlab](https://gitlab.com/GinesGarcia) [Github](https://github.com/GinesGarcia) [website](https://www.it.uc3m.es/gigarcia/index.html)

## Acknowledgments
* [5G EVE](https://www.5g-eve.eu/)