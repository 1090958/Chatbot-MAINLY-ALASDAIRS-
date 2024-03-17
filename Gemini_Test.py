import os,requests, time, settings
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import HTTPError

# Single line of code that i found to supress warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)# type: ignore


# using some ethical hacking knowledge(ctrl + shift + I), I managed to get a curl command that 
# is executed when sending a message to google gemini. From there just use requests and write a makeshift API

headers = {
    'Content-Type': 'application/json',
}

params = {
    'key': os.getenv('API_KEY', 'AIzaSyCqQIqwbVwFaEBJYcDKmhi-uY-Shk8e6oE'),
}
def query(input):
    json_data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': input,
                    },
                ],
            },
        ],
        'safetySettings': [
            {
                'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
                'threshold': 'BLOCK_ONLY_HIGH',
            },
        ],
        'generationConfig': {
            'stopSequences': [
                'Title',
            ],
            'temperature': 1.0,
            'maxOutputTokens': 100,
            'topP': 0.6,
            'topK': 2,
        },
    }
    response = None
    try:
        response = requests.post(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
        params=params,
        headers=headers,
        json=json_data,
        verify=not settings.restrictive_Network
        )
        response.raise_for_status()
    except HTTPError as http_err:
        # a 503 error is parsed when the server is overloaded, because we can't verify curls, there are some minor errors
        if "503" in str(http_err):
            time.sleep(2)
            return(query(input))
        print(f"{http_err}")
        quit()
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        pass
    
        
    end = """"
          }
        ],
        "role":"""
    return(response.text[response.text.find('text')+8:response.text.find(end)]) # type: ignore

intents = ['attack', 'heal', 'intimidate', 'charm', 'none']
def get_Intent(message):
    for i in range(10):
        response = query(f'return the top 3 possibilities of the user\'s intents from this message, \'{message}\', it may be from one of the following intents:\n -  {'\n -  '.join(intents)}\n Only reply using the top 3 of the intents, in order of descending weight using lowercase letters, with no punctuation or other words, only a space separating each one and the weights of each one')
        count = 0
        print(response)
        for intent in intents:
            if intent in response:
                
                count += 1
                
        if count == 3 and len(response.split()) == 6:
            break
        else:
            print(i)
    output = {}
    for i in range(1,4):
        pass
        #print(i)
    return response
if __name__ == "__main__":
    print(query(input()))