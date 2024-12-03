import json
import requests
from configuration import keyvault

from redis import StrictRedis
from redis_cache import RedisCache

client = StrictRedis(host="127.0.0.1", port=6379, decode_responses=True)
cache = RedisCache(redis_client=client)


# @cache.cache()
def get_token(env):
    response = requests.request(method="POST",
                                url=keyvault[env]["token_url"],
                                headers={"content-type": "application/x-www-form-urlencoded"},
                                data=f"grant_type=client_credentials&client_id={keyvault[env]["client_id"]}&client_secret={keyvault[env]["client_secret"]}&scope={keyvault[env]["scope"]}")

    if response.status_code == 200:
        print(f"********* {env} Token Generated Successfully ************")
        response_dict = json.loads(response.text)
        return "Bearer " + response_dict["access_token"]
    else:
        print(f"Error occurred while creating token. {response.text}")
        exit(1)
