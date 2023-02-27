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
            message = f"{len(outputs)} output value found for: {self.stack.external_name}"

            self.logger.info(f"{len(message)*'='}")
            self.logger.info(message)
            self.logger.info(f"{len(message)*'-'}")

            for item in outputs:
                key = item['OutputKey']
                val = item['OutputValue']

                self.logger.info(
                    f"{key}: {val}"
                )

            self.logger.info(f"{len(message)*'='}")
        except ClientError as e:
            self.logger.warning(f"WARN: unable to retrieve outputs for {self.argument}, does the stack exist?")


if __name__ == '__main__':
    h = PrintStackOutputs()
    h.run()