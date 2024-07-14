from fastapi import FastAPI
from routers import contacts, users
from dependencies.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import aioredis

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.router, prefix="/api/v1")
app.include_router(contacts.router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contact Management API"}


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    await FastAPILimiter.init(redis)

