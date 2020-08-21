import os

import boto3

client = boto3.client('s3')


def generate_downloads(bucket_name, remotepath, filename):
    url = client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': os.path.join(remotepath, filename)
        },
        ExpiresIn=604800  # one week
    )

    return url


def downloadToDisk(bucket_name, filename, localpath, remotepath):
    with open(os.path.join(localpath, filename), 'wb') as f:
        client.download_fileobj(bucket_name,
                                os.path.join(remotepath, filename), f)


def getObject(bucket_name, remoteKey):
    obj = client.get_object(Bucket=bucket_name, Key=remoteKey)


def listDir(bucket_name, remoteClass):
    objects = client.list_objects(Bucket=bucket_name,
                                  Prefix=remoteClass,
                                  Delimiter='/')
    foldernames = []
    for o in objects.get('CommonPrefixes'):
        foldernames.append(o.get('Prefix'))

    # only return the list of foldernames
    return foldernames


def listFiles(bucket_name, foldernames):
    objects = client.list_objects(Bucket=bucket_name,
                                  Prefix=foldernames)

    # return rich information about the files
    return objects.get('Contents')
