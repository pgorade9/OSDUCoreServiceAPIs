import asyncio
import json

import aiohttp

from configuration import keyvault
from constants.Constants import OUTPUT_DIR
from utils.TokenUtils import get_token


async def search_async(session, env, data_partition, file_id):
    DNS_HOST = keyvault[env]["adme_dns_host"]
    BASE_URL = "/api/search/v2/query"

    url = f"{DNS_HOST}{BASE_URL}"
    headers = {
        "data-partition-id": data_partition,
        "Authorization": get_token(env),
        'Content-Type': 'application/json',
    }
    with open(f"utils/search_query.json") as fp:
        payload = json.loads(fp.read())
        # print(payload)
    async with session.post(url=url, headers=headers, json=payload) as response:
        response_json = await response.json()
        if response.status == 200:
            print(f"Search query successful")
            with open(f"{OUTPUT_DIR}/search_response.json", "w") as fp:
                json.dump(response_json, fp, indent=4)
        elif response.status == 400:
            print(f"Invalid search query.\n{response_json}")
        elif response.status == 403:
            print(f"User not authorized to perform the action.\n{response_json}")
        else:
            print(f"Error occurred while searching query.\n{response_json}")


async def search_query(env, data_partition, file_id):
    async with aiohttp.ClientSession() as aio_session:
        tasks = [search_async(aio_session, env, data_partition, file_id)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    envs = ["evt", "weu", "sgp", "psc", "eut", "brs"]
    envs_ltops = ["evd-ltops", "evt-ltops", "adme-outerloop", "prod-canary-ltops", "prod-aws-ltops"]

    env = "weu"
    data_partition = "sandbox-weu-des-prod-testing-e"
    file_id = "sandbox-weu-des-prod-testing-e:dataset--File.Generic:ee7ae678-8a36-4b4a-a153-7a29d1aa2d61"
    asyncio.run(search_query(env, data_partition, file_id))