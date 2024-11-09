import asyncio

from apis.FileService import file_get
from apis.SchemaService import schema_get
from apis.StorageService import storage_get

# environments list for reference
envs = ["evd", "evt", "weu", "sgp", "psc", "eut", "brs"]
envs_ltops = ["evd-ltops", "evt-ltops", "adme-outerloop", "prod-canary-ltops", "prod-aws-ltops"]

env = "weu"
data_partition = "sandbox-weu-des-prod-testing-e"
file_id = "sandbox-weu-des-prod-testing-e:dataset--File.Generic:ee7ae678-8a36-4b4a-a153-7a29d1aa2d61"
schema_id = "osdu:wks:dataset--File.Generic:1.0.0"


if __name__ == "__main__":

    asyncio.run(file_get(env, data_partition, file_id))
    asyncio.run(storage_get(env, data_partition, file_id))
    asyncio.run(schema_get(env, data_partition, schema_id))
