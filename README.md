# compota
Social media to begin projects together, Final Project for CS50 Intro to CS course

# How to run
## Run flask server
`python -m flask run`

`python -m flask run --debugg` for reloading automatically and traceback on browser

## Generate secret key
You must provide a secret key to .env file so that the app can use for the sessions, you can generate one with

` python -c 'import secrets; print(secrets.token_hex())'`
## Generate the database
If it's not known, a way you can generate a database with the schema given in `compota.sql` is by using sqlite3 in command-line

`sqlite3 <db_name_>.sqlite3 < compota.sql`
