from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
from azure.cosmos.aio import CosmosClient
from azure.cosmos import PartitionKey, exceptions

#from app.auth.routes import router as auth_router

from app.auth.routes import router as auth_router

config = dotenv_values(".env")
app = FastAPI(
    title="Bikers Point 46 Auth Service",
    description="Authentication microservice for Bikers Point 46",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_NAME = "bikerpoint-auth-db"
CONTAINER_NAME = "users"

@app.on_event("startup")
async def startup_db_client():
    app.cosmos_client = CosmosClient(config["COSMOS_DB_URL"], credential=config["COSMOS_KEY"])
    await get_or_create_db(DATABASE_NAME)
    await get_or_create_container(CONTAINER_NAME)

async def get_or_create_db(db_name):
    try:
        app.database = app.cosmos_client.get_database_client(db_name)
        return await app.database.read()
    except exceptions.CosmosResourceNotFoundError:
        print("Creating database")
        return await app.cosmos_client.create_database(db_name)

async def get_or_create_container(container_name):
    try:
        app.user_container = app.database.get_container_client(container_name)
        return await app.user_container.read()
    except exceptions.CosmosResourceNotFoundError:
        print("Creating container with id as partition key")
        return await app.database.create_container(id=container_name, partition_key=PartitionKey(path="/id"))
    except exceptions.CosmosHttpResponseError:
        raise

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to Bikers Point 46 Auth Service", "docs": "/api/v1/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth-service"}