# Python GeoJSON API

This [Flask](https://flask.palletsprojects.com/en/2.2.x/) API serves GeoJSON to the [nextjs frontend](https://gitlab.tools.leapx.digital/tenants/geo/hex-api)

## Running the app

These are the commands to build and run
1. Install [Docker](https://docs.docker.com/get-docker/) on your machine
2. Build the docker image: `docker build . -t geo-api`
3. Run it `docker run --name geo-api geo-api`
4. Get the IP of the running container `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' geo-api` and use it to specify API_URL for frontend

The API should be available on [localhost:7007](http://localhost:7007)

# Learn More

## Dependencies

- [Flask](https://flask.palletsprojects.com/en/2.2.x/) - for creating API endpoints to the app
- [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/) - memoization is used to cache long running tasks to disk, making them fast on subsequent runs
- [GeoJSON](https://pypi.org/project/geojson/) - Python library for working with the [GeoJSON spec](https://geojson.org)
- [gunicorn](https://gunicorn.org) - is configured in the Dockerfile to serve the API
