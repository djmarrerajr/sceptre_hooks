from sceptre.hooks import Hook

from utilities.aws_client import get_resource, get_stack_output


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
        bucket_name = self._get_output_value(self.argument)

        if bucket_name:
            self._empty_s3_bucket(bucket_name)

    def _empty_s3_bucket(self, bucket_name: str):
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
            self.logger.error(f"ERROR: Unable to remove items from {bucket_name}", exc_info=e)

    def _get_output_value(self, output_key: str) -> str:
        outputs = get_stack_output(self.stack)

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
