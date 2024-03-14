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
def querie(input):
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
        # a 503 error is parsed when the server is overloaded, because we can't verify html there are some minor errors
        if "503" in str(http_err):
            time.sleep(2)
            return(querie(input))
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
if __name__ == "__main__":
    print(querie(input()))