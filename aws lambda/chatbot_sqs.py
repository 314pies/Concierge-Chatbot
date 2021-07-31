import json
import boto3
import http.client
import urllib

#yelp configurations
yelp_access_token = 'YELP_ACCESS_TOKEN'

def send_sms_to_phone(phone_number, message):
    print("sending SNS: ", message)
    # comment for money saving
    sns = boto3.client('sns')
    sns.publish(PhoneNumber=phone_number, Message=message)
    
def search_restarants_from_yelp(location, cuisine, limit=3):
    
    #  # curl --location --request GET 'https://api.yelp.com/v3/businesses/search?term=restaurants&location=New%20York&radius=40000&categories=japanese&limit=3' \
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
        

def lambda_handler(event, context):
    print("lambda_handler event:", event)
    print("event body: ", event["Records"][0]["body"])
    
    body = json.loads(event["Records"][0]["body"])
    cuisine = body["Cuisine"]
    dining_time = body["DiningTime"]
    location = body["Location"]
    number_of_people = body["NumberOfPeople"]
    phone_number = body["PhoneNumber"]
    
    restrant_info_list = search_restarants_from_yelp(location, cuisine, limit=3)
    sms_msg = f"Hello!, Here are my {cuisine} restaurant suggestions for {number_of_people} people, for {dining_time}:\n\n"
    for i, info in enumerate(restrant_info_list):
        sms_msg += f"{i+1}. {info['name']} located at {info['address']}\n\n"
    
    sms_msg += "Enjoy your meal !!!"
    
    send_sms_to_phone(phone_number, sms_msg)

    return {
        'statusCode': 200,
    }
