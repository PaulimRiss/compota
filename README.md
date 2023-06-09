# compota
Social media to begin projects together, Final Project for CS50 Intro to CS course

# How to run
## Run flask server
`python -m flask run`

`python -m flask run --debugg` for reloading automatically and traceback on browser

## Generate secret key
You must provide a secret key to .env file so that the app can use for the sessions, you can generate one with

` python -c 'import secrets; print(secrets.token_hex())'`
