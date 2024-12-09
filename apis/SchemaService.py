import asyncio
import json

import aiohttp

from configuration import keyvault
from constants.Constants import OUTPUT_DIR
from utils.TokenUtils import get_token


async def get_schema_async(session, env, data_partition, schema_id):
    DNS_HOST = keyvault[env]["adme_dns_host"]
    BASE_URL = "/api/schema-service/v1/schema/"

    url = f"{DNS_HOST}{BASE_URL}{schema_id}"
    headers = {
        "data-partition-id": data_partition,
        "Authorization": get_token(env)
    }
    try:
        async with session.get(url=url, headers=headers) as response:
            response_json = await response.json()
            if response.status == 200:
                file_name = response_json['id']
                print(f"Schema Retreived successfully with id = {file_name}")
                with open(f"{OUTPUT_DIR}/schema_response.json", "w") as fp:
                    json.dump(response_json, fp, indent=4)
                return response_json
            elif response.status == 404:
                print(f"Schema Not Found from Storage")
                return response_json

    except Exception as e:
        print(f"Error occurred while retrieving file from Storage. {e} ")
        return response_json


async def schema_get(env, data_partition, schema_id):
    async with aiohttp.ClientSession() as aio_session:
        # tasks = [get_record_from_storage_async(aio_session) for _ in range(100)]
        # tasks = [get_schema_async(aio_session, env, data_partition, schema_id)]
        return await get_schema_async(aio_session, env, data_partition, schema_id)


if __name__ == "__main__":

    envs = ["evt", "weu", "sgp", "psc", "eut", "brs"]
    envs_ltops = ["evd-ltops", "evt-ltops", "adme-outerloop", "prod-canary-ltops", "prod-aws-ltops"]

    env = "evt"
    data_partition = "opendes"
    schema_id = "osdu:wks:dataset--File.Generic:1.0.0"
    asyncio.run(schema_get(env, data_partition, schema_id))
