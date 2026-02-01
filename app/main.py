from fastapi import FastAPI
from app.router.v1 import router as v1_router

app = FastAPI(title="My API", version="1.0.0")

app.include_router(v1_router)

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": f"Server: {app.title} is running"}


