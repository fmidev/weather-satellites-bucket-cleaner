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

    print(now, "- Start cleaning", base_uri)

    s3 = S3FileSystem()

    tic = time.time()
    num = 0
    for prefix, sub_prefixes, objects in s3.walk(base_uri):
        for obj in objects:
            uri = os.path.join(prefix, obj)
            stat = s3.stat(uri)
            if stat['LastModified'] < max_age:
                age = (now - stat['LastModified']).total_seconds() / 3600.
                age_unit = "hours"
                if age > 24:
                    age /= 24.
                    age_unit = "days"
                print(f"Delete {uri} - age is {age:.1f} {age_unit}")
                s3.delete(uri)
                num += 1

    elapsed = time.time() - tic
    print(dt.datetime.now(dt.timezone.utc), f"- {num} objects deleted in {elapsed:.1f} seconds")

if __name__ == "__main__":
    main()
