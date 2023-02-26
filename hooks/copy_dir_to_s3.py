from os import path, walk
from mimetypes import guess_type
from pathlib import Path
from sceptre.hooks import Hook
from shutil import rmtree

from utilities.aws_client import get_client, get_stack_output


class CopyDirToS3(Hook):
    """
        This hook will recursively copy a directory tree to an S3 bucket.
        It will also, optionally, delete the source directory upon completion.

        Arguments (passed in as a dict):
            NONE

        Example Usage:
            hooks:
                after_create:
                    - !copy_dir_to_s3
                        source_dir: 'path to copy'
                        bucket_name: 'name of target bucket'
                        remove_source: true/false
    """

    def __init__(self, *args, **kwargs):
        super(CopyDirToS3, self).__init__(*args, **kwargs)

    def run(self):
        source_dir, bucket_name, remove_source = self._parse_arguments()

        if source_dir and bucket_name:
            self._copy_directory_to_s3(source_dir, bucket_name, remove_source)

    def _copy_directory_to_s3(self, source_dir, bucket_name, remove_source):
        s3_client = get_client(self.stack, 's3')
        bucket_name = self._get_output_value(bucket_name)

        try:
            self.logger.info(f"Copying contents of {source_dir} to {bucket_name}")

            for current_dir, subdirs, files in walk(source_dir):
                for filename in files:
                    destination_path = current_dir.replace(source_dir, '')
                    s3_object = path.normpath(destination_path + '/' + filename)
                    source_file = path.join(current_dir, filename)

                    content_type, encoding = guess_type(filename)
                    if content_type:
                        metadata = {'ContentType': content_type}
                    else:
                        metadata = None

                    s3_object = s3_object.replace('\\', '/')[1:]
                    s3_client.upload_file(source_file, bucket_name, s3_object, ExtraArgs=metadata)
        except Exception as e:
            self.logger.error(f"ERROR: Failed to upload {filename} to {bucket_name}", exc_info=e)
            return

        if remove_source:
            try:
                rmtree(source_dir)
            except Exception as e:
                self.logger.error(f"ERROR: Failed to remove {source_dir}", exc_info=e)

    def _get_output_value(self, output_key: str) -> str:
        outputs = get_stack_output(self.stack)

        for item in outputs:
            key = item["OutputKey"]
            val = item["OutputValue"]

            if key == output_key:
                return val

        return None

    def _parse_arguments(self) -> (str, str, str):
        current_dir = Path(__file__).parent

        if self.argument:
            if 'source_dir' in self.argument:
                source_dir = f"{current_dir.parent}/{self.argument['source_dir']}"
            else:
                self.logger.error("ERROR: Value for 'source_dir' not found")
                return

            if 'bucket_name' in self.argument:
                bucket_name = self.argument['bucket_name']
            else:
                self.logger.error("ERROR: Value for 'bucket_name' not found")
                return

            if 'remove_source' in self.argument:
                remove_source = self.argument['remove_source']
            else:
                remove_source = False
        else:
            self.logger.error("ERROR: Required arguments not found")
            return

        return source_dir, bucket_name, remove_source


if __name__ == '__main__':
    h = CopyDirToS3()
    h.run()