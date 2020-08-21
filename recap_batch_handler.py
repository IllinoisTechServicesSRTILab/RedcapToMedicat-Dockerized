import json
from redcap_uin_isolation import redcap_uin_isloation
from REDCapMedicatImport import REDCapMedicatImport


def handler(bucket_name, bucket_key):

    # TODO here retreive the json from s3
    with open("./fake_medicat_json.json", "r") as f:
        meddata = json.load(f)
    redcap_uin_isloation(meddata)
    REDCapMedicatImport(meddata)


if __name__ == "__main__":
    handler(None, None)