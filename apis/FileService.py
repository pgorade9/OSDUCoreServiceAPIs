import asyncio
import json

import aiohttp

from configuration import keyvault
from constants.Constants import OUTPUT_DIR
from utils.TokenUtils import get_token


async def get_metadata_from_file_async(session, env, data_partition, file_id):
    DNS_HOST = keyvault[env]["adme_dns_host"]
    BASE_URL = "/api/file/v2/files/"
    TAIL_PATH = "/metadata"
    url = f"{DNS_HOST}{BASE_URL}{file_id}{TAIL_PATH}"
    headers = {
        "data-partition-id": data_partition,
        "Authorization": get_token(env)
    }
    async with session.get(url=url, headers=headers) as response:
        response_json = await response.json()
        if response.status == 200:
            file_name = response_json['id']

            print(f"Received File with id = {file_name}")
            with open(f"{OUTPUT_DIR}/file_response.json", "w") as fp:
                json.dump(response_json, fp, indent=4)
        elif response.status == 404:
            print(f"File Not Found from Storage")
        else:
            print(f"Error occurred while retreiving file from File Service")


async def file_get(env, data_partition, file_id):
    async with aiohttp.ClientSession() as aio_session:
        # tasks = [get_record_from_storage_async(aio_session) for _ in range(100)]
        tasks = [get_metadata_from_file_async(aio_session, env, data_partition, file_id)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    envs = ["evt", "weu", "sgp", "psc", "eut", "brs"]
    envs_ltops = ["evd-ltops", "evt-ltops", "adme-outerloop", "prod-canary-ltops", "prod-aws-ltops"]

    env = "weu"
    data_partition = "sandbox-weu-des-prod-testing-e"
    file_id = "sandbox-weu-des-prod-testing-e:dataset--File.Generic:ee7ae678-8a36-4b4a-a153-7a29d1aa2d61"
    asyncio.run(file_get(env, data_partition, file_id))
