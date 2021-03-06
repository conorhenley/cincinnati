#Cincinnati

This is the continuation of the Cincinnati [summer project](https://github.com/dssg/cincinnati2015-public) done during DSSG 2015.

##About

First settled in 1788, Cincinnati is one of the oldest American cities west of the original colonies. Today, the 
city struggles with aging home stock, stifling economic redevelopment in some neighborhoods. 

DSSG is working with the City of Cincinnati to identify properties at risk of code violations or abandonment. We hope
that early intervention strategies can prevent further damage and stimulate neighborhood revitalization. Read more about
our project [here](http://dssg.uchicago.edu/2015/08/20/cincy-blight-prevention.html). 

##Setup

###Select folders for the code, data and output

The code relies on three environment variables, before you start running the code, decide where are you going to store the *raw data*,  *code* and *output*, a sample file `env_sample.sh`, which looks like this:

```bash
#Where to store the code
export ROOT_FOLDER="/path/to/repo/"
#Where data is stored
export DATA_FOLDER="/path/to/data/"
#Where to output results from models
export OUTPUT_FOLDER="/path/to/output/"

#Add lib folder to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$ROOT_FOLDER/lib_cinci
```

Modify the three environment variables, the `PYTHONPATH` line is also necessary since it includes many functions used across the project. Consider adding that to your shell profile, so they get loaded automatically.

###Clone the repo

Clone the repo in `$ROOT_FOLDER`

```bash
git clone https://github.com/dssg/cincinnati $ROOT_FOLDER
```

###Put the data following the repo structure

The pipeline follows certain simple conventions to make the code easy to understand. It is assumed that a file in `$ROOT_FOLDER/etl/something/` will get its raw data from `$DATA_FOLDER/etl/something/`.

Having, said that it's easy to know where to store the raw data. For example, the code that loads all taxes data is `$ROOT_FOLDER/etl/taxes/taxes.sh`, then, your raw taxes files should be stores in `$DATA_FOLDER/etl/taxes/`

The other convention is that intermediate files are stored on a `tmp/` folder, for example, since we need to preprocess the taxes files before uploading them to the database, the intermediate csv files will be on `$DATA_FOLDER/etl/taxes/tmp/`.

###Provide config.yaml, logger_config.yaml and pgpass

The code loads some parameters from a `config.yaml` file stored in the `$ROOT_FOLDER`. `logger_config.yaml` configures the logger for the Python interpreter.

Use the `config_sample.yaml` file to see the structure and then rename it to `config.yaml`, make sure that the file is stored in your `$ROOT_FOLDER`. Do the same for `logger_config.yaml`.

`.pgpass` (note the dot) is needed if your are going to use the Docker image and it will take
the file in `$ROOT_FOLDER/.pgpass` to build it. If you are not going to use Docker, just make sure that a standard `.pgpass` file is on your home folder. See `.pgpass_sample` for syntax details.

###Build docker ETL image

The ETL step depends on these programs:

* Python 2.7.11
* GDAL 1.11.2
* Java 1.8
* psql (PostgreSQL) 9.3.10
* PostGIS 2.1.4
* mdbtools 0.7.1 
* gnumeric 1.12.9
* stanford-ner-2015-12-09
* ...and many Python packages

To ease the setup, a Dockerfile is provided which builds an Ubuntu 14.04 image with all dependencies included and properly configured.

Most dependencies are needed for the ETL step, after the raw data is on the database, only Python (and a few packages) and psql is needed, hence, if you want, you can use the Docker image for the ETL phase only. For information on how to setup Docker, see the [official docs](https://docs.docker.com/).

Once Docker is properly setup, go to your `$ROOT_FOLDER` and run:

```bash
docker build -t cincinnati .
```

This process takes a while since it needs to download and install all dependencies, but with a decent internet connection is should take less than 1 hour.

###Run docker image

Once the image is ready, run it: 

```bash
docker run -v $DATA_FOLDER:/root/data -v $ROOT_FOLDER:/root/code -v $OUTPUT_FOLDER:/root/output -i -t cincinnati /bin/bash
```

Note that we are passing our three environment variables, and linking them to three folders inside the container. The purpose of the Docker container is to run code but not to store anything (not code and of course not data).

##Data Pipeline

Once you have set up your environment, you can start usng the pipeline, the general procedure is the following (specific instructions for each step are available inside each subfolder):

1. Load data into the database 
   1. Use the [ETL folder](etl/) to upload all the data to the database
   2. Perform geocoding on some datasets. Use the [bulk_geocode](bulk_geocoder/) for this.
2. Explore the data
3. [Generate features](model/features) from the data
4. Run some experiments. Use `model.py` inside [model](model/) to train models. `model.py` requires you to provide a configuration file, see `default.yaml` in this folder for reference.  [experiments](model/experiments) folder contains more examples.
5. Evaluate experiments
6. Prepare a new field test using the tools in [field_test_preparation](field_test_preparation/)