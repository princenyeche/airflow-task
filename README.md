# Apache Airflow
Running DAGs development test and configurations

## Installation using Docker

> [!INFO] Prerequisite
> Python must be installed on the system

```shell
docker pull apache/airflow:slim-latest-python3.13
# starting the service
docker run -p 8181:8181 apache/airflow:slim-latest-python3.13
```

###  Identify ports in use by running
```shell
lsof -i -n -P | grep TCP
```

This way, when creating the service port above, you don't hit a conflict.


Building an image using a `Dockerfile`

```shell
FROM apache/airflow:3.1.2
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
```


## Set Airflow Home
Airflow requires a home directory, and uses `~/airflow` by default, but you can set a 
different location if you prefer. The `AIRFLOW_HOME` environment variable is used to inform Airflow
of the desired location.

```shell
export AIRFLOW_HOME=~/airflow
```

###  Install using uv 

- Ensure you have uv installed on your machine
- You can use a constraint file, which is determined based on the URL passed.

```shell
AIRFLOW_VERSION=3.1.2

# Extract the version of Python you have installed. If you're currently using a Python version that is not supported by Airflow, you may want to set this manually.
# See above for supported versions.
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 3.0.0 with python 3.10: https://raw.githubusercontent.com/apache/airflow/constraints-3.1.2/constraints-3.10.txt

uv pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
# activate virtual environment
source .venv/bin/activate
```
> OR run the shell script

```shell
chmod +x run-airflow.sh
./run-airflow.sh
```
If the virtual environment doesn't change directly, you can manually ensure you're in 
a virtual environment by running
```shell
cd to_the_dirs_where_virtual_env_exist
.venv/bin/activate
# then cd back to the airflow dir
cd airflow
```

### Run the command

The `airflow standalone` command initializes the database, creates a user, and starts all components.
```shell
airflow standalone
```

### Access Airflow UI

Visit `localhost:8080` in your browser and log in with the admin account details shown in the terminal.
Note: The admin password is only displayed once and saved in the airflow directory, which is found 
```shell
cd ~/airflow/simple_auth_manager_passwords.json.generated
```


### Optional startup
If you want to run the individual parts of Airflow manually rather than using the all-in-one standalone command, you can instead run:

```shell
airflow db migrate

airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

airflow api-server --port 8080

airflow scheduler

airflow dag-processor

airflow triggerer
```

## To load Dags in UI
- Change the `airflow.cfg` file for the core path

```shell
cd ~/airflow
vi airflow.cfg
```
Look for the [core] header
```markdown
[core]
# The folder where your airflow pipelines live, most likely a
# subfolder in a code repository. This path must be absolute.
#
# Variable: AIRFLOW__CORE__DAGS_FOLDER
#
dags_folder = /Users/<name_of_device>/airflow/dags
```
change `dags_folder` `/to/path/absolute/` of where you want the dags to reside
