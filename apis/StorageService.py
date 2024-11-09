import asyncio
import json

import aiohttp

from configuration import keyvault
from constants.Constants import OUTPUT_DIR
from utils.TokenUtils import get_token


async def get_record_from_storage_async(session, env, data_partition, file_id):
    DNS_HOST = keyvault[env]["adme_dns_host"]
    BASE_URL = "/api/storage/v2/records/"

    url = f"{DNS_HOST}{BASE_URL}{file_id}"
    headers = {
        "data-partition-id": data_partition,
        "Authorization": get_token(env)
    }
    async with session.get(url=url, headers=headers) as response:
        response_json = await response.json()
        file_name = response_json['id']

        print(f"Received File from Storage with id = {file_name}")
        with open(f"{OUTPUT_DIR}/storage_response.json", "w") as fp:
            json.dump(response_json, fp, indent=4)

async def storage_get(env, data_partition, file_id):
    async with aiohttp.ClientSession() as aio_session:
        tasks = [get_record_from_storage_async(aio_session, env, data_partition, file_id)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":

    envs = ["evt", "weu", "sgp", "psc", "eut", "brs"]
    envs_ltops = ["evd-ltops", "evt-ltops", "adme-outerloop", "prod-canary-ltops", "prod-aws-ltops"]

    env = "weu"
    data_partition = "sandbox-weu-des-prod-testing-e"
    file_id = "sandbox-weu-des-prod-testing-e:dataset--File.Generic:ee7ae678-8a36-4b4a-a153-7a29d1aa2d61"
    asyncio.run(storage_get(env, data_partition, file_id))
