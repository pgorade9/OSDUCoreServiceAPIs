import asyncio
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import FastAPI

from apis.FileService import file_get
from apis.SchemaService import schema_get
from apis.StorageService import storage_get

app = FastAPI()
# CORS configuration
origins = [
    "http://localhost:4200",  # Allow Angular app running on localhost:4200
    # Add other origins as needed
]

# Add CORS middleware to allow requests from the specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    return {"hello": "world"}


@app.get("/file")
def index(env: str, id: str, data_partition_id: str):
    return asyncio.run(file_get(env, data_partition_id, id))


@app.get("/storage")
def index(env: str, id: str, data_partition_id: str):
    return asyncio.run(storage_get(env, data_partition_id, id))


@app.get("/schema")
def index(env: str, id: str, data_partition_id: str):
    return asyncio.run(schema_get(env, data_partition_id, id))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
