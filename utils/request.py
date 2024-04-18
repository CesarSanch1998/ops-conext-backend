import os
import json
from dotenv import load_dotenv
import requests
from utils.definitions import domain,headers,endpoints
from requests.auth import HTTPBasicAuth

# domain = definitions.domain
# headers = definitions.headers

load_dotenv()


def db_request(endpoint: str, data: dict):
    data["API_KEY"] = os.environ["API_KEY"]
    payload = json.dumps(data)
    url = f"{domain}{endpoint}"
    try:
        response = requests.post(url, data=payload, headers=headers, verify=False)
        if response.status_code != requests.codes.ok:
            return {
                "error": True,
                "data": None,
                "message": f"Request failed with status code: {response.status_code}",
            }
        response_json = response.json()
        return response_json
    except requests.RequestException as e:
        return {"error": True, "message": f"An error occurred: {str(e)}", "data": None}
    
def db_request_smartolt(endpoint: str, unique_id_smartolt: str):
    url = f"https://conext.smartolt.com/api{endpoints[endpoint]}/{unique_id_smartolt}"
    
    try:
        response = requests.get(url, headers = {'X-Token':os.environ["API_KEY_SMARTOLT"]},verify=True)
        # print(response.json())
        if response.status_code != requests.codes.ok:
            return {
                "error": True,
                "data": None,
                "message": f"Request failed with status code: {response.status_code}",
            }
        response_json = response.json()
        
        return response_json
    except requests.RequestException as e:
        return {"error": True, "message": f"An error occurred: {str(e)}", "data": None}

