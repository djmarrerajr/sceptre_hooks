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


class AwsClient:
    """
        AwsClient is a utility class that can be used bye custom Sceptre hooks
        as an abstraction layer around boto3 to provide profile/region sensitive
        clients.
    """

    def __init__(self, *args, **kwargs):
        super(AwsClient, self).__init__(*args, **kwargs)
