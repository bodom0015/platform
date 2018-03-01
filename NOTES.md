# Notes on Automated Deployment
An experiment in deploying and seeding the platform in a way that minimizes required human interaction.

# Prerequisites
* Git
* Docker

Clone this repository:
```bash
git clone https://github.com/knoweng/platform
cd platform/
```

Run a postgres:9.6.2 container from the official image:
```bash
docker run -p 5432:5432 -d --name=postgres -e PGDATA="/data/db/postgres" -e POSTGRES_USER="nest" -e POSTGRES_PASSWORD="GARBAGESECRET" postgres:9.6.2
```

Optional: Run a redis:3.0.3 container from the official image:
```bash
docker run -p 6379:6379 -d --name=redis redis
```

NOTE: Both of these containers are started with ephemeral storage (for testing only)

# Build
Build the two docker images with the following commands:
```bash
docker build -t nest/nest:flask -f Dockerfile.flask .
docker build -t nest/nest:jobs -f Dockerfile.jobs .
```

# Run
Run a test flask container in the foreground from the image you've just built:
```bash
docker run -it --rm --name flask2 \
    -p 80:80 -p 443:443 \
    --link postgres:postgres \
    -e POSTGRES_USERNAME="nest" \
    -e POSTGRES_PASSWORD="GARBAGESECRET" \
    -e POSTGRES_HOST="postgres" \
    -e POSTGRES_PORT="5432" \
    -e POSTGRES_DATABASE="nest" \
    -e AWS_SHARED_MNT_PATH="/mnt/knowdev/YOUR_NETID" \
    -e AWS_MESOS_MASTER="fixme.yourhost.com:4400" \
    -e AWS_REDIS_HOST="fixme.yourhost.com" \
    -e AWS_REDIS_PORT="6379" \
    -e AWS_REDIS_PASS="GARBAGE_SECRET" \
    -e SEED_USERS="fakeuser:GARBAGE_SECRET:False;fakeadmin:GARBAGE_SECRET:True" \
    nest/nest:flask
```
NOTE: the `SEED_USERS` variable is a semi-colon delimited list of users formatted as follows:
```
username:password:is_admin

For example:
fakeuser:fakeuser_password:False;fakeadmin:fakeadmin_password:True
```

Each time that the container starts up, you should see in the logs that it checks for the existence of the necessary tables in the "nest" database. The tables will be created if they do not already exist.

The `nest_users` table will also be populated with the value you have set above for `SEED_USERS` in your evironment, if they do not already exist in the database.

# Test
Navigate to https://localhost/static/index.html in your browser.

You should be able to log in as any of the users defined in `SEED_USERS` in your environment.

# Next Steps
* Need EFS mount containing the `/networks` data
* Ensure that database seed job runs correctly (e.g. all dependencies present)
* Refactor `nest_py/knoweng/jobs/chronos_job.py` into a base class and similar `kubernetes_job.py`
* Explore database locking techniques in Python
    * `app2` appears to startup multiple times in rapid succession, causing a race condition
