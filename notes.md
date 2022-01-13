# Deploying to heroku

- install heroku command line
- log in the heroku from the command line
  - `heroku container:login`
- provision a new postgres database with the *hobby-dev*
  - `heroku addons:create heroku-postgresql:hobby-dev --app sleepy-plateau-70707`
- build the production image and tag it with the following format:
  - `registry.heroku.com/<app>/<process-type>`
  - `docker build -f Dockerfile.prod -t registry.heroku.com/sleepy-plateau-34343/web .`
- you can test this container that you create:
  - `docker run --name flask-tdd -e "PORT=8765" -p 5005:8765 registry.heroku.com/sleep-pletay-78787/web:latest`
- build the new image and the push it to the registry:
  - `docker build -f Dockerfile.prod -t registry...`
  - `docker push registry...`
- release the image:
  - `heroku container:release web --app sleepuy...`


# Running commands on the heroku command line

- `heroku run python manage.py recreate_db --app sleepy-plateau-85855`