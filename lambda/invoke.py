import traceback
import json
from spotipy_lambda import invoked_process
from common import send_email

def handler(event, context):
    try:
        # Refer to the spotipy_lambda.py to get information of options.
        invoked_process()
        send_email()
        return {
            'isBase64Encoded': False,
            'statusCode': 200,
            'headers': {},
            'body': json.dumps({"result": "OK"})
        }
    except BaseException:
        error_message = traceback.format_exc()
        return {
            'isBase64Encoded': False,
            'statusCode': 500,
            'headers': {},
            'body': json.dumps({"result": "NG", "error_message": error_message})
        }
