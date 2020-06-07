# REDI Run Backend

This is a little python flask app that serves as a backend for the [redi run project](https://github.com/redi-js-teachers/js_sprint_2020_final_project_khomtali)


## Docs

This api is fully documented under via an openapi.yaml file that builds a static docs site [here](https://btbtravis.gitlab.io/redi-run-backend/#/)

## Development

If you want to run this app locally you'll need a few things

- mongo db server, setting this up via docker is easiest
- pytho and pipenv, dependancies in the project are managed via pipenv

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