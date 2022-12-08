import spotipy
import spotipy.util as util
import ast
import base64
import boto3
from botocore.exceptions import ClientError
import random
import os


username = 'Hikaru'
scope = 'playlist-read-private playlist-modify-public'
playlist_id = '07bihVSXGsycvuii4zNuMu'


def get_random_search():
    """
    Get a random character of unicode.
    """

    rand_char = ''

    while rand_char == '':
        rand_char = chr(random.randint(0, 1114111))

    randomSearch = ''

    if random.randint(0, 2) == 0:
        randomSearch = rand_char + '%'
    elif random.randint(0, 2) == 1:
        randomSearch = '%' + rand_char + '%'
    else:
        randomSearch = '%' + rand_char

    return randomSearch


def get_secret():
    """
    Get secrets values from AWS Secrets Manager.
    """

    secret_name = "spotipy-secret"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    else:
        if 'SecretString' in get_secret_value_response:
            secret_raw = get_secret_value_response['SecretString']
        else:
            secret_raw = base64.b64decode(
                get_secret_value_response['SecretBinary'])

    # Convert secrets into dictionary object.
    secret = ast.literal_eval(secret_raw)

    return secret


def authenticate():
    """
    Execute authentication on process spotify.
    """
    secret = get_secret()

    token = util.prompt_for_user_token(
        username, scope, secret['my_id'], secret['my_secret'], secret['redirect_uri'])

    sp = spotipy.Spotify(auth=token)

    return sp


def send_email():

    region_name = "us-east-1"

    # Create a SNS client
    session = boto3.session.Session()
    client = session.client(
        service_name='sns',
        region_name=region_name
    )
    params = {
        'TopicArn': os.environ['TOPIC_ARN'],
        'Subject': 'Lambda process completed!',
        'Message': 'Your request has been successfully processed!'
    }

    client.publish(**params)
