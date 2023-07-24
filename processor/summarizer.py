import requests
from bot import send, config

API_URL_CNN = config['API_URL_CNN']
API_URL_CNN2 = config['API_URL_CNN2']
API_URL_XSUM = config['API_URL_XSUM']

hf_api = config['hf_api']

headers = {"Authorization": hf_api}

async def summarize(para, update):
    
    """
    This function takes in a paragraph and an update object as input and returns a summary of the paragraph.
    
    The function makes use of external APIs to generate the summary, using a fallback mechanism if one API is unreachable or returns an error.
    
    The order of preference for the APIs is: API_URL_CNN, API_URL_CNN2, API_URL_XSUM.
    
    If none of the APIs are reachable or return an error, an error message is sent using the update object.
    
    :param para: The paragraph to be summarized.
    :param update: The update object used to send messages.
    :return: None
    """

    payload = {"inputs": para}
    try:
        response = requests.post(API_URL_CNN, headers=headers, json=payload)
        if response.status_code != 200 or "Error" in response.json():
            response = requests.post(API_URL_CNN2, headers=headers, json=payload)
            if response.status_code != 200 or "Error" in response.json():
                response = requests.post(API_URL_XSUM, headers=headers, json=payload)
                if response.status_code != 200 or "Error" in response.json():
                    message = "Unable to reach servers"
                    await send(message, update)
                    return
        message = response.json()[0]['summary_text']
        await send(message, update)
    except Exception as e:
        message = "Unable to reach servers"
        await send(message, update)