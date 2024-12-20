from fastapi import FastAPI, Path
from app.dependencies.database import Base, engine
from app.api.v1.api import api_router
import uvicorn

Base.metadata.create_all(engine)

app = FastAPI()        

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router)

# for debugging
if __name__ == '__main__':
    uvicorn.run(f"{Path(__file__).stem}:app", host="127.0.0.1", port=8888, reload=True)






