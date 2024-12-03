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
    try:
        async with session.get(url=url, headers=headers) as response:
            response_json = await response.json()

            if response.status == 200:
                file_name = response_json['id']

                print(f"Record Retreived successfully with id = {file_name}")
                with open(f"{OUTPUT_DIR}/storage_response.json", "w") as fp:
                    json.dump(response_json, fp, indent=4)
            elif response.status == 404:
                print(f"File Not Found from Storage")
    except Exception as e:
        print(f"Error occurred while retrieving file from Storage. {e} ")


async def storage_get(env, data_partition, file_id):
    async with aiohttp.ClientSession() as aio_session:
        tasks = [get_record_from_storage_async(aio_session, env, data_partition, file_id)]
        await asyncio.gather(*tasks)


async def delete_record_from_storage_async(session, env, data_partition, file_id):
    DNS_HOST = keyvault[env]["adme_dns_host"]
    BASE_URL = "/api/storage/v2/records/"

    url = f"{DNS_HOST}{BASE_URL}{file_id}"
    headers = {
        "data-partition-id": data_partition,
        "Authorization": get_token(env)
    }
    async with session.delete(url=url, headers=headers) as response:
        response_json = await response.json(content_type=None)
        if response.status == 204:
            print(f"Record deleted successfully with id = {file_id}")
        elif response.status == 400:
            print(f"Validation error.\n{response_json}")
        elif response.status == 403:
            print(f"User not authorized to perform the action.\n{response_json}")
        else:
            print(f"Error occurred while deleting file from Storage.\n{response_json}")


async def storage_delete(env, data_partition, file_id):
    async with aiohttp.ClientSession() as aio_session:
        tasks = [delete_record_from_storage_async(aio_session, env, data_partition, file_id)]
        await asyncio.gather(*tasks)


async def create_record_from_storage_async(session, env, data_partition, file_id):
    DNS_HOST = keyvault[env]["adme_dns_host"]
    BASE_URL = "/api/storage/v2/records"

    url = f"{DNS_HOST}{BASE_URL}"
    headers = {
        "data-partition-id": data_partition,
        "Authorization": get_token(env),
        'Content-Type': 'application/json',
    }
    with open(f"{OUTPUT_DIR}/storage_response.json") as fp:
        payload = [json.loads(fp.read())]
        # print(payload)
    async with session.put(url=url, headers=headers, json=payload) as response:
        response_json = await response.json()
        if response.status == 201:
            print(f"Record created successfully with id = {file_id}")
        elif response.status == 400:
            print(f"Invalid record format.\n{response_json}")
        elif response.status == 403:
            print(f"User not authorized to perform the action.\n{response_json}")
        else:
            print(f"Error occurred while creating file in Storage.\n{response_json}")


async def storage_create(env, data_partition, file_id):
    async with aiohttp.ClientSession() as aio_session:
        tasks = [create_record_from_storage_async(aio_session, env, data_partition, file_id)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    envs = ["evt", "weu", "sgp", "psc", "eut", "brs"]
    envs_ltops = ["evd-ltops", "evt-ltops", "adme-outerloop", "prod-canary-ltops", "prod-aws-ltops"]

    # env = "evt"
    # data_partition = "default-qa-sis-internal-hq"
    # file_id = "default-qa-sis-internal-hq:PersistedSeismicManifest:dc64409b0d78479ebf4f901f34c2f119"
    env = "weu"
    data_partition = "sandbox-weu-des-prod-testing-e"
    file_id = "sandbox-weu-des-prod-testing-e:dataset--File.Generic:ee7ae678-8a36-4b4a-a153-7a29d1aa2d61"
    asyncio.run(storage_get(env, data_partition, file_id))
