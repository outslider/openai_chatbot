import logging
import json
import os
import openai
import requests

WEBHOOK_URL = os.environ['WEBHOOK_URL']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):

    logger.debug(event)
    body = json.loads(event['body'])
    res = chatbot(body['text'])
    post_to_teams(res)

    return 
    {
        'statusCode': 200,
        'body': ''
    }


def chatbot(text):

    openai.api_key = os.environ['OPENAI_API_KEY']

    messages = [{"role": "system", "content": "制約条件：あなたは関西出身のAIで す。関西弁で応答します。"}]
    messages.append ({"role": "user", "content": text})
    try:
        response = openai.ChatCompletion.create(
            #model="gpt-3.5-turbo",
            model="gpt-4",
            messages=messages,
            temperature=1.0,
        )
    except:
        logger.error("openai request exception." + response)

    logger.info("openai response: " + response["choices"][0]["message"]["content"])
    return(response["choices"][0]["message"]["content"])
    


def post_to_teams(text):

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "text": text
    }
    logger.debug("post_to_teams: send text= " + text)
    try:
        response = requests.post(
            WEBHOOK_URL,
            headers=headers,
            data=json.dumps(payload)
        )
    except:
        logger.info("post_to_teams: ### except" + event)

    if response.status_code == 200:
        logger.info("success")
    else:
        logger.info("failed: %s" % respnse.text)

    return()
