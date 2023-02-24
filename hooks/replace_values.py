from sceptre.hooks import Hook

from utilities.aws_client import get_client


class ReplaceValues(Hook):
    """
        Arguments (passed in as a dict):
            NONE

        Example Usage:
            hooks:
                after_create:
                    - !replace_values
    """

    def __init__(self, *args, **kwargs):
        super(ReplaceValues, self).__init__(*args, **kwargs)

    def run(self):
        cloudfm = get_client(self.stack, 'cloudformation')

        self.logger.info(
            f"Executing {__name__}"
        )

        try:
            response = cloudfm.describe_stacks(StackName=self.stack.external_name)
            outputs = response['Stacks'][0]['Outputs']

            for item in outputs:
                key = item['OutputKey']
                val = item['OutputValue']

                self.logger.info(
                    f"{key}: {val}"
                )
        except Exception as e:
            self.logger.fatal(
                f"FATAL ERROR: {e}"
            )


if __name__ == '__main__':
    h = ReplaceValues()
    h.run()