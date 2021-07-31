# Dining Suggestion Chatbot

A serverless chatbot web app providing dining suggestions.   
Built with Python 3.8, AWS Lambda, AWS Lex and Yelp API.

## Showcase

<img src="https://raw.githubusercontent.com/314pies/Concierge-Chatbot-Dining-Suggestion/main/img%20host/demo.gif" height="300" >  


Try it Yourself: https://314pies.github.io/DiningChatbotDemo/

## Architecture

<img src="https://raw.githubusercontent.com/314pies/Dining-Suggestion-Chatbot/main/img%20host/Archi.PNG" height="360" >  

1. [Front-end](https://github.com/314pies/Dining-Suggestion-Chatbot/tree/main/front%20end) send requests to API Gateway
2. API Gateway invoke [chatbot_response](https://github.com/314pies/Dining-Suggestion-Chatbot/blob/ee0dfacf4b008801cf496b7fd409dbe5ece26977/aws%20lambda/chatbot_response.py#L34) lambda function
3. [chatbot_response](https://github.com/314pies/Dining-Suggestion-Chatbot/blob/ee0dfacf4b008801cf496b7fd409dbe5ece26977/aws%20lambda/chatbot_response.py#L34) called pre-trained [Lex Bot](https://github.com/314pies/Dining-Suggestion-Chatbot/blob/main/ConciergeDinningChatbot_LEX.zip)
4. Repeat steps 1~3 until successfully gathered all information needed to search for restaurants 
5. Invoke yelp API to find recommended restaurants and send them back to clients.
