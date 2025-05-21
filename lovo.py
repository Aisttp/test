import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
comprehend = boto3.client('comprehend')

table_name = 'Baza'

def lambda_handler(event, context):
    body = json.loads(event['body'])
    data_text = body['baza']
    data_id = str(uuid.uuid4())
   
    response_sentiment = comprehend.detect_sentiment(
        Text = data_text,
        LanguageCode = 'en'
    )
    
    table = dynamodb.Table(table_name)
    table.put_item(
        Item = {
            'BazaID': data_id,
            'BazaText': data_text,
            'Sentiment': response_sentiment['Sentiment'] 
        }
    )

    response = {
        'statusCode':200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'BazaID': data_id,
            'Sentiment': response_sentiment['Sentiment']
        })
    }
    return response
 