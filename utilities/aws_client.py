import logging

from boto3 import Session
from boto3_type_annotations import support
from sceptre.stack import Stack


def get_client(sceptre_context: Stack, service: str) -> support.client:
    try:
        session = Session(profile_name=sceptre_context.profile)
        client = session.client(service, region_name=sceptre_context.region)

        return client
    except Exception as e:
        logging.critical(f"FATAL ERROR: {e}")


def get_resource(sceptre_context: Stack, service: str) -> support.client:
    try:
        session = Session(profile_name=sceptre_context.profile)
        resource = session.resource(service, region_name=sceptre_context.region)

        return resource
    except Exception as e:
        logging.critical(f"FATAL ERROR: {e}")


def get_stack(sceptre_context: Stack, stack_name: str = '') -> dict:
    cloudfm = get_client(sceptre_context, 'cloudformation')

    try:
        if not stack_name:
            stack_name = sceptre_context.external_name

        response = cloudfm.describe_stacks(StackName=stack_name)
        return response['Stacks'][0]
    except Exception as e:
        raise

def get_stack_output(sceptre_context: Stack, stack_name: str = '') -> dict:
    cloudfm = get_client(sceptre_context, 'cloudformation')

    try:
        if not stack_name:
            stack_name = sceptre_context.external_name

        response = cloudfm.describe_stacks(StackName=stack_name)
        return response['Stacks'][0]['Outputs']
    except Exception as e:
        raise

