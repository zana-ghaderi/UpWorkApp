from fastapi import FastAPI
from Intuit.UpWork.src.api.user_routes import router as user_router
from Intuit.UpWork.src.api.user_routes import router as job_router
from Intuit.UpWork.src.api.user_routes import router as application_router


app = FastAPI()

app.include_router(user_router, prefix="/api")
app.include_router(job_router, prefix="/api")
app.include_router(application_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Upwork Clone API"}
