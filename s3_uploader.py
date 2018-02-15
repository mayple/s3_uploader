import mimetypes
import os
import argparse
import sys
import boto3

from botocore.exceptions import ClientError
from dotenv import load_dotenv, find_dotenv


def upload_file_to_s3(s3_client, bucket, file, bucket_key, acl):
    """
    Uploads a file to Amazon S3
    """
    try:
        guessed_mime_type = mimetypes.guess_type(file)
        s3_client.put_object(
            ACL=acl,
            Body=open(file, 'rb'),
            Bucket=bucket,
            Key=bucket_key,
            ContentType=guessed_mime_type[0]
        )
    except ClientError as err:
        print("Failed to upload file to S3.\n" + str(err))
        return False
    except IOError as err:
        print("Failed to access file in this directory.\n" + str(err))
        return False
    return True


def create_s3_client():
    """
    Creates a client for S3.
    Needs AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID to be set as environment vars
    :return:
    """
    try:
        client = boto3.client('s3')
        return client
    except ClientError as err:
        print("Failed to create boto3 client.\n" + str(err))
        return False


def prepare_single_file(path, new_name):
    if new_name is None or new_name == "":
        new_name = os.path.split(path)[1]

    return [(path, new_name)]


def prepare_dir_files(dir_path, new_name):
    if new_name is None or new_name == "":
        path_without_dir_name, dir_name = os.path.split(dir_path)
    else:
        path_without_dir_name, _ = os.path.split(dir_path)
        dir_name = new_name

    paths = []
    for root, directories, filenames in os.walk(dir_path):
        for filename in filenames:
            local_path = os.path.join(root, filename)
            paths.append(local_path)

    result = []
    for path in paths:
        relative_path = os.path.relpath(path, dir_path)
        result.append(
            (path, os.path.join(dir_name, relative_path))
        )

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bucket", help="Name of the existing S3 bucket")
    parser.add_argument("path", help="Path to file or dir")
    parser.add_argument("-n", "--new_name", help="New file or dir name",
                        default="")
    parser.add_argument("-a", "--acl",
                        help='ACL mode for uploading file',
                        choices=["private", "public-read", "public-read-write", "authenticated-read", "aws-exec-read",
                                 "bucket-owner-read", "bucket-owner-full-control"],
                        default="private")
    parser.add_argument("--loadenv", help="Is loading .env file needed", action="store_true")

    args = parser.parse_args()

    if args.loadenv:
        load_dotenv(find_dotenv())

    path = args.path
    if not os.path.exists(path):
        print("File does not exists {}".format(path))
        sys.exit(1)

    files_to_upload = []
    if os.path.isfile(path):
        files_to_upload = prepare_single_file(path, args.new_name)

    if os.path.isdir(path):
        files_to_upload = prepare_dir_files(path, args.new_name)

    client = create_s3_client()
    if client is False:
        sys.exit(1)

    for local_path, remote_path in files_to_upload:
        if not upload_file_to_s3(client, args.bucket, local_path, remote_path, args.acl):
            sys.exit(1)


if __name__ == "__main__":
    main()
