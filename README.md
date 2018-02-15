Help
----

```
python s3_uploader.py [-h] [-n NEW_NAME]
                      [-a {private,public-read,public-read-write,authenticated-read,aws-exec-read,bucket-owner-read,bucket-owner-full-control}]
                      [--loadenv]
                      bucket path

positional arguments:
  bucket        Name of the existing S3 bucket
  path            Path to file or dir

optional arguments:
  -h, --help            show this help message and exit
  -n NEW_NAME, --new_name NEW_NAME
                                 New file or dir name
  -a , --acl               ACL mode for uploading file
  --loadenv             Is loading .env file needed
```

ACL could be
- private
- public-read
- public-read-write
- authenticated-read
- aws-exec-read
- bucket-owner-read
- bucket-owner-full-control

Usage examples
--------------

```
python s3_uploader.py my-awesome-bucket /tmp/dirname --acl public-read --loadenv
```
After this command /tmp/dirname content will be accessible by url https://s3.amazonaws.com/my-awesome-bucket/dirname with public-read rights
<br><br>

```
python s3_uploader.py my-awsome-bucket /tmp/dirname --acl public-read --loadenv --new_name prefix/dir
```
This will upload /tmp/dirname https://s3.amazonaws.com/my-awesome-bucket/prefix/dir with public-read rights
<br><br>

```
python s3_uploader.py my-awsome-bucket /var/log/system.log --loadenv --new_name my_new_filename
```
This will upload /var/log/system.log file as https://s3.amazonaws.com/my-awesome-bucket/my_new_filename