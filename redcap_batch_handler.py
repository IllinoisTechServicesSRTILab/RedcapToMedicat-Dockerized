import argparse
import json
import os

import boto3

from REDCapMedicatImport import REDCapMedicatImport
from redcap_uin_isolation import redcap_uin_isloation

client = boto3.client('s3')


def handler(bucket_name, bucket_key):
    # create a data dir to hold temp json downloaded from s3
    localPath = os.path.join('/tmp', 'medicat')
    if not os.path.exists(localPath):
        os.makedirs(localPath)

    with open(os.path.join(localPath, "medicat.json"), 'wb') as fb:
        client.download_fileobj(bucket_name, bucket_key, fb)

    with open(os.path.join(localPath, "medicat.json"), 'r') as f:
        meddata = json.load(f)

    redcap_uin_isloation(meddata)
    REDCapMedicatImport(meddata)


if __name__ == "__main__":

    # read in command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--S3BucketName', required=True)
    parser.add_argument('--S3ObjectKey', required=True)
    params = vars(parser.parse_args())

    # main
    print(params["S3BucketName"], params["S3ObjectKey"], flush=True)
    handler(bucket_name=params["S3BucketName"], bucket_key=params["S3ObjectKey"])
