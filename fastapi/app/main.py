from fastapi import FastAPI
from api.agent import router as agent_router

app = FastAPI(title="Chat Agent")

app.include_router(agent_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
