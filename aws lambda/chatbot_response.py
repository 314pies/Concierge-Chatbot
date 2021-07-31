import json
import boto3
import http.client
import urllib

#YELP CONFIGURATION
yelp_access_token = 'YELP_ACCESS_TOKEN'

#LEX CONFIGURATION
lex_chatbot_name = 'ConciergeDinningChatbot'
lex_bot_alias = 'Production'

#SQS CONFIGURATION
is_send_to_sqs = False
sqs_QueueName = 'HW1ChatBotSQS'


client = boto3.client('lex-runtime')

def send_sqs(message):
  # Get the service resource
  sqs = boto3.resource('sqs')
  
  # Get the queue
  queue = sqs.get_queue_by_name(QueueName=sqs_QueueName)
  
  # Create a new message
  response = queue.send_message(MessageBody = message)
  
  # The response is NOT a resource, but gives you a message ID and MD5
  print("MessageId: ", response.get('MessageId'))
  print("MD5 of MessageBody: ",response.get('MD5OfMessageBody'))

def lambda_handler(event, context):
    # TODO implement
    
    print("lambda_handler event: ",event)
    print("lambda_handler context: ",context)
    
    clientText = event["messages"][0]["unstructured"]["text"]
    response = client.post_text(
        botName=lex_chatbot_name,
        botAlias=lex_bot_alias,
        userId='constant_0',
        sessionAttributes={
            'string': 'string'
        },
        requestAttributes={
            'string': 'string'
        },
        inputText=clientText
    )
    
    print("lex response ",response)
    
    if response["dialogState"] == "ReadyForFulfillment":
      #All set
      
      print("slots: ", response["slots"])
      #Optionaly send it to sqs (In case something wrong occur in run-time)
      if is_send_to_sqs:
        send_sqs(json.dumps(response["slots"]))
      
      lexMessageRep = get_suggestion(json.dumps(response["slots"]))
    else:
      lexMessageRep = response["message"];
    
    
    
    data = {
      "messages": [
        {
          "type": "unstructured",
          "unstructured": {
            "id": "constant_0",
            "text": lexMessageRep,
            "timestamp": "2021-08-10T00:00:00Z"
          }
        }
      ]
    }

    return data

def get_suggestion(bodyStr):
    body = json.loads(bodyStr)
    cuisine = body["Cuisine"]
    dining_time = body["DiningTime"]
    location = body["Location"]
    number_of_people = body["NumberOfPeople"]
    phone_number = body["PhoneNumber"]
    
    restrant_info_list = search_restarants_from_yelp(location, cuisine, limit=3)
    return_msg = f"OK! Here's my {cuisine} restaurant suggestions for {number_of_people} people on {dining_time}:\n\n"
    for i, info in enumerate(restrant_info_list):
        return_msg += "<p style=\"text-align:left;\">" + f"{i+1}. {info['name']}, at {info['address']}\n\n </p>"
    
    return_msg += "Enjoy your meal !!!"
    
    return return_msg


def search_restarants_from_yelp(location, cuisine, limit=3):
    
    # curl --location --request GET 'https://api.yelp.com/v3/businesses/search?term=restaurants&location=New%20York&radius=40000&categories=japanese&limit=3' \
    # --header 'Authorization: Bearer YELP_ACCESS_TOKEN'

    conn = http.client.HTTPSConnection("api.yelp.com")
    payload = ''
    headers = {
      'Authorization': 'Bearer ' + yelp_access_token
    }
    
    location = urllib.parse.quote(location.lower())
    cuisine = urllib.parse.quote(cuisine.lower())
    
    conn.request("GET", f"/v3/businesses/search?term=restaurants&location={location}&radius=40000&categories={cuisine}&limit=3", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    print('yelp response: ', data)
    
    res = []
    for b in data['businesses']:
        restrant_info = {
            'name': b['name'],
            'address': ', '.join(b['location']['display_address'])
        }
        res.append(restrant_info)
    return res
