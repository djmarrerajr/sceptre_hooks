from setuptools import setup

setup(
    name='sceptre_hooks',
    version='0.0.1',
    description='Sceptre Hooks',
    author='Dan Marrera',
    author_email='dan@marrera.com',
    py_modules=[
        'hooks.print_outputs',
        'hooks.empty_bucket',
        'hook.sreplace_values',
    ],
    requires=[
        'boto3',
        'sceptre',
        'setuptools',
    ],
    entry_points={
        'sceptre.hooks': [
            'print_outputs = hooks.print_outputs:PrintStackOutputs',
            'empty_bucket = hooks.empty_bucket:EmptyBucket',
            'replace_values = hooks.replace_values:ReplaceValues',
        ]
    }
)