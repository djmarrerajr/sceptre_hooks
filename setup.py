from setuptools import setup

setup(
    name="sceptre_hooks",
    packages=['hooks'],
    py_modules=[
        'print_outputs',
    ],
    entry_points={
        'sceptre.hooks': [
            'print_outputs = hooks.print_outputs:PrintStackOutputs',
        ]
    }
)