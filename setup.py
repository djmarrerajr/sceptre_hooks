from setuptools import setup

setup(
    name="sceptre_hooks",
    packages=['hooks'],
    py_modules=[
        'print_outputs',
        'empty_bucket',
        'replace_values',
    ],
    entry_points={
        'sceptre.hooks': [
            'print_outputs = hooks.print_outputs:PrintStackOutputs',
            'empty_bucket = hooks.empty_bucket:EmptyBucket',
            'replace_values = hooks.replace_values:ReplaceValues',
        ]
    }
)