#!/usr/bin/env python

import datetime as dt
import os
import sys
import time

from s3fs import S3FileSystem


def main():
    """Run the S3 cleaner."""
    base_uri = sys.argv[1]
    now = dt.datetime.now(dt.timezone.utc)
    max_age = now - dt.timedelta(hours=int(sys.argv[2]))

    print(now, "- Start cleaning", base_uri, flush=True)

    s3 = S3FileSystem()

    tic = time.time()
    num = 0
    for prefix, sub_prefixes, objects in s3.walk(base_uri):
        num = _check_age_and_delete_objects(s3, prefix, objects, max_age)

    elapsed = time.time() - tic
    print(dt.datetime.now(dt.timezone.utc),
          f"- {num} objects deleted in {elapsed:.1f} seconds",
          flush=True)


def _check_age_and_delete_objects(s3, prefix, objects, max_age):
    num = 0
    for obj in objects:
        uri = os.path.join(prefix, obj)
        stat = s3.stat(uri)
        if stat['LastModified'] < max_age:
            age = _get_age(stat['LastModified'])
            _delete_object(s3, uri, age)
            num += 1
    return num


def _get_age(modified):
    now = dt.datetime.now(dt.timezone.utc)
    age = (now - modified).total_seconds() / 3600.
    age_unit = "hours"
    if age > 24:
        age /= 24.
        age_unit = "days"
    return f"age is {age:.1f} {age_unit}"


def _delete_object(s3, uri, age):
    print(f"Delete {uri} - {age}", flush=True)
    s3.delete(uri)


if __name__ == "__main__":
    main()
