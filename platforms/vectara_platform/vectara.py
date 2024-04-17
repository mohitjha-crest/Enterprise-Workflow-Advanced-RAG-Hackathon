import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

VECTARA_API_KEY = os.environ.get("VECTARA_API_KEY")
VECTARA_CUSTOMER_ID = os.environ.get("VECTARA_CUSTOMER_ID")


def request_vectara(query: str):

    url = "https://api.vectara.io/v1/query"

    payload = json.dumps({
        "query": [
            {
                "query": query,
                "start": 0,
                "numResults": 1,
                "contextConfig": {
                    "sentences_before": 0,
                    "sentences_after": 100,
                    "start_tag": "<b>",
                    "end_tag": "</b>"
                },
                "corpusKey": [
                    {
                        "corpus_id": 2
                    }
                ],
                "summary": [
                    {
                        "max_summarized_results": 1,
                        "response_lang": "en"
                    }
                ]
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'customer-id': VECTARA_CUSTOMER_ID,
        'x-api-key': VECTARA_API_KEY
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = response.json()
    return response_dict
