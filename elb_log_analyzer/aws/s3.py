#!/usr/bin/env python

# standard library imports

# third party related imports
import boto.s3
from boto.s3.key import Key

# local library imports
from elb_log_analyzer.config import setting
from elb_log_analyzer.logger import logger


class S3(object):

    def __init__(self, bucket_name):

        self.conn = boto.s3.connect_to_region(
            setting.get('elb_log_s3', 'region'),
            aws_access_key_id=setting.get('aws', 'access_key'),
            aws_secret_access_key=setting.get('aws', 'secret_key')
        )
        self.bucket = self.conn.get_bucket(bucket_name)

    def download(self, key_name, output_fn):

        k = Key(self.bucket)
        k.key = key_name
        k.get_contents_to_filename(output_fn)

        logger.info('Download %s -> %s', key_name, output_fn)


if __name__ == '__main__':

    from contextlib import closing
    from tempfile import NamedTemporaryFile

    s3 = S3('kono-lb-logs')
    with closing(NamedTemporaryFile()) as f:
        s3.download(
            'optimus-prime/AWSLogs/127634673729/ELBAccessLogTestFile',
            f.name
        )
        print f.read()