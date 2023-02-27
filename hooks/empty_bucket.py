from botocore.exceptions import ClientError
from sceptre.hooks import Hook

from utilities.aws_client import get_resource, get_stack


class EmptyBucket(Hook):
    """
        Arguments (passed in as a dict):
            NONE

        Example Usage:
            hooks:
                before_delete:
                    - !empty_bucket
    """

    def __init__(self, *args, **kwargs):
        super(EmptyBucket, self).__init__(*args, **kwargs)

    def run(self):
        bucket_name = None
        try:
            stack = get_stack(self.stack)

            try:
                bucket_name = self._get_output_value(stack, self.argument)
            except ClientError as e:
                self.logger.warning(
                    f"WARN: unable to get bucket name for output '{self.argument}', was the stack deleted?"
                )
        except ClientError as e:
            pass

        if bucket_name:
            self._empty_s3_bucket(bucket_name)

    def _empty_s3_bucket(self, bucket_name: str):
        """clear the specified bucket of its content"""
        self.logger.info(f"Emptying contents of {bucket_name}")

        s3_resource = get_resource(self.stack, 's3')

        try:
            s3_bucket = s3_resource.Bucket(bucket_name)
            s3_versioning = s3_resource.BucketVersioning(bucket_name)

            if s3_versioning.status == 'Enabled':
                s3_bucket.object_versions.delete()
            else:
                s3_bucket.objects.all().delete()
        except Exception as e:
            self.logger.error(f"ERROR: while trying to remove items from {bucket_name}", exc_info=e)

    def _get_output_value(self, stack: dict, output_key: str) -> str:
        """return the value for the specified stack output"""
        outputs = stack['Outputs']

        if outputs:
            for item in outputs:
                key = item["OutputKey"]
                val = item["OutputValue"]

                if key == output_key:
                    return val

        return None


if __name__ == '__main__':
    h = EmptyBucket()
    h.run()
