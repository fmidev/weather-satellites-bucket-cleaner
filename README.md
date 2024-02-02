# Container recipe to clean S3 buckets

This recipe is automatically built on new version tags, and the image
is available from
https://quay.io/repository/fmi/weather-satellites-bucket-cleaner

The shortest cleaning cycle S3 supports is once-per-day. This
container can be used to clean S3 buckets with shorter cycle and
tighter cleaning.

## Configuration

The configuration files should be mounted to `/config/` directory.

### `/config/env-variables`

This file is used to set three strictly required environment variables:

```bash
# Name of the S3 bucket to be cleaned
export CLEAN_S3_BASE_URI="name-of-the-bucket"
# Maximum age of the objects in hours. Older objects will be deleted.
export CLEAN_S3_MAX_AGE="3"
# How often the cleaning is run. Given in seconds.
export CLEAN_S3_CYCLE_SECONDS="3600"
```

If the S3 storage requires configuration, set also the path to your S3
config:

```bash
# Location of s3.json configuration file
export FSSPEC_CONFIG_DIR="/config/"
```

See
https://filesystem-spec.readthedocs.io/en/latest/features.html#configuration
for the S3 access configuration.

The S3 credentials should be injected as environment variables and not
written to the config file.
