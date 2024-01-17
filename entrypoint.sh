#!/usr/bin/bash

source /opt/conda/.bashrc
source /config/env-variables

micromamba activate

while true; do
    /opt/conda/bin/clean_s3.py $CLEAN_S3_BASE_URI $CLEAN_S3_MAX_AGE
    sleep $CLEAN_S3_CYCLE_SECONDS
done
