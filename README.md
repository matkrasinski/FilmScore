## Prerequirements:
- There need to be tmdb.csv file in `tmdb/` directory
- There should be IMDb files in imdb directory:
`title.basics.tsv`
`title.ratings.tsv`
`name.basics.tsv`
`title.principals.tsv`
`title.crew.tsv`.

- If they are absent, application will automatically download them from:
[IMDb non-commercial dataset](https://datasets.imdbws.com/`)
- You need to have installed Python 3.10 version and Node.js 14.
- If you want to run the app on Docker you also need to have it installed.
## Running App locally
- create virtual environment: `python -m venv .`
- install requirements: `pip install -r requirements.txt`
- run the app `python -m backend.app`
- go to `ui` directory
- install required dependencies `npm install`
- run user interface app `npm run serve`

- Flask app is running on port 5000
- Vue.js app is running on port 8080

## Running App in Docker Container
- build docker image: `docker compose build`
- run docker containers: `docker compose up`

## Note 
If you don't have `sqlite.db` initialized, go to `backend/config/db_status.py` and clean its content. Then the next time you run backend app it will initialize database

## Running tests
- run unit and api tests with single command: `pytest backend/tests`
- if you want to run ui tests go to `ui-testing`, install python environtemnt for testing `python -m venv .`, install requirements `pip install -r requirements.txt` and run single test file with: `python -m test/test_xxx.py`