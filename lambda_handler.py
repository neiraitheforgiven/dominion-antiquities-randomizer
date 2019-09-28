import json
from randomizer import RandomizeDominion


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    }

    if event['requestContext']['httpMethod'] == 'POST':
        body = json.loads(event['body'] or '')
        if 'sets' in body:
            data = RandomizeDominion(body['sets'])
        else:
            data = RandomizeDominion()
        response['body'] = json.dumps(data)

    return response
