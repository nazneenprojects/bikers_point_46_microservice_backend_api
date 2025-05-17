# bikers_point_46_microservice_backend_api
*bikers_point_46_microservice_backend_api* represents backend API with Microservices architecture designed using Python, FastAPI, Azure Cloud, Cosmos NoSQL DB and more.
This is a solid, scalable, cloud-native microservices architecture, and the project structure fully supports CI/CD, testing, observability, and evolution over time.


## Microservice Project Architecture Decesions
1. Why Monorepo?

    Monorepo (current choice):
        All microservices live in one repo
        Centralized CI/CD workflows (shared pipeline templates)
        Easier local development via docker-compose
        Better for small team or solo dev
    Polyrepo (One repo per microservice):
        Cleaner separation of services
        More complex CI/CD (each repo needs its own pipeline)
        Harder to test end-to-end locally unless using remote CI env

2. Why Single DB per Service ?

    Each service owns its data and schema.
    Promotes true microservice independence.
    Prevents tight coupling.
   
   3. Other Aspects ?

       Area	                    Consideration
   Security	        Use JWT auth, and Key Vault for secrets
   Observability	Structured logs (JSON), Prometheus endpoints
   Retry/Timeouts	For Kafka and HTTP calls (via httpx)
   Error Handling	Consistent error schema across services
   Health Checks	Each service should expose /health endpoint
   API Versioning	E.g., /api/v1/products

5. How Scalability is achieved in this Microservice Project?
    
    Independent microservices (can scale individually)

    Kafka for decoupling services & async processing
    
    Cosmos DB (highly scalable NoSQL store)
    
    Docker + Kubernetes (for autoscaling)
    
    Gateway + CI/CD + Monitoring (production best practices)


Optional :

    Independent microservices (can scale individually)
    
    Kafka for decoupling services & async processing
    
    Cosmos DB (highly scalable NoSQL store)
    
    Docker + Kubernetes (for autoscaling)
    
    Gateway + CI/CD + Monitoring (production best practices)

6. Individual Microservice Structure ?

    FastAPI + asyncio
    
    Pydantic for models
    
    Logging, error handling
    
    Kafka producer/consumer (if applicable)
    
    CosmosDB interaction layer
    
    OpenAPI via FastAPI docs
    
    unit tests , integration test per microservices while E2E test at cental location

7. Microservice Development Sequence 
    - Authentication Service
    - User Service
    - Product Services
    - & so on
