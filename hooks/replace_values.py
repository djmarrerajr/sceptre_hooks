from os import path, walk
from pathlib import Path
from shutil import rmtree, copytree

from sceptre.hooks import Hook

from utilities.aws_client import get_stack_output


class ReplaceValues(Hook):
    """
        This hook will recursively process each of the files located within the
        path specified by 'source_dir' and replace each of the 'values_to_replace'
        with a new value writing to output to 'target_dir'

        Arguments (passed in as a dict):
            NONE

        Example Usage:
            hooks:
                after_create:
                    - !replace_values
                        source_dir: 'path containing files to update'
                        target_dir: 'path to write updated files'
                        replacements:
                            -   value_to_replace_1: '!stack_output:value-to-replace-it-with'
                                value_to_replace_2: 'value-to-replace-it-with'
    """

    def __init__(self, *args, **kwargs):
        super(ReplaceValues, self).__init__(*args, **kwargs)

    def run(self):
        source_dir, target_dir, replacements = self._parse_arguments()

        if source_dir and target_dir and replacements:
            self._replace_values(source_dir, target_dir, replacements)

    def _get_output_value(self, output_key: str) -> str:
        outputs = get_stack_output(self.stack)

        for item in outputs:
            key = item["OutputKey"]
            val = item["OutputValue"]

            if key == output_key:
                return val

        return None

    def _replace_values(self, source_dir, target_dir, replacements):
        self.logger.info(f"Performing necessary replacements in {source_dir}")

        if path.exists(target_dir):
            rmtree(target_dir, ignore_errors=True)

        copytree(source_dir, target_dir, dirs_exist_ok=True)

        source_files = set()

        for current_dir, subdirs, files in walk(target_dir):
            for filename in files:
                relative_path = path.join(current_dir, filename)
                absolute_path = path.abspath(relative_path)

                source_files.add(absolute_path)

        for file in source_files:
            try:
                with open(file, 'r') as source:
                    source_data = source.read()

                for item in replacements:
                    for token, new_value in item.items():
                        token = f"::{token}::"

                        if new_value.startswith('!stack_output:'):
                            stack_key = new_value.replace('!stack_output:', '')
                            new_value = self._get_output_value(stack_key)

                        if not new_value:
                            self.logger.warning(f"WARNING: Could not locate value for stack output: {stack_key}")
                            continue

                        source_data = source_data.replace(token, new_value)
                        source_data = source_data.replace(token.upper(), new_value)

                with open(file, 'w') as target:
                    target.write(source_data)
            except Exception as e:
                self.logger.error(f"ERROR: Unable to complete value replacements in {file}", exc_info=e)

    def _parse_arguments(self) -> (str, str, str):
        current_dir = Path(__file__).parent

        if self.argument:
            if 'source_dir' in self.argument:
                source_dir = f"{current_dir.parent}/{self.argument['source_dir']}"
            else:
                self.logger.error("ERROR: Value for 'source_dir' not found")
                return

            if 'target_dir' in self.argument:
                target_dir = f"{current_dir.parent}/{self.argument['target_dir']}"
            else:
                self.logger.error("ERROR: Value for 'target_dir' not found")
                return

            if 'replacements' in self.argument:
                replacements = self.argument['replacements']
            else:
                self.logger.error("ERROR: Value for 'replacements' not found")
                return
        else:
            self.logger.error("ERROR: Required arguments not found")
            return

        return source_dir, target_dir, replacements


if __name__ == '__main__':
    h = ReplaceValues()
    h.run()
