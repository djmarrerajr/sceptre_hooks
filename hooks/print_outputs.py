from botocore.exceptions import ClientError
from sceptre.hooks import Hook

from utilities.aws_client import get_stack_output


class PrintStackOutputs(Hook):
    """
        This hook will write the keys/values of all the outputs for the current stack.

        Arguments (passed in as a dict):
            NONE

        Example Usage:
            hooks:
                after_create:
                    - !print_outputs
    """

    def __init__(self, *args, **kwargs):
        super(PrintStackOutputs, self).__init__(*args, **kwargs)

    def run(self):
        try:
            outputs = get_stack_output(self.stack)

            self.logger.info(f"{(len(self.stack.external_name)+13)*'-'}")
            self.logger.info(f"Outputs for: {self.stack.external_name}")
            self.logger.info(f"{(len(self.stack.external_name)+13)*'-'}")

            for item in outputs:
                key = item['OutputKey']
                val = item['OutputValue']

                self.logger.info(
                    f"{key}: {val}"
                )
        except ClientError as e:
            self.logger.exception(
                f"ERROR: While trying to retrieve output for stack {self.stack.external_name}", exc_info=e
            )
        except Exception as e:
            self.logger.exception(
                f"UNEXPECTED ERROR: While trying to retrieve output for stack {self.stack.external_name}", exc_info=e
            )


if __name__ == '__main__':
    h = PrintStackOutputs()
    h.run()