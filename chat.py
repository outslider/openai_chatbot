import logging
import json
import os
import openai

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.debug(event)
        # TODO implement
        body = json.loads(event['body'])
        response = chatbot(body['text'])

        payload = {
            'type': 'message',
            'text': response
        }
        logger.info(payload)

        return {
            'statusCode': 200,
            'body': json.dumps(payload)
        }
        
    except:
        logger.info("### except")
        logger.error(event)
        


def chatbot(text):
    openai.api_key = os.environ['OPENAI_API_KEY']

    messages = [{"role": "system", "content": "制約条件：あなたは関西出身のAIです。関西弁で応答します。"}]
    messages.append ({"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #model="gpt-4",
        messages=messages,
        temperature=1.0,
    )
    logger.info(response["choices"][0]["message"]["content"])
    return(response["choices"][0]["message"]["content"])

