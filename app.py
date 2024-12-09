import asyncio

from apis.FileService import file_get
from apis.SchemaService import schema_get
from apis.SearchService import search_query
from apis.StorageService import storage_get, storage_create, storage_delete



# environments list for reference
envs = ["evd", "evt", "weu", "sgp", "psc", "eut", "brs"]
envs_ltops = ["evd-ltops", "evt-ltops", "adme-outerloop", "prod-canary-ltops", "prod-aws-ltops"]

# Test Data
# env = "weu"
# data_partition = "sandbox-weu-des-prod-testing-e"
# file_id = "sandbox-weu-des-prod-testing-e:dataset--File.Generic:ee7ae678-8a36-4b4a-a153-7a29d1aa2d61"
# schema_id = "osdu:wks:dataset--File.Generic:1.0.0"

# Test Data
# env = "evd"
# data_partition = "default-dev-sis-internal-hq"
# file_id = "default-dev-sis-internal-hq:dataset--File.Generic:48ec54f2-c3be-449d-8f2d-5331968b73be"
# schema_id = "osdu:wks:dataset--File.Generic:1.0.0"


env = "evt"
data_partition = "default-qa-sis-internal-hq"
# file_id = "default-qa-sis-internal-hq:wks:work-product-component--WellboreMarkerSet:5b718938-3635-4b6b-9d40-447ad5a816db"
file_id = "default-qa-sis-internal-hq:dataset--File.Generic:5b718938-3635-4b6b-9d40-447ad5a816db"



# env = "sgp"
# data_partition = "petronas-osdu"
# file_id = "petronas-osdu:dataset--File.Generic:24b6d71d-1942-4851-8605-7378d8066e02"
# schema_id = "osdu:wks:dataset--File.Generic:1.0.0"

if __name__ == "__main__":
# PLEASE START REDIS BEFORE RUNNING THIS

    asyncio.run(file_get(env, data_partition, file_id))

    # asyncio.run(storage_create(env, data_partition, file_id))
    # asyncio.run(storage_get(env, data_partition, file_id))
    # asyncio.run(storage_delete(env, data_partition, file_id))
    # asyncio.run(storage_create(env, data_partition, file_id))

    # asyncio.run(schema_get(env, data_partition, schema_id))

    # asyncio.run(search_query(env, data_partition, file_id))
