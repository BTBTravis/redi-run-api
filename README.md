# REDI Run Backend

A API written with python + flask. Directly supports [REDI Run frontend react app](https://github.com/redi-js-teachers/js_sprint_2020_final_project_khomtali)

## Docs

This api is fully documented via [docs/openapi.yaml](docs/openapi.yaml), the swagger ui can be found **[here](https://btbtravis.gitlab.io/redi-run-backend/#/)**

## Arch

![tech arch diagram](docs/redi_run_arch.png)

## Development

*Currently @btbtravis is the sole contributer. This information needs to be updated before inviting collaborators*

Dev setup requries locally running:

- MongoDB server, in the future a docker-compose.yml will be provided for this
- Redis server, in the future a docker-compose.yml will be provided for this
- Python 3.7+ and pipenv as dependencies in the project are managed via pipenv

So the basic setup would look like this:

```shell
$ git clone git@gitlab.com:BTBTravis/redi-run-backend.git
$ cd redi-run-backend
$ cp .env.sample .env
```
*then update .env values*
```shell
$ pipenv install
$ pipenv shell
$ FLASK_APP=redi-run-app.py flask run -p 5001 --reload
```
